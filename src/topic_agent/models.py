from pydantic import BaseModel
from typing import Literal


class QueryUnderstanding(BaseModel):
    topic: str
    request: Literal[
        "explain_topic", 
        "latest_developments",
        "compare", 
        "deep_reseach", 
        "unknown"
    ]
    time_frame: str |None = None
    knowledge_freshness_required: Literal["low", "medium", "high"]
    depth_required: Literal["quick", "standard", "deep"]


class RouterDecision(BaseModel):
    route: Literal[
        "answer_from_exisitng_graph", 
        "update_exisitng_graph", 
        "build_new_grpah", 
        "ask_clarifying_quesitons"
    ]
    reason: str

class ResearchPlan(BaseModel):
    source_types_needed: list[str]
    search_queries: list[str]
    expected_graph_nodes: list[str]
    expected_graph_edges: list[str]

class PlanningResult(BaseModel):
    original_query: str
    query_understanding: QueryUnderstanding
    router_decision: RouterDecision
    research_plan: ResearchPlan | None = None
