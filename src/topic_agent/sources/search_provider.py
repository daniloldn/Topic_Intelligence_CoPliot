from typing import Protocol
from topic_agent.models import CandidateContentItem

#after make real api calls/ use llm websearch to do it 
class MockSearchProvider:
    def search(self, query: str, max_results: int = 5) -> list[CandidateContentItem]:
        discovery_method = (
            "trusted_source_search" if "site:" in query else "broad_web_search"
        )

        return [
            CandidateContentItem(
                title="OpenAI announces updates to agent tooling",
                url="https://openai.com/news/example-agent-update",
                source_name="OpenAI News",
                domain="openai.com",
                source_type="official_ai_lab",
                published_at="2026-05-20",
                snippet="OpenAI shares recent updates related to AI agents, tool use, and developer workflows.",
                discovery_query=query,
                discovery_method=discovery_method,
            ),
            CandidateContentItem(
                title="LangGraph release notes for agent workflows",
                url="https://blog.langchain.com/example-langgraph-release",
                source_name="LangChain Blog",
                domain="blog.langchain.com",
                source_type="framework_blog",
                published_at="2026-05-18",
                snippet="LangChain describes updates to LangGraph for building reliable AI agent workflows.",
                discovery_query=query,
                discovery_method=discovery_method,
            ),
        ][:max_results]
    