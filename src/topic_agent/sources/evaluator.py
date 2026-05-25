from topic_agent.models import CandidateContentItem, EvaluatedContentItem, PlanningResult


TRUSTED_DOMAIN_SCORES = {
    "openai.com": 95,
    "anthropic.com": 95,
    "blog.langchain.com": 85,
    "llamaindex.ai": 80,
    "arxiv.org": 85,
    "github.com": 75,
}


def evaluate_content_items(
    items: list[CandidateContentItem],
    planning_result: PlanningResult,
) -> list[EvaluatedContentItem]:
    evaluated = [
        evaluate_content_item(item, planning_result)
        for item in items
    ]

    return sorted(evaluated, key=lambda x: x.overall_score, reverse=True)


def evaluate_content_item(
    item: CandidateContentItem,
    planning_result: PlanningResult,
) -> EvaluatedContentItem:
    topic = planning_result.query_understanding.topic.lower()
    title = item.title.lower()
    snippet = (item.snippet or "").lower()
    domain = item.domain or ""

    relevance_score = 80 if topic in title or topic in snippet else 50
    authority_score = TRUSTED_DOMAIN_SCORES.get(domain, 50)

    recency_score = 70 if item.published_at else 50

    technical_depth_score = 75 if item.source_type in [
        "framework_blog",
        "academic_research",
        "developer_docs",
        "release_notes",
    ] else 50

    evidence_value_score = 80 if item.discovery_method == "trusted_source_search" else 60

    bias_risk_score = 40 if item.source_type == "official_ai_lab" else 25

    overall_score = round(
        0.30 * relevance_score
        + 0.25 * authority_score
        + 0.15 * recency_score
        + 0.15 * evidence_value_score
        + 0.15 * technical_depth_score
        - 0.05 * bias_risk_score
    )

    if overall_score >= 50:
        recommendation = "ingest"
    elif overall_score >= 35:
        recommendation = "maybe"
    else:
        recommendation = "skip"

    return EvaluatedContentItem(
        item=item,
        relevance_score=relevance_score,
        authority_score=authority_score,
        recency_score=recency_score,
        evidence_value_score=evidence_value_score,
        technical_depth_score=technical_depth_score,
        bias_risk_score=bias_risk_score,
        overall_score=overall_score,
        recommendation=recommendation,
        reason=(
            f"Scored based on relevance to '{planning_result.query_understanding.topic}', "
            f"domain authority, evidence value, and technical depth."
        ),
    )