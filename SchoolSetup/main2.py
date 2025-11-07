import requests
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import Button, Digits, Footer, Header, ProgressBar, Checkbox, Input, Label
from textual.screen import Screen

def get_stuff(username: str):
    r = requests.get(f"https://api.github.com/users/{username}/repos")
    repos = r.json()
    
    for repo in repos:
        print(repo["name"])
    
    r = requests.get(f"https://api.github.com/repos/{username}/{repos[0]['name']}/commits")
    
    commits = r.json()
    email = commits[0]["commit"]["author"]["email"]
    return email, repos
    
class UsernameInput(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Enter your Github Username:")
        yield Input(placeholder="20edunn", id="user_input")
        yield Footer()
    def on_input_submitted(self, event: Input.Submitted) -> None:
        username = event.value.strip()
        self.app.push_screen(EmailCheck(username))


class EmailCheck(Screen):
    def __init__(self, username: str, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.username = username
        try:
            self.email, self.repos = get_stuff(self.username)
        except Exception:
            self.app.switch_screen(EmailInput())
        
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Welcome, {self.username}!")
       
        yield Label(f"is, {self.email} your email")
        yield HorizontalGroup(
            Button("Yes", variant="success", id="yesEmail"),
            Button("No", variant="error", id="noEmail")
        )
       
        yield Footer()
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yesEmail":
            pass
        elif event.button.id == "noEmail":
            self.app.push_screen(EmailInput())
            
class EmailInput(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Enter your Github Email:")
        yield Input(placeholder="20edunn@thelangton.org.uk", id="user_email")
        yield Footer()
    def on_input_submitted(self, event: Input.Submitted) -> None:
        username = event.value.strip()
        self.app.push_screen(EmailCheck(username))

class GitTime(Screen):
    
    

class SchoolSetup(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    def on_mount(self) -> None:
        self.push_screen(UsernameInput())
        
        
        


if __name__ == "__main__":
    app = SchoolSetup()
    app.run()