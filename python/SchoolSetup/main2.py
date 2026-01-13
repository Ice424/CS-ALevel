import requests
from threading import Semaphore
import os

from textual import work
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup, VerticalScroll
from textual.widgets import Button, Footer, Header, ProgressBar, Checkbox, Input, Label, LoadingIndicator
from textual.screen import Screen
from textual.worker import Worker, get_current_worker

PATH = "SchoolSetup"

GIT_PATH = os.path.abspath("~\\AppData\\Local\\Programs\\Git\\cmd\\git.exe")

CODE_PATH = os.path.abspath("~\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe")

global download_count
download_count = 0

def fetch_latest_release(url, identifier) -> str:
        r = requests.get(url)
        for asset in r.json()["assets"]:
            if identifier in asset["browser_download_url"]:
                return asset["browser_download_url"]
        return url
    
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
        self.app.username = username
        try:
            self.app.email, self.repos = get_stuff(self.app.username)
        except Exception:
            self.app.push_screen(EmailInput())
        
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(f"Welcome, {self.app.username}!")
       
        yield Label(f"is, {self.app.email} your email")
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
            if self.app.git_worker.is_finished and self.app.code_worker.is_finished:
                self.app.push_screen(GitTime())
            else:
                self.app.push_screen(WaitTime())
        elif event.button.id == "noEmail":
            self.app.switch_screen(EmailInput())
            
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
        email = event.value.strip()
        self.app.email = email
        if self.app.git_worker.is_finished and self.app.code_worker.is_finished:
            self.app.push_screen(GitTime())
        else:
            self.app.push_screen(WaitTime())

class WaitTime(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Waiting for git & VsCode")
        bar1 = ProgressBar(id="Bar1")
        bar1.update(total=1, progress=1)
        bar2 = ProgressBar(id="Bar2")
        bar2.update(total=1, progress=1)
        bar3 = ProgressBar(id="Bar3")
        
        yield bar1
        yield bar2  

        yield LoadingIndicator()
        
        
        yield Footer()
        
        self.wait_for_download()
        
    @work(exclusive=False)
    async def wait_for_download(self):
        await self.app.workers.wait_for_complete([self.app.code_worker, self.app.git_worker])
        self.app.switch_screen(GitTime())
class GitTime(Screen):
    def compose(self) -> ComposeResult:
        bar1 = ProgressBar(id="Bar1")
        bar1.update(total=1, progress=1)
        bar2 = ProgressBar(id="Bar2")
        bar2.update(total=1, progress=1)
        bar3 = ProgressBar(id="Bar3")
        
        yield bar1
        yield bar2  
        yield bar3

class OtherApps(Screen):
    
    def compose(self) -> ComposeResult:
        r = requests.get("https://raw.githubusercontent.com/Ice424/CS-ALevel/refs/heads/main/SchoolSetup/otherProgams.json")
        self.data = r.json()
        yield Header()
        yield Label("What Other apps would you like")
        with VerticalScroll(id="CheckScroll"):
            for program in self.data.keys():
                yield Checkbox(program)
        
        yield Button("Continue", variant="success", id="OtherAppsContinue")
        
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
        if event.button.id == "OtherAppsContinue":
            
            scroll = self.query_one("#CheckScroll", VerticalScroll)
            checkboxes = scroll.query(Checkbox).results()
            app = self.app
            for cb in checkboxes:
                if cb.value:
                    url = self.data[cb.label]["url"]
                    if self.data[cb.label]["GH"]:
                        url = fetch_latest_release(url, self.data[cb.label]["exe_identifier"])
                    self.app.Download(str(cb.label) + ".exe",url, self.app)
                    print(cb.value, cb.label)
            self.app.push_screen(UsernameInput())

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
        self.download_semaphore = Semaphore(3)
        self.downloaded_items = 0
        self.download_count = 0
        self.username = ""
        self.email = ""
        if not os.path.isfile(CODE_PATH):
             self.code_worker = self.Download("code.exe", "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user", self.app)
        if not os.path.isfile(GIT_PATH):
            url = fetch_latest_release("https://api.github.com/repos/git-for-windows/git/releases/latest", ".exe")
            self.git_worker = self.Download("git.exe", url, self.app)
        self.push_screen(OtherApps())
        
    
    @work(exclusive=False, thread=True, )
    def Download(self, name:str, url:str, app:App) -> None:
        with self.download_semaphore: 
            PATH = "SchoolSetup"
            self.download_count += 1
            progress_bar_name = "#Bar" +  str(((self.download_count - 1) % 3) + 1)
            progress_bar = app.query_one(progress_bar_name, ProgressBar)
            worker = get_current_worker()
            response = requests.get(url, stream=True)

            if not os.path.isfile(os.path.join(PATH, name)):
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
            os.system("taskkill /IM code /F")
            app.call_from_thread(progress_bar.update, total=1, progress=1)
        
    def download_done(self):
        self.downloaded_items += 1
        
        
        


if __name__ == "__main__":
    app = SchoolSetup()
    app.run()