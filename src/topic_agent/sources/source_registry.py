from topic_agent.models import TrustedSource

TRUSTED_SOURCES = [
    TrustedSource(
        name="OpenAI News",
        domain="openai.com",
        search_scope="site:openai.com/news",
        source_type="official_ai_lab",
        topics=["AI agents", "LLMs", "tool use", "OpenAI"],
    ),
    TrustedSource(
        name="Anthropic News",
        domain="anthropic.com",
        search_scope="site:anthropic.com/news",
        source_type="official_ai_lab",
        topics=["AI agents", "Claude", "tool use", "computer use"],
    ),
    TrustedSource(
        name="LangChain Blog",
        domain="blog.langchain.com",
        search_scope="site:blog.langchain.com",
        source_type="framework_blog",
        topics=["AI agents", "LangGraph", "agent frameworks", "orchestration"],
    ),
    TrustedSource(
        name="LlamaIndex Blog",
        domain="llamaindex.ai",
        search_scope="site:llamaindex.ai/blog",
        source_type="framework_blog",
        topics=["AI agents", "RAG", "agent frameworks", "LlamaIndex"],
    ),
    TrustedSource(
        name="arXiv",
        domain="arxiv.org",
        search_scope="site:arxiv.org",
        source_type="academic_research",
        topics=["AI agents", "LLMs", "multi-agent systems", "evaluation"],
    ),
]