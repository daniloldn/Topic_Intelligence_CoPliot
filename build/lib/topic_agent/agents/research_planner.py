from topic_agent.models import QueryUnderstanding, ResearchPlan





def create_research_plan(understanding: QueryUnderstanding) -> ResearchPlan:

    #going to make this an LLM call as well, should only apply for deep reseach, explain and latest developemts
    if understanding.request == "latest_developments":
        return ResearchPlan(
            source_types_needed=[
                "official announcements",
                "release notes",
                "technical blogs",
                "research papers",
                "independent commentary",
            ],
            search_queries=[
                f"{understanding.topic} latest developments",
                f"{understanding.topic} recent updates",
                f"{understanding.topic} release notes",
                f"{understanding.topic} technical analysis",
            ],
            expected_graph_nodes=[
                "Topic",
                "Development",
                "Source",
                "Organisation",
                "Tool",
                "Claim",
            ],
            expected_graph_edges=[
                "RELATED_TO",
                "EVIDENCED_BY",
                "RELEASED_BY",
                "UPDATES",
                "SUPPORTS",
                "CONTRADICTS",
            ],
        )