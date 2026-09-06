import re
from scripts.models import Evidence

PACKAGES = {"axum": "Axum", "tokio": "Tokio", "tonic": "Tonic", "serde": "Serde", "sqlx": "SQLx", "tracing": "Tracing", "rdkafka": "rdkafka", "async-nats": "NATS"}


def detect(files: dict[str, str]) -> list[Evidence]:
    return [Evidence(tech, "Backend & Systems", path) for path, content in files.items() if path.endswith("Cargo.toml") for package, tech in PACKAGES.items() if re.search(rf"(?m)^\s*{re.escape(package)}\s*=", content)]
