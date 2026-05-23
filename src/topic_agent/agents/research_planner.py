from topic_agent.models import QueryUnderstanding, ResearchPlan, RouterDecision
from topic_agent.llm.openai_client import OpenAIResearchPlanningClient





def create_research_plan(query, understanding: QueryUnderstanding, route:RouterDecision) -> ResearchPlan:
    client = OpenAIResearchPlanningClient()
    return client.plan_research(query, understanding, route)