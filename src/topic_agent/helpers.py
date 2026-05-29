from topic_agent.models import PlanningResult, EvaluatedContentItem
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

def print_discovery_summary(items: list[EvaluatedContentItem], console: Console):
    console.print("[bold]Recommended items to ingest[/bold]")

    recommended = [x for x in items if x.recommendation == "ingest"]

    if not recommended:
        console.print("[yellow]No strong ingestion candidates found.[/yellow]")
        return

    for i, evaluated in enumerate(recommended[:10], start=1):
        item = evaluated.item
        console.print(f"\n[bold]{i}. {item.title}[/bold]")
        console.print(f"URL: {item.url}")
        console.print(f"Source: {item.source_name or item.domain}")
        console.print(f"Published: {item.published_at or 'Unknown'}")
        console.print(f"Score: {evaluated.overall_score}/100")
        console.print(f"Recommendation: {evaluated.recommendation}")
        console.print(f"Role:{evaluated.source_role}")
        console.print(f"Reason: {evaluated.reason}")