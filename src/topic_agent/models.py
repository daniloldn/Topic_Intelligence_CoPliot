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

from typing import Literal
from pydantic import BaseModel, Field


class TrustedSource(BaseModel):
    name: str
    domain: str
    search_scope: str
    source_type: str
    topics: list[str]
    trust_level: Literal["trusted", "candidate", "unknown", "avoid"] = "trusted"
    feed_url : str | None = None


class CandidateContentItem(BaseModel):
    title: str
    url: str
    source_name: str | None = None
    domain: str | None = None
    source_type: str | None = None
    published_at: str | None = None
    snippet: str | None = None
    discovery_query: str
    discovery_method: Literal["trusted_source_search", "broad_web_search"]
    


class EvaluatedContentItem(BaseModel):
    item: CandidateContentItem
    relevance_score: int = Field(ge=0, le=100)
    authority_score: int = Field(ge=0, le=100)
    recency_score: int = Field(ge=0, le=100)
    evidence_value_score: int = Field(ge=0, le=100)
    technical_depth_score: int = Field(ge=0, le=100)
    bias_risk_score: int = Field(ge=0, le=100)
    overall_score: int = Field(ge=0, le=100)
    recommendation: Literal["ingest", "maybe", "skip"]
    reason: str =  Field(
        description= "Why you chose the particular source for the question the user wants"
    )
    source_role: Literal[
    "primary_announcement",
    "implementation_release",
    "academic_evidence",
    "benchmark",
    "independent_analysis",
    "business_context",
    "documentation"
]
    date_relevance: Literal[
    "current",
    "recent",
    "historical",
    "unknown",
]


class DiscoveryResult(BaseModel):
    query: str
    items: list[EvaluatedContentItem] = Field(
        description="Exactly 5 evaluated candidate sources, ranked from best to worst."
    )
