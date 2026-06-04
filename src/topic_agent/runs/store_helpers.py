import re
from pathlib import Path
from datetime import datetime, timezone
from topic_agent.models import PlanningResult, DiscoveryResult, DiscoveryRun


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")[:60]


def create_run_id(topic_slug: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    return f"{timestamp}_{topic_slug}"


def build_discovery_run(
    query: str,
    planning_result: PlanningResult,
    discovery_result: DiscoveryResult,
) -> DiscoveryRun:
    topic_slug = slugify(planning_result.query_understanding.topic)

    return DiscoveryRun(
        run_id=create_run_id(topic_slug),
        query=query,
        topic_slug=topic_slug,
        created_at=datetime.now(timezone.utc),
        planning_result=planning_result,
        discovery_result=discovery_result,
    )


def save_discovery_run(run: DiscoveryRun, base_dir: Path = Path("data/runs")) -> Path:
    run_dir = base_dir / run.run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    path = run_dir / "discovery.json"
    path.write_text(run.model_dump_json(indent=2), encoding="utf-8")

    return path