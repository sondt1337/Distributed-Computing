import json
import sys
import numpy as np
import subprocess
import random

# receive worker sequence number, F (json) & G (json)
i = int(sys.argv[1])
F_json = sys.argv[2]
F = np.array(json.loads(F_json))

err = random.randint(1, 6) # random rate of workers

G_json = sys.argv[3]
G = np.array(json.loads(G_json))
M_json = sys.argv[4]
m_json = sys.argv[5]

# create error rate 
if (err == 1):
    F+=F
def write_to_file(file, content):
    with open(file, 'a') as f:
        f.write(content + '\n')
        
FmulG = np.dot(F, G) # F mul G
FmulG_json = json.dumps(FmulG.tolist()) # convert value -> json 
write_to_file("result.txt", f"{FmulG}")

# send F mul G to server (from each worker)
def server(FmulG_json, i): 
    subprocess.run(["python", "server_docker.py", "check", str(i), FmulG_json, M_json, m_json])
    
if __name__ == "__main__":
    server(FmulG_json, i)