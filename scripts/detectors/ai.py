import re
from scripts.models import Evidence


def detect(files: dict[str, str]) -> list[Evidence]:
    found: list[Evidence] = []
    for path, content in files.items():
        lower = content.lower()
        if "rag" in lower and re.search(r"(retrieval|retriever|vector|context).{0,80}rag|rag.{0,80}(retrieval|retriever|vector|context)", lower, re.S):
            found.append(Evidence("RAG", "AI Engineering", path))
        if "huggingface" in lower or "hugging face" in lower:
            found.append(Evidence("Hugging Face", "AI Engineering", path))
        if re.search(r"(tool[_ ]call|agentic|\bagent\b)", lower) and ("tools.py" in path or "/agent" in path or "agentic" in lower):
            found.append(Evidence("AI Agents", "AI Engineering", path))
        if re.search(r"\b(llm|large language model)\b", lower):
            found.append(Evidence("LLMs", "AI Engineering", path))
    return found
