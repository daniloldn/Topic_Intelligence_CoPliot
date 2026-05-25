from topic_agent.models import PlanningResult
from topic_agent.sources.source_registry import TRUSTED_SOURCES


def build_discovery_queries(result: PlanningResult) -> tuple[list[str], list[str]]:
    topic = result.query_understanding.topic

    plan_queries = []
    if result.research_plan:
        plan_queries = result.research_plan.search_queries[:3]

    trusted_queries = []

    for source in TRUSTED_SOURCES:
        if any(t.lower() in topic.lower() or topic.lower() in t.lower() for t in source.topics):
            trusted_queries.append(f"{source.search_scope} {topic}")

        for q in plan_queries[:2]:
            trusted_queries.append(f"{source.search_scope} {q}")

    broad_queries = plan_queries or [
        f"{topic} latest developments",
        f"{topic} recent updates",
        f"{topic} technical analysis",
    ]

    return trusted_queries[:8], broad_queries[:5]