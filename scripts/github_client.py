"""Read-only GitHub API client. It never enumerates account repositories."""

from __future__ import annotations

from io import BytesIO
import json
import os
from zipfile import ZipFile
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class MissingRepository(Exception):
    pass


class GitHubClient:
    def __init__(self, token: str | None = None) -> None:
        self.token = token or os.environ.get("GITHUB_TOKEN")

    def _get(self, url: str) -> object:
        headers = self._headers()
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=30) as response:  # nosec B310: fixed GitHub API URLs
                return json.load(response)
        except HTTPError as error:
            if error.code == 404:
                raise MissingRepository(url) from error
            raise

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _bytes(self, url: str) -> bytes:
        request = Request(url, headers=self._headers())
        try:
            with urlopen(request, timeout=30) as response:  # nosec B310: fixed GitHub API URLs
                return response.read()
        except HTTPError as error:
            if error.code == 404:
                raise MissingRepository(url) from error
            raise

    def languages(self, repo: str) -> dict[str, int]:
        return self._get(f"https://api.github.com/repos/{repo}/languages")  # type: ignore[return-value]

    def files(self, repo: str) -> dict[str, str]:
        metadata = self._get(f"https://api.github.com/repos/{repo}")
        branch = metadata["default_branch"]  # type: ignore[index]
        files: dict[str, str] = {}
        archive = self._bytes(f"https://api.github.com/repos/{repo}/zipball/{branch}")
        with ZipFile(BytesIO(archive)) as zip_file:
            for entry in zip_file.infolist():
                path = entry.filename.split("/", 1)[-1] if "/" in entry.filename else ""
                if entry.is_dir() or not _is_relevant(path):
                    continue
                files[path] = zip_file.read(entry).decode("utf-8", errors="replace")
        return files


def _is_relevant(path: str) -> bool:
    ignored = ("node_modules/", ".next/", "dist/", "build/", "target/", "vendor/", ".venv/", "venv/", "coverage/", "generated/", ".cache/")
    if path.startswith(ignored):
        return False
    name = path.rsplit("/", 1)[-1]
    exact = {"README.md", "package.json", "pnpm-lock.yaml", "bun.lock", "bun.lockb", "package-lock.json", "pyproject.toml", "uv.lock", "Cargo.toml", "CMakeLists.txt", "conanfile.py", "conanfile.txt", "vcpkg.json", "Dockerfile", "docker-compose.yml", "docker-compose.yaml", "Chart.yaml", ".gitlab-ci.yml"}
    if name in exact or name.startswith("requirements") or path.endswith(".tf"):
        return True
    configuration_roots = (".github/workflows/", "infrastructure/", "argocd/", "observability/", "deploy/", "k8s/")
    if path.startswith(configuration_roots) and path.endswith((".yaml", ".yml", ".json", ".toml")):
        return True
    # Strong agent evidence is intentionally narrow; source code is never executed.
    return path.endswith(("/tools.py", "/agent.py", "/agents.py")) or "/agent/" in path
