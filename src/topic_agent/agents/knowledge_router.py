from src.topic_agent.models import RouterDecision, QueryUnderstanding

def route_query(understanding: QueryUnderstanding)-> RouterDecision:

    # need to add a way to check the existing graphs 
    #need to make a decision if there ia already enough knowledege to answer everthing
    #also need to see if the query fits cleanly into one of the exisitng grpah, if there is ambiguity we need ask clarifying questions 
    
    #for now there is no graphs 

    graph_exists = False

    #if no graph exists, need to build a new one 
    if not graph_exists:
        return RouterDecision(
            route="build_new_graph", 
            reason="No graphs exists yet so we need to build a new one"
        )
    
    #if a graph exists but we need the latest information we need to update
    if understanding.knowledge_freshness_required == "high":
        #need to check when the graph was last updated
        #make judgement to see if we need to update the graph
        #need to add if statemetn to either update or answer from exisitng knowledge 
        return RouterDecision(
            route="update_exisitng_graph",
            reason="Exisitng graph might be stale for the current quesiton"
        )
    
    return RouterDecision(
        route="answer_from_existing_graph",
        reason="Existing graph is sufficient.",
    )


    
    