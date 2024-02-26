import json
import sys
import numpy as np
import subprocess

i = int(sys.argv[1])
F_json = sys.argv[2]
F = np.array(json.loads(F_json))

G_json = sys.argv[3]
G = np.array(json.loads(G_json))

FmulG = np.dot(F, G)
FmulG_json = json.dumps(FmulG.tolist())

def server(FmulG_json, i):
    subprocess.run(["python", "server.py", "check", str(i), FmulG_json])
    
if __name__ == "__main__":
    server(FmulG_json, i)
