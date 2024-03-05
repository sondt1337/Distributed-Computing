# python server.py create
import subprocess
import multiprocessing
import numpy as np
import math
import random
import json
import sys 
import time

# COMPUTE time --> total.txt    
def write_total(correct_count, start_time):
    with open("total.txt", "w") as file:
        file.write(f"number of correct: {correct_count}\n")
        file.write(f"number of incorrect: {incorrect_count}\n")
        file.write(f"elapsed time: {time.time() - start_time} seconds\n")
        
# SEND worker sequence number, F (json) & G (json)       
def worker(i, F_json, G_json):
    subprocess.run(["python", "worker.py", str(i), F_json, G_json])

# WRITE file function
def write_to_file(file, content):
    with open(file, 'a') as f:
        f.write(content + '\n')
        
# COUNT number of worker (correct) --> total.txt            
def get_number_of_correct():
    with open("total.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if "number of correct:" in line:
                return int(line.split(":")[1].strip())
            
# COUNT number of worker (incorrect) --> total.txt      
def get_number_of_incorrect():
    with open("total.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if "number of incorrect:" in line:
                return int(line.split(":")[1].strip())

# CREATE random matrix (X, Y)
def create_matrix(rows, cols):
    matrix = np.random.randint(100, size=(rows, cols))
    return matrix

# DIVIDE sub matrix 1 
def print_sub_matrices_1(matrix, submatrix_rows, submatrix_cols):
    num_rows, num_cols = matrix.shape
    sub_matrices = {}
    for i in range(0, num_rows, submatrix_rows):
        for j in range(0, num_cols, submatrix_cols):
            sub_matrix = matrix[i : i + submatrix_rows, j : j + submatrix_cols]
            sub_matrix_name = f"A_{i//submatrix_rows +1}_{j//submatrix_cols+ 1}"
            sub_matrices[sub_matrix_name] = sub_matrix
    return sub_matrices

# DIVIDE sub matrix 2
def print_sub_matrices_2(matrix, submatrix_rows, submatrix_cols):
    num_rows, num_cols = matrix.shape
    sub_matrices = {}
    for i in range(0, num_rows, submatrix_rows):
        for j in range(0, num_cols, submatrix_cols):
            sub_matrix = matrix[i : i + submatrix_rows, j : j + submatrix_cols]
            sub_matrix_name = f"B_{i//submatrix_rows +1}_{j//submatrix_cols+ 1}"
            sub_matrices[sub_matrix_name] = sub_matrix
    return sub_matrices

# GEN additional matrix 1 (row)
def create_additional_matrices_1(submatrix_rows, submatrix_cols, n, delta_pc):
    additional_matrices = {}
    for i in range(1, delta_pc + 1):
        for j in range(1, n + 1):
            sub_matrix = create_matrix(submatrix_rows, submatrix_cols)
            sub_matrix_name = f"R_{i}_{j}"
            additional_matrices[sub_matrix_name] = sub_matrix
    return additional_matrices

# GEN additional matrix 2 (col)
def create_additional_matrices_2(submatrix_rows, submatrix_cols, n, delta_pc):
    additional_matrices = {}
    for i in range(n, 0, -1):
        for j in range(1, delta_pc + 1):
            sub_matrix = create_matrix(submatrix_rows, submatrix_cols)
            sub_matrix_name = f"R'_{i}_{j}"
            additional_matrices[sub_matrix_name] = sub_matrix
    return additional_matrices

# COMPUTE F(z)
def calc_F(sub_matrices, additional_matrices, z, m, n, delta_pc):
    F1 = 0
    F2 = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            F1 += sub_matrices[f"A_{i}_{j}"] * pow(z, n * (i - 1) + (j - 1))
    for i in range(1, delta_pc + 1):
        for j in range(1, n + 1):
            F2 += additional_matrices[f"R_{i}_{j}"] * pow(z, n * (i - 1) + (j - 1))
    F = F1 + F2
    return F

# COMPUTE G(z)
def calc_G(sub_matrices, additional_matrices, z, m, n, p, delta_pc):
    G1 = 0
    G2 = 0
    for k in range(1, n + 1):
        for l in range(1, p + 1):
            G1 += sub_matrices[f"B_{k}_{l}"] * pow(
                z, n - k + (m + delta_pc) * n * (l - 1)
            )
    for k in range(1, n + 1):
        for l in range(1, delta_pc + 1):
            G2 += additional_matrices[f"R'_{k}_{l}"] * pow(
                z, (m + delta_pc) * n * p + n * l - k
            )
    G = G1 + G2
    return G

# GEN key (random 1 - 20)
def key_gen():
    key = random.randint(1, 20)
    return key

# COMPUTE recovery threshold Pr
def recovery_threshold(m, n, p, delta_pc, Pc):
    if (delta_pc == Pc/n):
        return (m + delta_pc) * n * (p + 1) + n * delta_pc - 1
    else:
        return (m + delta_pc) * n * (p + 1) - n * delta_pc + 2 * Pc - 1 

if __name__ == "__main__":
    # CREATE process (server when start)
    if len(sys.argv) == 1:
        start_time = time.time() # start count time
        # delete old data in total.txt & result.txt
        with open("total.txt", "w"):
            pass
        with open("result.txt", "w"):
            pass
        # M = 2, N = 4, P = 6, m = 2, n = 1, p = 3, Pc = 2
        M, N, P, m, n, p, Pc = map(int, input("Enter M, N, P, m, n, p, Pc: ").split())
        print("[+] Calculating and interacting with workers")

        delta_pc = math.ceil(Pc / n) # COMPUTE delta_pc

        # GEN 2 MATRIX
        matrix1 = create_matrix(M, N)
        matrix2 = create_matrix(N, P)

        # DIVIDE matrix & GEN additional matrix
        sub_matrices1 = print_sub_matrices_1(matrix1, M // m, N // n)
        additional_matrices1 = create_additional_matrices_1(M // m, N // n, n, delta_pc)
        sub_matrices2 = print_sub_matrices_2(matrix2, N // n, P // p)
        additional_matrices2 = create_additional_matrices_2(N // n, P // p, n, delta_pc)
        
        # CONVERT key -> numpy type
        key = np.int64(key_gen())
        key_json = int(key)

        with open("result.txt", "w") as f:
            f.write("Matrix 1:\n")
            np.savetxt(f, matrix1, fmt="%d")
            f.write("\nMatrix 2:\n")
            np.savetxt(f, matrix2, fmt="%d")
            f.write("\nGenerated Key: " + json.dumps(key_json) + '\n')

        for i in range(28):  # 28 workers (changeable)
            print(" ", end="\r")
            F = calc_F(sub_matrices1, additional_matrices1, i, m, n, delta_pc)
            G = calc_G(sub_matrices2, additional_matrices2, i, m, n, p, delta_pc)
            FxG = np.dot(F, G)
            FxG_key = np.dot(FxG, key)
            write_to_file("result.txt", f"worker {i+1} (FxG_key):\n{FxG_key}")
            F_json = json.dumps(F.tolist())
            G_json = json.dumps(G.tolist())
            r = multiprocessing.Process(target=worker, args=(i, F_json, G_json)) # parallel send from server to workers
            r.start()
            r.join() 
            correct_count = get_number_of_correct()
            incorrect_count = get_number_of_incorrect()
            if correct_count >= recovery_threshold(m, n, p, delta_pc, Pc):
                print("[+] Number of correct exceeds recovery threshold. Stopping all workers.")
                write_total(correct_count, start_time)
                    
                with open("total.txt", "r") as total_file:
                        total_content = total_file.read()
                print(total_content)
                
                # option: read result.txt
                while True:
                    with open("result.txt", "r") as result_file:
                        result_content = result_file.read()

                    choose = input("Do you want read result.txt? (yes/no): ")
                    if (choose == "yes"):
                        print("result.txt:")
                        print(result_content)
                        break
                    elif (choose == "no"):
                        break
                    else: 
                        print("please choose yes or no!")
                with open("total.txt", "w"):
                    pass     
                break
            
    # CHECK process (server when receive data from workers)  
    if len(sys.argv) == 4 and sys.argv[1] == "check":
        # receive worker sequence number, F mul G (json)
        i = int(sys.argv[2])
        FmulG_json = sys.argv[3]
        FmulG = np.array(json.loads(FmulG_json))
        
        # GET key gen from result.txt
        with open("result.txt", "r") as file:
            content = file.read()
            start_index = content.find("Generated Key:")
            if start_index != -1:
                end_index = content.find("\nworker", start_index)
                key_string = content[start_index + len("Generated Key:"):end_index].strip()
                key = int(key_string)
        key_int64 = np.int64(key)
        
        # CONVERT F mul G from numpy type -> string 
        FmulG_check = np.dot(FmulG, key_int64)
        FmulG_check_str = str(FmulG_check)
        
        # GET F mul G 
        with open('result.txt', 'r') as file:
            lines = file.readlines()
        last_line = lines[-1].strip()
        
        # CHECK server value & workers value
        if np.array_equal(FmulG_check_str, last_line):
            with open("result.txt", "a") as file:
                file.write("Correct Array\n")
            with open("total.txt", "r+") as total_file:
                lines = total_file.readlines()
                num_correct = 0
                num_incorrect = 0
                for line in lines:
                    if "number of correct:" in line:
                        num_correct = int(line.split(":")[1])
                    elif "number of incorrect:" in line:
                        num_incorrect = int(line.split(":")[1])

                num_correct += 1
                total_file.seek(0)
                total_file.truncate()
                total_file.write(f"number of correct: {num_correct}\n")
                total_file.write(f"number of incorrect: {num_incorrect}\n")
        else:
            with open("result.txt", "a") as file:
                file.write("Incorrect Array\n")
            with open("total.txt", "r+") as total_file:
                lines = total_file.readlines()
                num_correct = 0
                num_incorrect = 0
                for line in lines:
                    if "number of correct:" in line:
                        num_correct = int(line.split(":")[1])
                    elif "number of incorrect:" in line:
                        num_incorrect = int(line.split(":")[1])

                num_incorrect += 1
                total_file.seek(0)
                total_file.truncate()
                total_file.write(f"number of correct: {num_correct}\n")
                total_file.write(f"number of incorrect: {num_incorrect}\n")
