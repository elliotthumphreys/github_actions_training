import requests
import json
from github import Github, Repository
import os, shutil, fileinput, sys
import subprocess

g = Github(os.environ['GITHUB_TOKEN'])

def create_repo_on_github(repo_name):
    g.get_organization(os.environ['GITHUB_ORG_NAME']).create_repo(
            name= repo_name,
            description= "Repository generated for GitHub Actions COP",
            private= False,
            has_issues= True,
            has_projects= True,
            has_wiki= True,
            team_id=3952270
        )

def create_repo_from_template(repo_name):
    def copytree(src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def replace_files(src, original, replace):
        files = [
            src + "/" + original + ".sln",
            src + "/" + original + ".csproj",
            src + "/Something.cs",
            src + "/push_repo_files.sh"]

        for filename in files:
            with fileinput.FileInput(filename, inplace=True) as file:
                for line in file:
                    print(line.replace(original, replace), end='')

        for filename in files:
            os.rename(filename, filename.replace(original, replace))

    os.mkdir("./" + repo_name)

    copytree("./template", "./" + repo_name)

    replace_files("./" + repo_name, "template", repo_name)

def push_files(location):
    rc = os.system("sh " + location + "push_repo_files.sh")

# add attendess of the github actions cop here
repos_to_make = []
for new_repo_name in repos_to_make:
    create_repo_on_github(new_repo_name)
    create_repo_from_template(new_repo_name)
    push_files("./" + new_repo_name + "/")