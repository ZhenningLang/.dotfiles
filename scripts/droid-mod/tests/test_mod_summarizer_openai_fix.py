import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path("/Users/zhenninglang/.dotfiles/scripts/droid-mod/mods/mod_summarizer_openai_fix.py")
STATUS = Path("/Users/zhenninglang/.dotfiles/scripts/droid-mod/status.py")

ORIGINAL_BYTES = (
    b'provider==="openai")return(await new OA({apiKey:N.apiKey,baseURL:N.baseUrl,organization:null,project:null,defaultHeaders:N.extraHeaders}).responses.create({model:M,input:I,store:!1,instructions:J,max_output_tokens:K})).output_text;if(N&&N.provider==="generic-chat-completion-api"){'
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


class ModSummarizerOpenAIFixTests(unittest.TestCase):
    def test_patches_openai_summarizer_path_and_status_detects_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir)
            droid = _write_droid(home, ORIGINAL_BYTES)

            result = _run(SCRIPT, home)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            patched = droid.read_bytes()
            self.assertEqual(len(patched) - len(ORIGINAL_BYTES), 28)
            self.assertIn(b'provider==="openai"&&!1)return(', patched)
            self.assertIn(
                b'if(N&&(N.provider==="generic-chat-completion-api"||N.provider=="openai")){',
                patched,
            )
            self.assertNotIn(
                b'if(N&&N.provider==="generic-chat-completion-api"){',
                patched,
            )

            rerun = _run(SCRIPT, home)
            self.assertEqual(rerun.returncode, 0, rerun.stdout + rerun.stderr)
            self.assertIn("已应用", rerun.stdout)

            status = _run(STATUS, home)
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn("mod-summarizer-openai-fix: 已修改", status.stdout)


if __name__ == "__main__":
    unittest.main()
