import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG = REPO_ROOT / "skills" / "catalog.json"
VERIFY_SCRIPT = REPO_ROOT / "scripts" / "verify_skills.py"


class SkillsRegistryTests(unittest.TestCase):
    RENAMED_LEGACY_NAMES = {
        "frontend-design",
        "ui-design",
        "eng-architecture",
        "eng-check",
        "eng-close",
        "eng-debug",
        "eng-learn",
        "eng-map",
        "eng-plan",
        "eng-quality",
        "eng-readable-metrics",
        "eng-refactor",
        "eng-research",
        "eng-review",
        "eng-secure",
        "eng-ship",
        "eng-tdd",
        "eng-unstuck",
        "eng-verify",
        "se-rewrite-readable",
    }

    CANONICAL_NAMES = {
        "assist-learn",
        "dev-debug",
        "dev-refactor",
        "dev-tdd",
        "fe-ui-design",
        "guard-check",
        "guard-close",
        "guard-review",
        "guard-secure",
        "guard-ship",
        "guard-verify",
        "readable-metrics",
        "readable-rewrite",
        "think-architecture",
        "think-map",
        "think-plan",
        "think-quality",
        "think-research",
        "think-unstuck",
    }

    def test_catalog_exists_and_declares_phase1_skills(self) -> None:
        self.assertTrue(CATALOG.exists(), "skills/catalog.json should exist")
        catalog = json.loads(CATALOG.read_text())
        names = {entry["name"] for entry in catalog["skills"]}
        self.assertIn("web-read", names)
        self.assertIn("agent-health", names)
        self.assertIn("guard-check", names)
        self.assertIn("fe-ui-design", names)
        self.assertIn("assist-learn", names)
        self.assertIn("readable-metrics", names)
        self.assertIn("readable-rewrite", names)

    def test_catalog_keeps_latest_names_only_for_renamed_skills(self) -> None:
        catalog = json.loads(CATALOG.read_text())
        names = {entry["name"] for entry in catalog["skills"]}
        self.assertTrue(self.CANONICAL_NAMES.issubset(names))
        self.assertTrue(self.RENAMED_LEGACY_NAMES.isdisjoint(names))
        self.assertFalse((REPO_ROOT / "skills" / "frontend-design").exists())
        self.assertFalse((REPO_ROOT / "skills" / "eng-plan").exists())
        self.assertFalse((REPO_ROOT / "skills" / "eng-review").exists())
        self.assertFalse((REPO_ROOT / "skills" / "ui-design").exists())

    def test_verify_script_exists_and_repo_passes(self) -> None:
        self.assertTrue(VERIFY_SCRIPT.exists(), "scripts/verify_skills.py should exist")
        result = subprocess.run(
            ["python3", str(VERIFY_SCRIPT)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_verify_script_reports_broken_skill_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            skill_dir = repo / "skills" / "web-demo"
            skill_dir.mkdir(parents=True)
            (repo / "skills" / "catalog.json").write_text(
                json.dumps(
                    {
                        "skills": [
                            {
                                "name": "web-demo",
                                "path": "skills/web-demo",
                                "domain": "web",
                                "role": "canonical",
                            }
                        ]
                    }
                )
            )
            (skill_dir / "SKILL.md").write_text(
                "---\nname: web-demo\ndescription: 当测试时使用；demo\n---\nSee references/missing.md\n"
            )

            result = subprocess.run(
                ["python3", str(VERIFY_SCRIPT), str(repo)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("BROKEN REFERENCE", result.stderr)

    def test_verify_script_reports_unknown_future_canonical_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            skill_dir = repo / "skills" / "legacy-demo"
            skill_dir.mkdir(parents=True)
            (repo / "skills" / "catalog.json").write_text(
                json.dumps(
                    {
                        "skills": [
                            {
                                "name": "legacy-demo",
                                "path": "skills/legacy-demo",
                                "domain": "think",
                                "role": "legacy",
                                "migration": {
                                    "state": "planned",
                                    "canonical": "think-demo",
                                },
                            }
                        ]
                    }
                )
            )
            (skill_dir / "SKILL.md").write_text(
                "---\nname: legacy-demo\ndescription: 当测试时使用；demo\n---\n# demo\n"
            )

            result = subprocess.run(
                ["python3", str(VERIFY_SCRIPT), str(repo)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("UNKNOWN FUTURE CANONICAL", result.stderr)

    def test_verify_script_reports_description_trigger_prefix_violation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            skill_dir = repo / "skills" / "think-demo"
            skill_dir.mkdir(parents=True)
            (repo / "skills" / "catalog.json").write_text(
                json.dumps(
                    {
                        "skills": [
                            {
                                "name": "think-demo",
                                "path": "skills/think-demo",
                                "domain": "think",
                                "role": "canonical",
                            }
                        ]
                    }
                )
            )
            (skill_dir / "SKILL.md").write_text(
                "---\nname: think-demo\ndescription: 用户要求 demo 时使用\n---\n# demo\n"
            )

            result = subprocess.run(
                ["python3", str(VERIFY_SCRIPT), str(repo)],
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("DESCRIPTION TRIGGER PREFIX VIOLATION", result.stderr)

    def test_verify_script_accepts_trigger_exempt_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            skill_dir = repo / "skills" / "dev-demo"
            skill_dir.mkdir(parents=True)
            (repo / "skills" / "catalog.json").write_text(
                json.dumps(
                    {
                        "skills": [
                            {
                                "name": "dev-demo",
                                "path": "skills/dev-demo",
                                "domain": "dev",
                                "role": "canonical",
                                "trigger-exempt": True,
                            }
                        ]
                    }
                )
            )
            (skill_dir / "SKILL.md").write_text(
                "---\nname: dev-demo\ndescription: Run after a demo\n---\n# demo\n"
            )

            result = subprocess.run(
                ["python3", str(VERIFY_SCRIPT), str(repo)],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)

    def test_verify_script_accepts_brand_exception_without_trigger_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            skill_dir = repo / "skills" / "hive"
            skill_dir.mkdir(parents=True)
            (repo / "skills" / "catalog.json").write_text(
                json.dumps(
                    {
                        "skills": [
                            {
                                "name": "hive",
                                "path": "skills/hive",
                                "domain": "team",
                                "role": "brand-exception",
                            }
                        ]
                    }
                )
            )
            (skill_dir / "SKILL.md").write_text(
                "---\nname: hive\ndescription: Hive 基础 skill，无固定触发前缀\n---\n# hive\n"
            )

            result = subprocess.run(
                ["python3", str(VERIFY_SCRIPT), str(repo)],
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
