import requests


def fetch_latest_release(url) -> str:
    r = requests.get(url)
    for asset in r.json()["assets"]:
        if ".exe" in asset["browser_download_url"]:
            return asset["browser_download_url"]
    return url


url = fetch_latest_release(
    "https://api.github.com/repos/git-for-windows/git/releases/latest"
)

print(f"\n{url}")