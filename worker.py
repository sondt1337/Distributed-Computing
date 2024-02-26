import json
import sys
import numpy as np

i = int(sys.argv[1])
F_json = sys.argv[2]
F = np.array(json.loads(F_json))

G_json = sys.argv[3]
G = np.array(json.loads(G_json))

print(F)
print(G)

# print("Hello World! " + str(i))