import git
from git import Repo # pip3 install GitPython
import random
import string
import shutil
import sys

pat = "CHANGEME" # https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
git_username = "CHANGEME" # Example: https://github.com/github = github
git_repo = "temp" # Create a private repository in Github
folder = "./temp" # Location to store repository, start with a "." for the current folder
commit_msg = "Your message here"

# Create Random String
random = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Delete folder if exists already
shutil.rmtree(folder, ignore_errors=True)

# Clone Repository
try:
    repo = Repo.init(folder)
    repo.create_remote('origin', url=f'https://{pat}:x-oauth-basic@github.com/{git_username}/{git_repo}')
    repo.remotes.origin.fetch()
    repo = git.Repo(folder)
    origin = repo.remote("origin")
    assert origin.exists()
    origin.fetch()
    print(f"Cloned repository {git_repo}")
except:
    print(f"Failed to clone repository {git_repo}")
    sys.exit(1)

# Pull Repository
try:
    repo = git.Repo(folder)
    g = git.Git('temp')
    g.pull('origin', 'main')
    print("Pulled repository successfully")
except:
    print("Failed to pull repository")
    sys.exit(1)

# Create file in repository
try:
    with open(f'{folder}/{random}.txt', 'w') as f:
        f.write('Nothing special in here')
    print("Created file in repository")
except:
    print("Failed to create file")
    sys.exit(1)

# Commit file to Github
try:
    repo.index.add([f"{random}.txt"])
    repo.index.commit(commit_msg)
    repo.git.push("--set-upstream", origin, repo.head.ref)
    print("Pushed successfully to Github")
except:
    print("Failed to push to Github")
    sys.exit(1)

# Remove Local Repository
shutil.rmtree(folder, ignore_errors=True)