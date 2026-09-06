"""Generate an evidence-backed README section from the explicit project allowlist."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
import sys
from concurrent.futures import ThreadPoolExecutor

# Keep `python scripts/generate_tech_stack.py` usable in CI without packaging it.
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.github_client import GitHubClient, MissingRepository
from scripts.models import Footprint, Project
from scripts.detectors import ai, cloud_native, cpp, data, javascript, languages, python, rust

ROOT = Path(__file__).resolve().parents[1]
START, END = "<!-- TECH-FOOTPRINT:START -->", "<!-- TECH-FOOTPRINT:END -->"
CATEGORIES = ["Languages", "AI Engineering", "Backend & Systems", "Frontend", "Cloud Native & Platform", "Data & Messaging"]


def load_projects(path: Path) -> list[Project]:
    """Parse the deliberately small, reviewed YAML subset without a YAML dependency."""
    projects: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if line.startswith("- "):
            if current:
                projects.append(current)
            current = {}
            line = line[2:]
        if current is not None and ":" in line:
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip().strip('"\'')
    if current:
        projects.append(current)
    return [Project(**{**item, "enabled": item.get("enabled", "false").lower() == "true"}) for item in projects]  # type: ignore[arg-type]


def render(footprint: Footprint, projects: list[Project], existing: set[str]) -> str:
    lines = [START, "## Technology Footprint", "", "> Automatically generated from selected production-oriented portfolio repositories.", ""]
    for category in CATEGORIES:
        technologies = footprint.technologies(category)
        if technologies:
            lines.extend([f"### {category}", "`" + "` · `".join(technologies) + "`", ""])
    lines.extend(["### Portfolio Coverage", "", "| Project | Domain | Status |", "| --- | --- | --- |"])
    for project in projects:
        status = "Active" if project.repo in existing and project.status.lower() == "active" else project.status.title()
        lines.append(f"| {project.name} | {project.domain} | {status} |")
    lines.extend(["", END])
    return "\n".join(lines)


def update_readme(readme: Path, section: str) -> bool:
    original = readme.read_text()
    pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.S)
    updated = pattern.sub(section, original) if pattern.search(original) else original.rstrip() + "\n\n" + section + "\n"
    if updated == original:
        return False
    readme.write_text(updated)
    return True


def main(root: Path = ROOT, client: GitHubClient | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    client = client or GitHubClient()
    projects = load_projects(root / "profile-projects.yaml")
    footprint, existing = Footprint(), set()
    def scan(project: Project) -> tuple[Project, dict[str, int], dict[str, str]] | None:
        try:
            repo_languages = client.languages(project.repo)
            files = client.files(project.repo)
        except MissingRepository:
            logging.warning("Allowlisted repository does not exist; skipping: %s", project.repo)
            return None
        return project, repo_languages, files

    # The allowlist is small and each repository is independent; parallel reads keep the daily job quick.
    with ThreadPoolExecutor(max_workers=5) as executor:
        scans = list(executor.map(scan, projects))
    for result in scans:
        if result is None:
            continue
        project, repo_languages, files = result
        existing.add(project.repo)
        if not (project.enabled and project.status.lower() == "active"):
            continue
        footprint.add(project.repo, languages.detect(repo_languages))
        for detector in (javascript, python, rust, cpp, cloud_native, data, ai):
            footprint.add(project.repo, detector.detect(files))
    generated = root / "generated"
    generated.mkdir(exist_ok=True)
    (generated / "technology-evidence.json").write_text(json.dumps(footprint.as_json(), indent=2, sort_keys=True) + "\n")
    changed = update_readme(root / "README.md", render(footprint, projects, existing))
    logging.info("Technology footprint %s", "updated" if changed else "already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
