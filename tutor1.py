import click
import art
import rich

def libLoad():
    rich.print("[green]Rich is now loaded[/green]")
    art.tprint("Art Lib is loaded")
    click.echo("Click is also loaded successfully", fg = "#90EE90")



if  __name__ == "__main__":
    libLoad()
