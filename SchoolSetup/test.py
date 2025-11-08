import requests
import os

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Static, ProgressBar
from textual.screen import Screen
from textual.worker import Worker, get_current_worker

class AnotherScreen(Screen):
    def __init__(self, main, name: str | None = None, id: str | None = None, classes: str | None = None) -> None:
        super().__init__(name, id, classes)
        self.main = main
        
    def compose(self) -> ComposeResult:
        yield Static("1 Download Done")
        with VerticalScroll(id="weather-container"):
            yield ProgressBar(id="Bar1")
            yield ProgressBar(id="Bar2")

class DownloadApp(App):
    def compose(self) -> ComposeResult:
        self.downloads_complete = 0
        yield Button()
        with VerticalScroll(id="weather-container"):
            yield ProgressBar(id="Bar1")
            yield ProgressBar(id="Bar2")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        
        


if __name__ == "__main__":
    app = DownloadApp()
    app.run()