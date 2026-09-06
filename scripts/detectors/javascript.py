import json
from scripts.models import Evidence

PACKAGES = {"next": "Next.js", "react": "React", "typescript": "TypeScript", "tailwindcss": "Tailwind CSS", "gsap": "GSAP", "three": "Three.js", "@react-three/fiber": "React Three Fiber", "@react-three/drei": "React Three Drei", "zod": "Zod", "vitest": "Vitest", "playwright": "Playwright"}


def detect(files: dict[str, str]) -> list[Evidence]:
    found: list[Evidence] = []
    for path, content in files.items():
        if path.endswith("package.json"):
            try:
                manifest = json.loads(content)
            except json.JSONDecodeError:
                continue
            dependencies = {**manifest.get("dependencies", {}), **manifest.get("devDependencies", {})}
            found.extend(Evidence(tech, "Frontend", path) for package, tech in PACKAGES.items() if package in dependencies)
        elif path.endswith("pnpm-lock.yaml"):
            found.append(Evidence("pnpm", "Frontend", path))
        elif path.endswith(("bun.lock", "bun.lockb")):
            found.append(Evidence("Bun", "Frontend", path))
        elif path.endswith("package-lock.json"):
            found.append(Evidence("npm", "Frontend", path))
    return found
