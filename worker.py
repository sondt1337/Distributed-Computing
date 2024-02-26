import json
import sys
import numpy as np
import subprocess

i = int(sys.argv[1])
F_json = sys.argv[2]
F = np.array(json.loads(F_json))

G_json = sys.argv[3]
G = np.array(json.loads(G_json))

print(F)
print(G)

FmulG = np.dot(F, G)
FmulG_json = json.dumps(FmulG.tolist())

def server(FmulG_json):
    subprocess.run(["python", "worker.py", FmulG_json])