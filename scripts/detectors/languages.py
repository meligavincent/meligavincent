from scripts.models import Evidence

LANGUAGES = {"Python", "TypeScript", "JavaScript", "Rust", "C++", "C", "Shell", "SQL", "HTML", "CSS"}


def detect(languages: dict[str, int]) -> list[Evidence]:
    return [Evidence(language, "Languages", "GitHub languages API") for language in languages if language in LANGUAGES]
