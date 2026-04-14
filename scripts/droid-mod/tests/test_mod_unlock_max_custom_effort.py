import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path("/Users/zhenninglang/.dotfiles/scripts/droid-mod/mods/mod_unlock_max_custom_effort.py")
STATUS = Path("/Users/zhenninglang/.dotfiles/scripts/droid-mod/status.py")

ORIGINAL_BYTES = (
    b'id:C.id,displayName:C.displayName,shortDisplayName:C.displayName,modelProvider:C.provider,'
    b'supportedReasoningEfforts:h?["off","low","medium","high"]:["none"],defaultReasoningEffort:C.reasoningEffort??"none",'
    b'isCustom:!0,noImageSupport:C.noImageSupport;'
    b'id:R.model,modelProvider:R.provider,displayName:A,shortDisplayName:A,'
    b'supportedReasoningEfforts:L?["off","low","medium","high"]:["none"],defaultReasoningEffort:R.reasoningEffort??"none",'
    b'isCustom:!0,noImageSupport:R.noImageSupport'
)


def _write_droid(home: Path, data: bytes) -> Path:
    droid = home / ".local/bin/droid"
    droid.parent.mkdir(parents=True, exist_ok=True)
    droid.write_bytes(data)
    return droid


def _run(script: Path, home: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOME"] = str(home)
    return subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


class ModUnlockMaxCustomEffortTests(unittest.TestCase):
    def test_upgrades_effort_lists_with_compact_provider_aware_patch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir)
            droid = _write_droid(home, ORIGINAL_BYTES)

            result = _run(SCRIPT, home)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            patched = droid.read_bytes()
            self.assertEqual(
                patched.count(b'.provider=="openai"?["none","low","medium","high","xhigh"]:["off","low","medium","high","max"]'),
                1,
            )
            self.assertIn(
                b'supportedReasoningEfforts:L?["off","low","medium","high","max"]:["none"],defaultReasoningEffort:R.reasoningEffort',
                patched,
            )
            self.assertNotIn(b'["off","low","medium","high"]:["none"]', patched)
            self.assertEqual(len(patched) - len(ORIGINAL_BYTES), 72)

            rerun = _run(SCRIPT, home)
            self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
            self.assertIn("已应用", rerun.stdout)

            status = _run(STATUS, home)
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn("mod-unlock-max-custom-effort: 已修改", status.stdout)


if __name__ == "__main__":
    unittest.main()
