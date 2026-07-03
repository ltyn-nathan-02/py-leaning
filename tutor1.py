import time
from rich import print
from rich.panel import Panel
from rich.align import Align as ag
from rich.progress import track

for i in track(range(200), description="[yellow]Preparing the tutor..."):
    time.sleep(0.01)  # Simulates loading assets

# 2. Display the auto-rescaling content block right after loading finishes
content = "Welcome to the Rich Tutor!\n \n A simple tutorial for Rich"

styled_panel = Panel(
    content, 
    title="Rich Test project", 
    expand=False, 
    border_style="cyan",
    padding=(1, 4)
)

# Print the centered panel using your 'ag' shortcut
print(ag.center(styled_panel))
