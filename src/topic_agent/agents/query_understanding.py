from src.topic_agent.models import QueryUnderstanding

#made it rule based for now but will come back to change it to call an LLM API
def understand_query(query:str) -> QueryUnderstanding:
    lowered = query.lower()

    if "latest" in lowered or "recent" in lowered or "developments" in lowered:
        intent = "latest_developments"
        freshness = "high"
        time_window = "last 7 days"
    else:
        intent = "explain_topic"
        freshness = "low"
        time_window = None

    return QueryUnderstanding(
        topic=query,
        intent=intent,
        time_window=time_window,
        freshness_required=freshness,
        depth="standard",
    )