from pathlib import Path

from topic_agent.models import DiscoveryRun


def load_discovery_run(path: Path) -> DiscoveryRun:
    return DiscoveryRun.model_validate_json(
        path.read_text(encoding="utf-8")
    )