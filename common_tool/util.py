import subprocess
import shlex

def run(cmd, *args, **kwargs):
    return subprocess.run(shlex.split(cmd), *args, **kwargs)