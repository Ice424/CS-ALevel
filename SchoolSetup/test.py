from textual.app import App, ComposeResult
from textual.widgets import ProgressBar, Static
from textual.containers import Vertical
import requests
import os
import asyncio

PATH = "."  # Change to your path

class DownloadApp(App):
    CSS = """
    ProgressBar {
        height: 3;
    }
    """

    def __init__(self, name: str, url: str):
        super().__init__()
        self.file_name = name
        self.url = url

    def compose(self) -> ComposeResult:
        with Vertical():
            self.label = Static(f"Preparing to download {self.file_name}...")
            self.progress = ProgressBar(total=100)
            yield self.label
            yield self.progress

    async def on_mount(self) -> None:
        # Run download in background so UI can render
        asyncio.create_task(self.download_file(self.file_name, self.url))

    async def download_file(self, name, url):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._download_blocking, name, url)

    def _download_blocking(self, name, url):
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        downloaded = 0

        with open(os.path.join(PATH, name), "wb") as file:
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded += len(data)
                if total_size > 0:
                    percent = int(downloaded / total_size * 100)
                    # Update the progress bar safely in the main thread
                    self.call_from_thread(self.progress.update, percent)
                    self.call_from_thread(
                        self.label.update, f"Downloading {name}: {percent}%"
                    )

        # Final update
        self.call_from_thread(self.label.update, f"{name} downloaded!")
        self.call_from_thread(self.progress.update, 100)

if __name__ == "__main__":
    DownloadApp("code.exe", "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user").run()
