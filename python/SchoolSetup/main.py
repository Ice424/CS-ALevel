import requests
import os
import shutil
from tqdm import tqdm
import json
import subprocess
PATH = "SchoolSetup"

GIT_PATH = os.path.abspath("~\\AppData\\Local\\Programs\\Git\\cmd\\git.exe")

CODE_PATH = os.path.abspath("~\\AppData\\Local\\Programs\\Microsoft VS Code\\code.exe")

def download(name, url):
    response = requests.get(url, stream=True)

    # Sizes in bytes.
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    with tqdm(total=total_size, unit="B", unit_scale=True) as progress_bar:
        with open(os.path.join(PATH, name), "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

    if total_size != 0 and progress_bar.n != total_size:
        raise RuntimeError("Could not download file")

try:
    os.makedirs(PATH)
except:
    pass

if not os.path.isfile(os.path.join(PATH, "git.exe")):
    download("git.exe", "https://github.com/git-for-windows/git/releases/download/v2.51.0.windows.1/Git-2.51.0-64-bit.exe")
    
if not os.path.isfile(os.path.join(PATH, "code.exe")):
    download("code.exe", "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user")

if not os.path.isfile(GIT_PATH):
    os.system(os.path.join(PATH, 'git.exe'), "/SILENT")

if not os.path.isfile(CODE_PATH):
    os.system(os.path.join(PATH, "code.exe"), "/VERYSILENT")

try:
    with open(os.path.join(PATH, "config.json"), "r") as f:
        config = json.loads(f.read())
except:
    username = input("Enter your github username: ")
    email = input("Enter your github email: ")
    repo = f"https://github.com/{username}/{username}.github.io.git"
    config = {
        "username": username,
        "email": email,
        "repo": repo
    }
    with open(os.path.join(PATH, "config.json"), "w") as f:
         f.write(json.dumps(config))

os.chdir(GIT_PATH.replace("git.exe", ""))

if not os.path.isdir(os.path.expanduser(f'~/Documents/{config["username"]}.github.io/.git')):
    print("cloning")
    os.system(f"""'{GIT_PATH}' clone {config["repo"]} """)
print("setting config")

os.system(f"git.exe config --global user.name {config['username']}")
os.system(f"git.exe config --global user.email {config['email']}")

os.chdir(CODE_PATH.replace("code.exe", ""))
os.system(f"""code.exe {os.path.expanduser(f"~/Documents/{config['username']}.github.io")}""")