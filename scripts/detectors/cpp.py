from scripts.models import Evidence


def detect(files: dict[str, str]) -> list[Evidence]:
    found: list[Evidence] = []
    for path, content in files.items():
        lower = content.lower()
        if path.endswith("CMakeLists.txt"):
            found.append(Evidence("CMake", "Backend & Systems", path))
        if path.endswith(("conanfile.py", "conanfile.txt")):
            found.append(Evidence("Conan", "Backend & Systems", path))
        for marker, technology in {"grpc": "gRPC", "protobuf": "Protobuf", "onnxruntime": "ONNX Runtime", "opencv": "OpenCV", "boost": "Boost", "ninja": "Ninja"}.items():
            if marker in lower:
                found.append(Evidence(technology, "Backend & Systems", path))
    return found
