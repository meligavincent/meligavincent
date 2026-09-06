import re
from scripts.models import Evidence

PACKAGES = {"fastapi": ("FastAPI", "Backend & Systems"), "pydantic": ("Pydantic", "Backend & Systems"), "torch": ("PyTorch", "AI Engineering"), "tensorflow": ("TensorFlow", "AI Engineering"), "transformers": ("Transformers", "AI Engineering"), "langchain": ("LangChain", "AI Engineering"), "langgraph": ("LangGraph", "AI Engineering"), "llama-index": ("LlamaIndex", "AI Engineering"), "mlflow": ("MLflow", "AI Engineering"), "opentelemetry": ("OpenTelemetry", "Cloud Native & Platform"), "sqlalchemy": ("SQLAlchemy", "Backend & Systems"), "alembic": ("Alembic", "Backend & Systems"), "celery": ("Celery", "Backend & Systems"), "ray": ("Ray", "AI Engineering"), "polars": ("Polars", "Data & Messaging"), "numpy": ("NumPy", "Data & Messaging"), "pandas": ("Pandas", "Data & Messaging"), "scikit-learn": ("scikit-learn", "AI Engineering")}


def detect(files: dict[str, str]) -> list[Evidence]:
    found: list[Evidence] = []
    for path, content in files.items():
        if not (path.endswith("pyproject.toml") or "/requirements" in path or path.startswith("requirements")):
            continue
        lower = content.lower()
        for package, (tech, category) in PACKAGES.items():
            if re.search(rf"(?<![\w-]){re.escape(package)}(?=[\s=<>\[\]~\"'])", lower):
                found.append(Evidence(tech, category, path))
        if path.endswith("pyproject.toml") and "[tool.uv]" in lower:
            found.append(Evidence("uv", "Backend & Systems", path))
    if any(path.endswith("uv.lock") for path in files):
        found.append(Evidence("uv", "Backend & Systems", "uv.lock"))
    return found
