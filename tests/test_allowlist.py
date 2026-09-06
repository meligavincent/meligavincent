import tempfile
import unittest
from pathlib import Path

from scripts.generate_tech_stack import load_projects


class AllowlistTests(unittest.TestCase):
    def test_only_explicit_projects_are_loaded(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.yaml"
            path.write_text("projects:\n  - repo: owner/approved\n    name: Approved\n    domain: Test\n    inspiration: Test\n    status: active\n    enabled: true\n")
            projects = load_projects(path)
        self.assertEqual([project.repo for project in projects], ["owner/approved"])
        self.assertTrue(projects[0].enabled)
