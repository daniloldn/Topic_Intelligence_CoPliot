from pydantic import BaseModel, Field
from typing import Literal


class QueryUnderstanding(BaseModel):
    topic: str = Field(description="The main topic the user is asking about.")
    request: Literal[
        "explain_topic", 
        "latest_developments",
        "compare", 
        "deep_reseach", 
        "unknown"
    ]
    time_frame: str |None =Field(
        default=None,
        description="The relevant time period, e.g. 'last 7 days', 'last 30 days'.",
    )
    knowledge_freshness_required: Literal["low", "medium", "high"]
    depth_required: Literal["quick", "standard", "deep"]
    user_goal: str = Field(
        description="A short explanation of what the user wants to achieve."
    )
    clarification_needed: bool
    clarification_question: str | None = Field(
        description= "Only use if the topic feels vague, then ask quesitions to clarifiy what the user wants, asking them to be more specific. "
    )


class RouterDecision(BaseModel):
    route: Literal[
        "answer_from_exisitng_graph", 
        "update_exisitng_graph", 
        "build_new_graph", 
        "ask_clarifying_quesitons"
    ]
    reason: str

class SourcePriority(BaseModel):
    source_type: str
    priority: int = Field(description="Priority from 1 to 5, where 5 is highest.")
    reason: str


class ResearchPlan(BaseModel):
    source_types_needed: list[str]
    source_priority: list[SourcePriority]
    search_queries: list[str]
    evidence_requirements: list[str]
    expected_graph_nodes: list[str]
    expected_graph_edges: list[str]
    ranking_signals: list[str]
    risks_and_biases: list[str]
    #removed clarificatoin, might add it back later

class PlanningResult(BaseModel):
    original_query: str
    query_understanding: QueryUnderstanding
    router_decision: RouterDecision | None = None
    research_plan: ResearchPlan | None = None
