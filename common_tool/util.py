import subprocess
import shlex

def run(cmd, *args, **kwargs):
    subprocess.run(shlex.split(cmd), *args, **kwargs)