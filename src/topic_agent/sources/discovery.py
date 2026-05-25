from topic_agent.models import CandidateContentItem, PlanningResult
from topic_agent.sources.query_builder import build_discovery_queries
from topic_agent.sources.search_provider import MockSearchProvider



def deduplicate_by_url(items: list[CandidateContentItem]) -> list[CandidateContentItem]:
    seen = set()
    deduped = []

    for item in items:
        if item.url in seen:
            continue
        seen.add(item.url)
        deduped.append(item)

    return deduped

def discover_content_items(
    planning_result: PlanningResult,
    search_provider: MockSearchProvider,
    max_results_per_query: int = 3,
) -> list[CandidateContentItem]:
    trusted_queries, broad_queries = build_discovery_queries(planning_result)

    candidates: list[CandidateContentItem] = []

    for query in trusted_queries:
        results = search_provider.search(query, max_results=max_results_per_query)
        candidates.extend(results)

    # Broad search is fallback/backfill.
    # For MVP, run it always but limit it.
    for query in broad_queries[:2]:
        results = search_provider.search(query, max_results=max_results_per_query)
        candidates.extend(results)

    return deduplicate_by_url(candidates)


