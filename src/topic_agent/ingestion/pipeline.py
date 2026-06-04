from datetime import datetime, timezone
from pathlib import Path

from topic_agent.ingestion.fetcher import fetch_url
from topic_agent.ingestion.cleaner import clean_html
from topic_agent.ingestion.store import (
    stable_hash,
    make_source_id,
    make_episode_id,
)
from topic_agent.models import DiscoveryRun, SourceRecord, Episode, IngestionRun


def ingest_discovery_run(
    discovery_run: DiscoveryRun,
    max_items: int = 3,
    base_dir: Path = Path("data/graphs"),
) -> IngestionRun:
    graph_dir = base_dir / discovery_run.topic_slug
    raw_dir = graph_dir / "raw"
    cleaned_dir = graph_dir / "cleaned"
    episodes_dir = graph_dir / "episodes"

    raw_dir.mkdir(parents=True, exist_ok=True)
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    episodes_dir.mkdir(parents=True, exist_ok=True)

    ingestable_items = [
        item for item in discovery_run.discovery_result.items
        if item.recommendation == "ingest"
    ][:max_items]

    episodes: list[Episode] = []

    for evaluated_item in ingestable_items:
        candidate = evaluated_item.item

        source_id = make_source_id(candidate.url)

        try:
            raw_html = fetch_url(candidate.url)
            cleaned_text = clean_html(raw_html)
            content_hash = stable_hash(cleaned_text)

            episode_id = make_episode_id(source_id, content_hash)

            raw_path = raw_dir / f"{source_id}.html"
            cleaned_path = cleaned_dir / f"{source_id}.txt"
            episode_path = episodes_dir / f"{episode_id}.json"

            raw_path.write_text(raw_html, encoding="utf-8")
            cleaned_path.write_text(cleaned_text, encoding="utf-8")

            episode = Episode(
                episode_id=episode_id,
                source_id=source_id,
                title=candidate.title,
                url=candidate.url,
                ingested_at=datetime.now(timezone.utc),
                published_at=candidate.published_at,
                raw_path=str(raw_path),
                cleaned_path=str(cleaned_path),
                content_hash=content_hash,
                status="success",
                failure_reason=None,
            )

            episode_path.write_text(
                episode.model_dump_json(indent=2),
                encoding="utf-8",
            )

        except Exception as exc:
            episode = Episode(
                episode_id=f"failed_{source_id}",
                source_id=source_id,
                title=candidate.title,
                url=candidate.url,
                ingested_at=datetime.now(timezone.utc),
                published_at=candidate.published_at,
                raw_path="",
                cleaned_path="",
                content_hash="",
                status="failed",
                failure_reason=str(exc),
            )

        episodes.append(episode)

    return IngestionRun(
        run_id=f"ingest_{discovery_run.run_id}",
        discovery_run_id=discovery_run.run_id,
        topic_slug=discovery_run.topic_slug,
        created_at=datetime.now(timezone.utc),
        sources_attempted=len(ingestable_items),
        sources_succeeded=sum(1 for ep in episodes if ep.status == "success"),
        episodes=episodes,
    )