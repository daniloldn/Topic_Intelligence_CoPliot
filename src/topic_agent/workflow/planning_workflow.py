from topic_agent.agents.knowledge_router import route_query
from topic_agent.agents.query_understanding import understand_query
from topic_agent.agents.research_planner import create_research_plan
from topic_agent.models import PlanningResult


# this is not gonna be a LLM for the MVP, it is going ot be a deterministic workflow
def run_planning_workflow(query: str) -> PlanningResult:
    understanding = understand_query(query)

    if understanding.clarification_needed:
        #add a while loop to ask for clarification
        # then rerun understanding
        # for now just returning clarifcatoin questions for mvp
        return PlanningResult(
            original_query=query,
            query_understanding=understanding,
            router_decision=None,
            research_plan=None,
        )

    router_decision = route_query(understanding)

    if router_decision.route in ["build_new_graph", "update_existing_graph"]:
        research_plan = create_research_plan(
            query,
            understanding,
            router_decision,
        )
    else:
        research_plan = None

    return PlanningResult(
        original_query=query,
        query_understanding=understanding,
        router_decision=router_decision,
        research_plan=research_plan,
    )