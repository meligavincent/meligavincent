import re
from scripts.models import Evidence


def detect(files: dict[str, str]) -> list[Evidence]:
    found: list[Evidence] = []
    for path, content in files.items():
        lower = content.lower()
        name = path.rsplit("/", 1)[-1]
        if name == "Dockerfile" or name.startswith("docker-compose"):
            found.append(Evidence("Docker", "Cloud Native & Platform", path))
        if path.endswith("Chart.yaml") or "/helm/" in path and "/templates/" in path:
            found.append(Evidence("Helm", "Cloud Native & Platform", path))
        if path.endswith(".tf"):
            found.append(Evidence("Terraform", "Cloud Native & Platform", path))
            for marker, tech in {"provider \"aws\"": "AWS", "provider \"azurerm\"": "Microsoft Azure", "provider \"google\"": "Google Cloud", "aws_eks": "Amazon EKS", "azurerm_kubernetes_cluster": "Azure AKS", "google_container_cluster": "Google Kubernetes Engine"}.items():
                if marker in lower:
                    found.append(Evidence(tech, "Cloud Native & Platform", path))
        if path.startswith(".github/workflows/"):
            found.append(Evidence("GitHub Actions", "Cloud Native & Platform", path))
        if name == ".gitlab-ci.yml":
            found.append(Evidence("GitLab CI", "Cloud Native & Platform", path))
        if path.endswith((".yaml", ".yml")) and re.search(r"(?m)^apiVersion:\s*.+\n(?:.+\n){0,8}?kind:\s*", content):
            found.append(Evidence("Kubernetes", "Cloud Native & Platform", path))
        if "argoproj.io" in lower or re.search(r"(?m)^kind:\s*(Application|ApplicationSet)\s*$", content):
            found.append(Evidence("Argo CD", "Cloud Native & Platform", path))
        for marker, tech in {"opentelemetry": "OpenTelemetry", "prometheus.io/": "Prometheus", "prometheus": "Prometheus", "grafana": "Grafana", "kind: scaledobject": "KEDA", "kind: externalsecret": "External Secrets"}.items():
            if marker in lower:
                found.append(Evidence(tech, "Cloud Native & Platform", path))
    return found
