import tempfile
import unittest
from pathlib import Path

from scripts.generate_tech_stack import END, START, update_readme


class ReadmeUpdateTests(unittest.TestCase):
    def test_preserves_content_outside_markers(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text("# Existing\n\nBefore\n\n" + START + "\nold\n" + END + "\n\nAfter\n")
            update_readme(readme, START + "\nnew\n" + END)
            self.assertEqual(readme.read_text(), "# Existing\n\nBefore\n\n" + START + "\nnew\n" + END + "\n\nAfter\n")

    def test_adds_markers_when_absent(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text("# Existing\n")
            update_readme(readme, START + "\nnew\n" + END)
            self.assertIn(START, readme.read_text())
