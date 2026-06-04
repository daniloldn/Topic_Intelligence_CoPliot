import hashlib
import re
from pathlib import Path


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def make_source_id(url: str) -> str:
    return f"source_{stable_hash(url)}"


def make_episode_id(source_id: str, content_hash: str) -> str:
    return f"episode_{stable_hash(source_id + content_hash)}"


def safe_filename(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")[:80]