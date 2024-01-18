import subprocess

print("---------------------------------------------")
print("Welcome to the distributed-computing Program!")
print("---------------------------------------------")

n = int(input("\n> col: "))
m = int(input("> row: "))

for i in range(n):
    for j in range(m):
        print(f"Running ./test for combination ({i+1}, {j+1})")
        
        # call ./test --> running many process as workers 
        subprocess.run(["./test", str(i+1), str(j+1)])

print("Program execution completed.")
