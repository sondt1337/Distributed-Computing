import subprocess
import multiprocessing

def worker(i, j):
    # print(f"Running ./test for combination ({i+1}, {j+1})")
    subprocess.run(["./worker", str(i+1), str(j+1)])

if __name__ == "__main__":
    print("---------------------------------------------")
    print("Welcome to the distributed-computing Program!")
    print("---------------------------------------------")

    while True: 
        n = int(input("\n> col: "))
        m = int(input("> row: "))

        processes = [] # list of process

        for i in range(n):
            for j in range(m):
                p = multiprocessing.Process(target=worker, args=(i, j))
                processes.append(p)
                p.start()

        for p in processes:
            p.join()

        print("Program execution completed.")

        choice = input("Do you want to run the program again? (y/n): ")
        if choice.lower() != 'y':
            break  # end process