import os
from openai import OpenAI
from topic_agent.models import QueryUnderstanding, ResearchPlan


class OpenAIQueryUnderstandingClient:
    def __init__(self, model: str | None = None):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model or os.getenv("QUERY_MODEL", "gpt-5-mini")

    def understand_query(self, query: str) -> QueryUnderstanding:
        system_prompt = """
You are the query understanding component of an agentic topic intelligence system.

Your job is to convert a user's natural language request into structured metadata.

Classify:
- topic
- request
- relevant time window
- knowledge freshness requirement
- depth required
- user's goal

Request meanings:
- explain_topic: user wants a stable explanation
- latest_developments: user wants recent updates/news/developments
- compare: user wants comparison between topics/tools/ideas
- deep_research: user wants a thorough research plan or investigation
- unknown: unclear request

Knoweledge Freshness:
- low: stable knowledge is enough
- medium: recent-ish knowledge may help
- high: must search recent sources

Depth:
- quick: short answer
- standard: useful but not exhaustive
- deep: detailed research-style answer
"""

        response = self.client.responses.parse(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            text_format=QueryUnderstanding,
        )

        return response.output_parsed
    

class OpenAIResearchPlanningClient:
    def __init__(self, model:str|None=None):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model or os.getenv("RESEARCH_PLAN_MODEL", "gpt-5-mini")

    def build_research_planner_user_prompt(
            self,
    original_query: str,
    query_understanding_json: str,
    router_decision_json: str,
    ) -> str:
        return f"""
    Create a research plan for the following user query.

    Original user query:
        {original_query}

    Query understanding:
    {query_understanding_json}

    Router decision:
    {router_decision_json}

    Return a structured research plan that the source discovery and knowledge graph agents can use.
    """

    def plan_research(self, query, understanding_json, route_decision: str) -> ResearchPlan:
        system_prompt = """
You are the Research Planning Agent for an agentic topic intelligence system.

Your job is to create a clear, structured research plan from a user's query understanding.

You do NOT browse the web.
You do NOT invent specific facts.
You do NOT claim that developments happened.
You only decide how the system should research the topic.

The system you are part of builds and updates topic knowledge graphs. It uses your plan to:
1. discover sources,
2. evaluate sources,
3. ingest content,
4. extract claims/developments/concepts,
5. update a knowledge graph,
6. produce a grounded briefing.

You must think like a careful research analyst and source strategist.

Given:
- the original user query,
- the interpreted topic,
- the user's request,
- the required knowledge freshness,
- the time window,
- the desired depth,

produce a research plan that specifies:

1. source_types_needed
   The categories of sources that should be searched.
   Examples:
   - official company/lab announcements
   - academic papers
   - developer documentation
   - framework release notes
   - technical blogs
   - independent expert commentary
   - mainstream news
   - regulatory/government sources
   - YouTube/transcript sources
   - GitHub repositories
   - benchmark/evaluation reports

2. source_priority
   Which source types should be prioritised first and why.

3. search_queries
   Concrete search queries the source discovery agent can use.

4. evidence_requirements
   What kind of evidence is needed to answer the user well.
   Examples:
   - primary sources for factual claims
   - independent commentary for significance
   - release notes for implementation changes
   - papers for research claims
   - benchmarks for performance claims
   - government pages for legal/regulatory claims

5. expected_graph_nodes
   The types of knowledge graph nodes likely to be extracted.
   Examples:
   - Topic
   - Concept
   - Claim
   - Development
   - Source
   - Organisation
   - Tool
   - Paper
   - Person
   - Event
   - Date
   - Benchmark
   - Regulation

6. expected_graph_edges
   The types of relationships likely to be extracted.
   Examples:
   - RELATED_TO
   - EVIDENCED_BY
   - RELEASED_BY
   - AUTHORED_BY
   - UPDATES
   - REPLACES
   - BUILDS_ON
   - SUPPORTS
   - CONTRADICTS
   - COMPARES_WITH
   - MEASURED_BY
   - AFFECTS

7. ranking_signals
   The criteria downstream agents should use to rank source/content importance.
   Examples:
   - recency
   - source authority
   - primary-source status
   - cross-source confirmation
   - technical depth
   - practical impact
   - novelty
   - relevance to user intent

8. risks_and_biases
   What the system should be careful about.
   Examples:
   - hype-heavy sources
   - outdated information
   - vendor bias
   - duplicate reporting
   - weak evidence
   - speculative claims
   - missing primary sources

Rules:
- Be specific to the topic.
- Do not produce generic research advice.
- Do not include URLs unless they are obvious source categories, not claimed findings.
- Do not say "latest" facts unless they are provided in the input.
- If the topic is fast-moving, prioritise fresh and primary sources.
- If the topic is legal, medical, tax, financial, or regulatory, prioritise official and expert sources.
- If the topic is technical, prioritise docs, release notes, papers, benchmarks, and engineering blogs.
- If the user asks for "latest developments", use a high-freshness plan.
- If the user asks for an explanation, use a stable-knowledge plan.
- If the user asks for comparison, include comparison-focused queries and graph edges.
- Your output must be valid structured data matching the required schema.
"""

        response = self.client.responses.parse(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": self.build_research_planner_user_prompt(query, understanding_json, route_decision)},
            ],
            text_format=ResearchPlan,
        )

        return response.output_parsed
    
        