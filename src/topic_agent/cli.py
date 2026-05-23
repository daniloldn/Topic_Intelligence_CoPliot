import typer
from rich.console import Console


app = typer.Typer()
console = Console()

@app.command()
def hello(name:str= typer.Argument("World")):
    console.print(f"Hello, [bold green]{name}[/bold green]!")


# a command to create a new knowledge graph 
@app.command()
def create(topic:str):
    console.print(f"Starting to create a knowledge history for {topic}")



