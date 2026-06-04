import typer
import time
from rich.console import Console
from rich.prompt import Confirm
from topic_agent.workflow.planning_workflow import run_planning_workflow
from dotenv import load_dotenv
from topic_agent.helpers import print_plan_summary, print_discovery_summary
from topic_agent.sources.search_provider import MockSearchProvider
from topic_agent.sources.evaluator import evaluate_content_items
from topic_agent.sources.discovery import discover_content_items
from topic_agent.agents.source_provider import find_source
from topic_agent.runs.store_helpers import build_discovery_run, save_discovery_run

load_dotenv()


app = typer.Typer()
console = Console()

@app.command()
def hello(name:str= typer.Argument("World")):
    console.print(f"Hello, [bold green]{name}[/bold green]!")


# a command to create a new knowledge graph 
@app.command()
def create(topic:str):
    console.print(f"Starting to create a knowledge history for {topic}")

# a command to update an exisitng knoledge graph 
@app.command()
def update(topic:str):
    console.print(f"Updating the {topic} knowledge history")

# a command for view all the knowledge histories that are in the database
@app.command()
def view():
    console.print("Here are all the knoweledge histories available so far")

# a command to plan what research is required from the user prompt
@app.command()
def plan(query: str, full: bool = False):
    """Create a research plan for a topic."""
    start = time.perf_counter()
    with console.status("[bold green]Planning research workflow...[/bold green]", spinner="dots"):
        result = run_planning_workflow(query)

    elapsed = time.perf_counter() - start

    console.print(f"[dim]Completed in {elapsed:.2f}s[/dim]")

    if full:
        console.print(result.model_dump_json(indent=2))
    else:
        print_plan_summary(result, console)

    

@app.command()
def discover(query: str, full: bool = False):
    """Discover and evaluate candidate content items for a query."""
    start = time.perf_counter()
    with console.status("[bold green]Planning and discovering sources...[/bold green]", spinner="dots"):
        planning_result = run_planning_workflow(query)

        if planning_result.query_understanding.clarification_needed:
            console.print("[yellow]Clarification needed:[/yellow]")
            console.print(planning_result.query_understanding.clarification_question)
            return
    with console.status("[bold green]Finding 5 sources from the web...[/bold green]", spinner="dots"):
        source_result = find_source(planning_result)
        evaluated =  source_result.items

        #when using a search provider keepign for now, until final flow is decided 
        #search_provider = MockSearchProvider()
        #candidates = discover_content_items(planning_result, search_provider)
        #evaluated = evaluate_content_items(candidates, planning_result)
    
    elapsed = time.perf_counter() - start
    console.print(f"[dim]Completed in {elapsed:.2f}s[/dim]")

    if full:
        console.print([item.model_dump() for item in evaluated])
    else:
        print_discovery_summary(evaluated, console)

    should_save = Confirm.ask(
        "\n[bold]Save this discovery run?[/bold]",
        default=False,
    )

    if should_save:
        discovery_run = build_discovery_run(
            query=query,
            planning_result=planning_result,
            discovery_result=source_result,
        )

        saved_path = save_discovery_run(discovery_run)

        console.print(f"\n[green]Saved discovery run:[/green] {saved_path}")
        console.print(f"[dim]Next:[/dim] uv run fde ingest {saved_path}")
    else:
        console.print("[dim]Discovery run not saved.[/dim]")



