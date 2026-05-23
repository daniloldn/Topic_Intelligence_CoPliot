import typer
from rich.console import Console
from topic_agent.workflow.planning_workflow import run_planning_workflow
from dotenv import load_dotenv

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
def plan(query:str):
    results = run_planning_workflow(query)
    console.print(results.model_dump_json(indent=2))



