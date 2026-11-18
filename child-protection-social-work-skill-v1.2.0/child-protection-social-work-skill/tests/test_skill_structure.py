import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    return (ROOT / name).read_text(encoding="utf-8")


class SkillStructureTests(unittest.TestCase):
    def test_required_files(self):
        for name in ("README.md", "CHANGELOG.md", "SECURITY.md", "SKILL.md",
                     ".gitignore", ".github/workflows/validate.yml",
                     "examples/fictional-case.md", "templates/output-templates.md",
                     "references/family-function-assessment.md",
                     "references/sdm-assessment-guide.md", "references/source-registry.md"):
            with self.subTest(name=name):
                self.assertTrue((ROOT / name).is_file())

    def test_frontmatter(self):
        header = read("SKILL.md").split("---\n")
        self.assertEqual(header[0], "")
        self.assertIn("name: child-protection-social-work\n", header[1])
        self.assertIn("description:", header[1])

    def test_items(self):
        body = read("references/family-function-assessment.md")
        for prefix, count in (("F", 13), ("C", 12)):
            actual = re.findall(rf"^\| ({prefix}\d{{2}}) \|", body, re.MULTILINE)
            self.assertEqual(actual, [f"{prefix}{i:02d}" for i in range(1, count + 1)])

    def test_modes(self):
        for mode in ("標準版", "速寫版", "督導版", "教學版"):
            self.assertIn(mode, read("SKILL.md"))
            self.assertIn(mode, read("templates/output-templates.md"))

    def test_sdm(self):
        for tool in ("SDM-S", "SDM-R", "SDM-RR"):
            self.assertIn("## " + tool + " ", read("references/sdm-assessment-guide.md"))

    def test_private_paths(self):
        for path in ("private-sources/", "case-data/"):
            self.assertIn(path, read(".gitignore").splitlines())
