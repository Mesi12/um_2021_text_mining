# %%
import sys
import os
import subprocess

# https://stackoverflow.com/questions/22081209/find-the-root-of-the-git-repository-where-the-file-lives#comment44778829_22081487
repo_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
sys.path.insert(1, os.path.join(sys.path[0], repo_dir))
from helper.HolmesReader import HolmesReader

# %%
holmesReader = HolmesReader()
story = holmesReader.get_story("a_case_of_identity")
print(story['title'])


# %%
