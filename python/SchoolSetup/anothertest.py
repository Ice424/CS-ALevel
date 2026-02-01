import requests

r = requests.get("https://api.github.com/repos/git-for-windows/git/releases/latest")
print(r.json()["assets"][0]["browser_download_url"])