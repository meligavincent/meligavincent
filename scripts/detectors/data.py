from scripts.models import Evidence

MARKERS = {"postgres": "PostgreSQL", "pgvector": "pgvector", "redis": "Redis", "redpanda": "Redpanda", "kafka": "Kafka", "nats jetstream": "NATS JetStream", "nats": "NATS", "rabbitmq": "RabbitMQ", "clickhouse": "ClickHouse", "timescaledb": "TimescaleDB", "mongodb": "MongoDB", "minio": "S3-compatible storage"}


def detect(files: dict[str, str]) -> list[Evidence]:
    found: list[Evidence] = []
    for path, content in files.items():
        lower = content.lower()
        for marker, technology in MARKERS.items():
            if marker in lower:
                found.append(Evidence(technology, "Data & Messaging", path))
    return found
