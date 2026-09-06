"""Small shared models and normalization for the footprint generator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


NORMALIZED = {
    "k8s": "Kubernetes", "kubernetes": "Kubernetes", "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL", "reactjs": "React", "next": "Next.js",
    "huggingface": "Hugging Face", "otel": "OpenTelemetry", "cpp": "C++",
}


def normalize(name: str) -> str:
    return NORMALIZED.get(name.lower(), name)


@dataclass(frozen=True)
class Evidence:
    technology: str
    category: str
    path: str


@dataclass
class Project:
    repo: str
    name: str
    domain: str
    inspiration: str
    status: str
    enabled: bool


@dataclass
class Footprint:
    evidence: dict[str, dict[str, list[str]]] = field(default_factory=dict)

    def add(self, repository: str, items: Iterable[Evidence]) -> None:
        for item in items:
            technology = normalize(item.technology)
            key = f"{item.category}:{technology}"
            repos = self.evidence.setdefault(key, {})
            repos.setdefault(repository, [])
            if item.path not in repos[repository]:
                repos[repository].append(item.path)

    def technologies(self, category: str) -> list[str]:
        return sorted(key.split(":", 1)[1] for key in self.evidence if key.startswith(f"{category}:"))

    def as_json(self) -> dict[str, dict[str, object]]:
        result: dict[str, dict[str, object]] = {}
        for key, repositories in sorted(self.evidence.items()):
            _, technology = key.split(":", 1)
            entry = result.setdefault(technology, {"categories": [], "repositories": [], "evidence": []})
            entry["categories"].append(key.split(":", 1)[0])
            for repo, paths in repositories.items():
                if repo not in entry["repositories"]:
                    entry["repositories"].append(repo)
                entry["evidence"].extend({"repository": repo, "path": path} for path in paths)
        return result
