"""Offline tests for lib: metadata limits, URL parsing, approval gate. No network."""
from __future__ import annotations

import pathlib
import subprocess
import sys
import unittest
from datetime import datetime, timedelta, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib import fingerprint, parse_chapters, parse_youtube_url, tags_length, validate_metadata, verify_confirmation  # noqa: E402
from lib.metadata import has_errors  # noqa: E402
from lib.youtube_client import iso8601_duration_to_seconds, outlier_scores  # noqa: E402

GOOD = {
    "title": "Cómo editar vídeos el doble de rápido en DaVinci Resolve",
    "description": "Aprende el flujo exacto que uso para editar un vídeo de 10 minutos en 2 horas en DaVinci Resolve.\n\n"
    "00:00 El problema\n00:45 Atajos clave\n03:10 Plantillas\n06:00 Exportar\n\n#davinciresolve #edicion",
    "tags": ["davinci resolve", "edición de vídeo", "atajos"],
    "categoryId": "27",
    "privacyStatus": "private",
    "madeForKids": False,
}


def errors(meta, **kw):
    return [i for i in validate_metadata(meta, **kw) if i.level == "error"]


class Metadata(unittest.TestCase):
    def test_good_payload_has_no_errors(self):
        self.assertEqual(errors(GOOD, duration_seconds=600), [])

    def test_title_limits(self):
        self.assertTrue(errors({**GOOD, "title": "x" * 101}))
        self.assertTrue(errors({**GOOD, "title": ""}))
        self.assertTrue(errors({**GOOD, "title": "a <b> title"}))

    def test_description_bytes_not_chars(self):
        # "é" is 2 bytes: 2600 chars = 5200 bytes > 5000
        self.assertTrue(errors({**GOOD, "description": "é" * 2600}))
        self.assertFalse(errors({**GOOD, "description": "e" * 4999 + "\n"}))

    def test_hashtags_over_15_is_error(self):
        tags = " ".join(f"#t{i}" for i in range(16))
        self.assertTrue(errors({**GOOD, "description": "A long enough first line for the description check.\n" + tags}))

    def test_tags_length_counts_quotes_and_commas(self):
        self.assertEqual(tags_length(["ab", "c d"]), 2 + (3 + 2) + 1)
        self.assertTrue(errors({**GOOD, "tags": ["x" * 250, "y" * 251]}))

    def test_chapters(self):
        self.assertEqual(parse_chapters("0:00 Intro\n1:05:10 Late\nnot a chapter"), [(0, "Intro"), (3910, "Late")])
        bad_start = {**GOOD, "description": "First line long enough to pass the soft check.\n0:05 A\n1:00 B\n2:00 C"}
        self.assertTrue(errors(bad_start))
        too_few = {**GOOD, "description": "First line long enough to pass the soft check.\n0:00 A\n1:00 B"}
        self.assertTrue(errors(too_few))
        too_short = {**GOOD, "description": "First line long enough to pass the soft check.\n0:00 A\n0:05 B\n1:00 C"}
        self.assertTrue(errors(too_short))
        past_end = errors(GOOD, duration_seconds=300)
        self.assertTrue(any("after the video ends" in i.message for i in past_end))

    def test_made_for_kids_must_be_declared(self):
        meta = dict(GOOD)
        meta.pop("madeForKids")
        self.assertTrue(errors(meta))

    def test_schedule_requires_private_and_future(self):
        future = (datetime.now(timezone.utc) + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.assertFalse(errors({**GOOD, "publishAt": future}))
        self.assertTrue(errors({**GOOD, "publishAt": future, "privacyStatus": "public"}))
        self.assertTrue(errors({**GOOD, "publishAt": "2020-01-01T00:00:00Z"}))
        self.assertTrue(errors({**GOOD, "publishAt": "2030-01-01T00:00:00"}))  # no timezone

    def test_shorts_max_length(self):
        self.assertTrue(errors({**GOOD, "isShort": True}, duration_seconds=181))
        self.assertFalse(has_errors(validate_metadata({**GOOD, "isShort": True, "description": ""}, duration_seconds=59)))


class UrlParser(unittest.TestCase):
    def test_video_forms(self):
        for url in (
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s",
            "https://youtu.be/dQw4w9WgXcQ",
            "youtube.com/embed/dQw4w9WgXcQ",
            "dQw4w9WgXcQ",
        ):
            self.assertEqual(parse_youtube_url(url).video_id, "dQw4w9WgXcQ", url)
        self.assertEqual(parse_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1m5s").start_seconds, 65)

    def test_short_live_comment(self):
        self.assertEqual(parse_youtube_url("https://youtube.com/shorts/dQw4w9WgXcQ").kind, "short")
        self.assertEqual(parse_youtube_url("https://www.youtube.com/live/dQw4w9WgXcQ").kind, "live")
        p = parse_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ&lc=UgzAbc123")
        self.assertEqual(p.comment_id, "UgzAbc123")

    def test_channel_handle_playlist(self):
        self.assertEqual(parse_youtube_url("https://www.youtube.com/@mkbhd").handle, "@mkbhd")
        cid = "UC" + "a" * 22
        self.assertEqual(parse_youtube_url(f"https://www.youtube.com/channel/{cid}").channel_id, cid)
        self.assertEqual(parse_youtube_url("https://www.youtube.com/playlist?list=PL123").playlist_id, "PL123")

    def test_rejects_other_hosts(self):
        self.assertEqual(parse_youtube_url("https://evil.example/watch?v=dQw4w9WgXcQ").kind, "unknown")


class Approval(unittest.TestCase):
    def test_fingerprint_is_stable_and_order_independent(self):
        self.assertEqual(fingerprint({"a": 1, "b": 2}), fingerprint({"b": 2, "a": 1}))

    def test_any_change_invalidates(self):
        fp = fingerprint(GOOD)
        self.assertTrue(verify_confirmation(GOOD, fp))
        self.assertFalse(verify_confirmation({**GOOD, "title": GOOD["title"] + "!"}, fp))
        self.assertFalse(verify_confirmation(GOOD, None))
        self.assertFalse(verify_confirmation(GOOD, ""))


class ClientHelpers(unittest.TestCase):
    def test_duration(self):
        self.assertEqual(iso8601_duration_to_seconds("PT1H2M3S"), 3723)
        self.assertEqual(iso8601_duration_to_seconds("PT45S"), 45)
        self.assertEqual(iso8601_duration_to_seconds("P1DT1S"), 86401)

    def test_outlier_scores(self):
        vids = [
            {"id": str(i), "snippet": {"title": f"v{i}", "publishedAt": "2026-01-01T00:00:00Z"}, "statistics": {"viewCount": str(v)}, "contentDetails": {"duration": "PT10M"}}
            for i, v in enumerate([100, 100, 100, 500])
        ]
        rows = outlier_scores(vids)
        self.assertEqual(rows[0]["video_id"], "3")
        self.assertEqual(rows[0]["outlier"], 5.0)


class Bundle(unittest.TestCase):
    def test_check_skills_passes(self):
        res = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_skills.py")], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)

    def test_validator_cli_exit_codes(self):
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as d:
            good = pathlib.Path(d) / "good.json"
            bad = pathlib.Path(d) / "bad.json"
            good.write_text(json.dumps(GOOD), encoding="utf-8")
            bad.write_text(json.dumps({**GOOD, "title": "x" * 120}), encoding="utf-8")
            script = str(ROOT / "scripts" / "validate_metadata.py")
            self.assertEqual(subprocess.run([sys.executable, script, str(good), "--duration", "600"], capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run([sys.executable, script, str(bad)], capture_output=True).returncode, 1)

    def test_write_scripts_use_approval_gate(self):
        for name in ("publish_video.py", "update_video.py", "reply_comments.py"):
            text = (ROOT / "scripts" / name).read_text(encoding="utf-8")
            self.assertIn("verify_confirmation", text, name)
            self.assertIn("--confirm", text, name)


if __name__ == "__main__":
    unittest.main()
