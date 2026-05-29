from topic_agent.models import PlanningResult, DiscoveryResult
from topic_agent.llm.openai_client import OpenAISourceFinderClient


def find_source(planning_result: PlanningResult) -> DiscoveryResult:
    client = OpenAISourceFinderClient()
    return client.find_sources(planning_result)