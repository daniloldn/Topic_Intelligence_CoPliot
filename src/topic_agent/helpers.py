from topic_agent.models import PlanningResult
from rich.console import Console

def print_plan_summary(result: PlanningResult, console:Console):
    console.print("[bold]Research Plan Summary[/bold]")
    console.print(f"Topic: {result.query_understanding.topic}")
    console.print(f"Request: {result.query_understanding.request}")
    console.print(f"Route: {result.router_decision.route}")

    if result.research_plan:
        console.print("\n[bold]Source types:[/bold]")
        for source_type in result.research_plan.source_types_needed:
            console.print(f"- {source_type}")

        console.print("\n[bold]Top search queries:[/bold]")
        for query in result.research_plan.search_queries[:5]:
            console.print(f"- {query}")