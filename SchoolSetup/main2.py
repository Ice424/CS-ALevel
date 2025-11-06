import requests
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Button, Digits, Footer, Header, ProgressBar, Checkbox, Input

def get_stuff():
    r = requests.get("https://api.github.com/users/ice424/repos")
    repos = r.json()
    
    for repo in repos:
        print(repo["name"])
    
    r = requests.get(f"https://api.github.com/repos/Ice424/{repos[0]['name']}/commits")
    
    commits = r.json()
    email = commits[0]["commit"]["author"]["email"]
    


class ghinput(Input):
    def __init__(self):
        self


class SchoolSetup(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield ghinput()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    def on_input_submitted(value):
        


if __name__ == "__main__":
    app = SchoolSetup()
    app.run()