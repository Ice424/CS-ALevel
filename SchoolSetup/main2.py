import requests
import os

from textual import work
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, Digits, Footer, Header, ProgressBar, Checkbox, Input, Label
from textual.screen import Screen
from textual.worker import Worker, get_current_worker

PATH = "SchoolSetup"

GIT_PATH = os.path.abspath("~\\AppData\\Local\\Programs\\Git\\cmd\\git.exe")

CODE_PATH = os.path.abspath("~\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe")

global download_count
download_count = 0

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
        
        bar1 = ProgressBar(id="Bar1")
        bar1.update(total=1, progress=1)
        bar2 = ProgressBar(id="Bar2")
        bar2.update(total=1, progress=1)
        bar3 = ProgressBar(id="Bar3")
        
        yield bar1
        yield bar2  
        yield bar3
        yield Footer()
    def on_input_submitted(self, event: Input.Submitted) -> None:
        username = event.value.strip()
        self.app.push_screen(EmailCheck(username))

class EmailCheck(Screen):
    def __init__(self, username: str, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.username = username
        self.email = ""
        try:
            self.email, self.repos = get_stuff(self.username)
        except Exception:
            self.app.push_screen(EmailInput())
        
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Welcome, {self.username}!")
       
        yield Label(f"is, {self.email} your email")
        yield HorizontalGroup(
            Button("Yes", variant="success", id="yesEmail"),
            Button("No", variant="error", id="noEmail")
        )
        
        bar1 = ProgressBar(id="Bar1")
        bar1.update(total=1, progress=1)
        bar2 = ProgressBar(id="Bar2")
        bar2.update(total=1, progress=1)
        bar3 = ProgressBar(id="Bar3")
        
        yield bar1
        yield bar2  
        yield bar3
       
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
        
        bar1 = ProgressBar(id="Bar1")
        bar1.update(total=1, progress=1)
        bar2 = ProgressBar(id="Bar2")
        bar2.update(total=1, progress=1)
        bar3 = ProgressBar(id="Bar3")
        
        yield bar1
        yield bar2  
        yield bar3
        yield Footer()
    def on_input_submitted(self, event: Input.Submitted) -> None:
        username = event.value.strip()
        self.app.push_screen(EmailCheck(username))

class GitTime(Screen):
    pass

class OtherApps(Screen):
    def __init__(self, app:App, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.app = app
    
    def compose(self) -> ComposeResult:
        r = requests.get("url")
        yield Header()
        yield Label("What Other apps would you like")
        scroll = VerticalScroll()
        
        VerticalScroll(
            for 
        )
        
        bar1 = ProgressBar(id="Bar1")
        bar1.update(total=1, progress=1)
        bar2 = ProgressBar(id="Bar2")
        bar2.update(total=1, progress=1)
        bar3 = ProgressBar(id="Bar3")
        
        yield bar1
        yield bar2  
        yield bar3
        yield Footer()
        

class SchoolSetup(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    def compose(self) -> ComposeResult:
        bar1 = ProgressBar(id="Bar1")
        bar1.update(total=1, progress=1)
        bar2 = ProgressBar(id="Bar2")
        bar2.update(total=1, progress=1)
        bar3 = ProgressBar(id="Bar3")
        
        yield bar1
        yield bar2  
        yield bar3
    def on_mount(self) -> None:
        self.downloaded_items =0
        if not os.path.isfile(CODE_PATH):
             self.code_worker = self.Download("code.exe", "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user", self.app)
        if not os.path.isfile(GIT_PATH):
            url = self.fetch_latest_release("https://api.github.com/repos/git-for-windows/git/releases/latest")
            self.git_worker = self.Download("git.exe", url, self.app)
        self.push_screen(OtherApps(self))
        

    def fetch_latest_release(self, url) -> str:
        r = requests.get(url)
        for asset in r.json()["assets"]:
            if ".exe" in asset["browser_download_url"]:
                return asset["browser_download_url"]
        return url
    
    @work(exclusive=False, thread=True)
    def Download(self, name:str, url:str, app:App) -> None:
        PATH = "SchoolSetup"
        global download_count
        download_count += 1
        progress_bar_name = "#Bar" + str(download_count%3)
        progress_bar = app.query_one(progress_bar_name, ProgressBar)
        worker = get_current_worker()
        response = requests.get(url, stream=True)

        # Sizes in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        progress = 0
        app.call_from_thread(progress_bar.update, total=total_size)
        
        with open(os.path.join(PATH, name), "wb") as file:
            for data in response.iter_content(block_size):
                screen = app.screen
                progress = progress+len(data)
                if worker.is_cancelled:
                    return
                progress_bar = screen.query_one(progress_bar_name, ProgressBar)
                app.call_from_thread(progress_bar.update, total=total_size, progress=progress)
                file.write(data)
        self.call_from_thread(self.download_done)
        screen = app.screen
        progress_bar = screen.query_one(progress_bar_name, ProgressBar)
        app.call_from_thread(progress_bar.update, total=None)
        os.system(os.path.join(PATH, name)+ " /VERYSILENT")
        app.call_from_thread(progress_bar.update, total=1, progress=1)
        
    def download_done(self):
        self.downloaded_items += 1
        
        
        


if __name__ == "__main__":
    app = SchoolSetup()
    app.run()