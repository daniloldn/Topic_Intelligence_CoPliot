import typer
import time
from rich.console import Console
from topic_agent.workflow.planning_workflow import run_planning_workflow
from dotenv import load_dotenv
from topic_agent.helpers import print_plan_summary

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
  



