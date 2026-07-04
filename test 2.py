import time
from rich import box
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.progress import track
from rich.rule import Rule
from rich.text import Text
from rich.live import Live
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

console = Console()
session = PromptSession("> ")

def make_layout(current_input: str):
    layout = Layout(name="root")
    layout.split_column(
        Layout(name="header", size=1),
        Layout(name="main", ratio=1),
        Layout(name="divider", size=1),
        Layout(name="prompt", size=3),
        Layout(name="footer", size=1),
    )

    layout["header"].update(Align.right(Text("Session: 0 AIC used", style="grey62")))

    content = "Welcome to the Rich Tutor!\n\nA simple tutorial for Rich"
    main_panel = Panel(
        Align.center(Text(content, justify="center")),
        title="Rich Test project",
        border_style="cyan",
        padding=(1, 4),
        box=box.ROUNDED,
        expand=False,
    )
    layout["main"].update(Align.center(main_panel, vertical="middle"))

    layout["divider"].update(Rule(style="grey30"))

    # Show the typed input inside the UI prompt area
    prompt_table = Text.assemble(("› ", "bold white"), (current_input or "", "white"))
    layout["prompt"].update(Panel(prompt_table, box=box.MINIMAL, padding=(0,1), style="on #0b0e12"))

    footer = Text.assemble(("/ commands · ? help · → next tab", "grey58"), (" " * 10, ""), ("Auto", "grey58"))
    layout["footer"].update(Panel(footer, box=box.MINIMAL, padding=(0,1), style="on #0b0e12"))
    return layout

# Optional loading animation before entering interactive mode
for _ in track(range(100), description="[yellow]Preparing the tutor..."):
    time.sleep(0.01)

console.clear()
# Use Live; avoid full-screen buffer inside VS Code terminal which shows raw escape codes
import os
use_screen = True
# VS Code's integrated terminal doesn't handle the alternate/full-screen buffer well
if os.environ.get("TERM_PROGRAM") in ("vscode", "vscode-insiders"):
    use_screen = False

with Live(make_layout(""), console=console, screen=use_screen, refresh_per_second=10) as live:
    # patch_stdout prevents prints from disturbing prompt_toolkit's prompt
    with patch_stdout():
        while True:
            try:
                # prompt appears at bottom and is managed by prompt_toolkit (no underlying PS prompt)
                text = session.prompt()
            except (EOFError, KeyboardInterrupt):
                break

            if not text.strip():
                # refresh to show empty input again
                live.update(make_layout(""))
                continue

            # update the UI prompt area to show the last command typed
            live.update(make_layout(text))

            if text.strip().lower() in ("exit", "quit"):
                break

            # Example: echo back below the panel (you can replace with app logic)
            console.print(f"[green]You typed:[/green] {text}")

console.clear()
print("Goodbye.")