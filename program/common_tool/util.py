import subprocess
import shlex

def run(cmd, *args, **kwargs):
    return subprocess.run(shlex.split(cmd), *args, **kwargs)

class Jsonable:
    def to_json(self):
        j = vars(self).copy()
        return j