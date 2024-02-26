# python server.py create
import subprocess
import multiprocessing
import numpy as np
import math
import random
import json
import sys 

def worker(i, F_json, G_json):
    subprocess.run(["python", "worker.py", str(i), F_json, G_json])


def write_to_file(file, content):
    with open(file, 'a') as f:
        f.write(content + '\n')


def create_matrix(rows, cols):
    matrix = np.random.randint(100, size=(rows, cols))
    return matrix


def print_sub_matrices_1(matrix, submatrix_rows, submatrix_cols):
    num_rows, num_cols = matrix.shape
    sub_matrices = {}
    for i in range(0, num_rows, submatrix_rows):
        for j in range(0, num_cols, submatrix_cols):
            sub_matrix = matrix[i : i + submatrix_rows, j : j + submatrix_cols]
            sub_matrix_name = f"A_{i//submatrix_rows +1}_{j//submatrix_cols+ 1}"
            sub_matrices[sub_matrix_name] = sub_matrix
    return sub_matrices


def print_sub_matrices_2(matrix, submatrix_rows, submatrix_cols):
    num_rows, num_cols = matrix.shape
    sub_matrices = {}
    for i in range(0, num_rows, submatrix_rows):
        for j in range(0, num_cols, submatrix_cols):
            sub_matrix = matrix[i : i + submatrix_rows, j : j + submatrix_cols]
            sub_matrix_name = f"B_{i//submatrix_rows +1}_{j//submatrix_cols+ 1}"
            sub_matrices[sub_matrix_name] = sub_matrix
    return sub_matrices


def create_additional_matrices_1(submatrix_rows, submatrix_cols, n, delta_pc):
    additional_matrices = {}
    for i in range(1, delta_pc + 1):
        for j in range(1, n + 1):
            sub_matrix = create_matrix(submatrix_rows, submatrix_cols)
            sub_matrix_name = f"R_{i}_{j}"
            additional_matrices[sub_matrix_name] = sub_matrix
    return additional_matrices


def create_additional_matrices_2(submatrix_rows, submatrix_cols, n, delta_pc):
    additional_matrices = {}
    for i in range(n, 0, -1):
        for j in range(1, delta_pc + 1):
            sub_matrix = create_matrix(submatrix_rows, submatrix_cols)
            sub_matrix_name = f"R'_{i}_{j}"
            additional_matrices[sub_matrix_name] = sub_matrix
    return additional_matrices


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


def key_gen():
    key = random.randint(1, 20)
    return key

def recovery_threshold(m, n, p, delta_pc, Pc):
    if (delta_pc == Pc/n):
        return (m + delta_pc) * n * (p+1) + n * delta_pc - 1
    else:
        return (m + delta_pc) * n * (p + 1) - n * delta_pc + 2 * Pc - 1 

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "create":

        # M = 2, N = 4, P = 6, m = 2, n = 1, p = 3, Pc = 2
        M, N, P, m, n, p, Pc = map(int, input("Enter M, N, P, m, n, p, Pc: ").split())
        delta_pc = math.ceil(Pc / n)
        matrix1 = create_matrix(M, N)
        matrix2 = create_matrix(N, P)

        sub_matrices1 = print_sub_matrices_1(matrix1, M // m, N // n)
        additional_matrices1 = create_additional_matrices_1(M // m, N // n, n, delta_pc)
        sub_matrices2 = print_sub_matrices_2(matrix2, N // n, P // p)
        additional_matrices2 = create_additional_matrices_2(N // n, P // p, n, delta_pc)

        key = np.int64(key_gen())
        key_json = int(key)

        with open("result.txt", "w") as f:
            # f.write("Matrix 1:\n")
            # np.savetxt(f, matrix1, fmt="%d")
            # f.write("\nMatrix 2:\n")
            # np.savetxt(f, matrix2, fmt="%d")
            f.write("Generated Key: " + json.dumps(key_json) + '\n')
            # f.write("Program execution completed.\n")

        for i in range(5):  # 5 workers
            F = calc_F(sub_matrices1, additional_matrices1, i, m, n, delta_pc)
            G = calc_G(sub_matrices2, additional_matrices2, i, m, n, p, delta_pc)
            FxG = np.dot(F, G)
            FxG_key = np.dot(FxG, key)
            write_to_file("result.txt", f"worker {i+1} (FxG_key):\n{FxG_key}")
            F_json = json.dumps(F.tolist())
            G_json = json.dumps(G.tolist())
            r = multiprocessing.Process(target=worker, args=(i, F_json, G_json))
            r.start()
            r.join() 
    if len(sys.argv) == 4 and sys.argv[1] == "check":
        i = int(sys.argv[2])
        FmulG_json = sys.argv[3]
        FmulG = np.array(json.loads(FmulG_json))
        
        with open("result.txt", "r") as file:
            content = file.read()
            start_index = content.find("Generated Key:")
            if start_index != -1:
                end_index = content.find("\nworker", start_index)
                key_string = content[start_index + len("Generated Key:"):end_index].strip()
                key = int(key_string)
        key_int64 = np.int64(key)
        
        FmulG_check = np.dot(FmulG, key_int64)
        FmulG_check_str = str(FmulG_check)
        
        with open('result.txt', 'r') as file:
            lines = file.readlines()
        last_line = lines[-1].strip()
        
        
        if np.array_equal(FmulG_check_str, last_line):
            with open("result.txt", "a") as file:
                file.write("Correct Array\n")
        else:
            with open("result.txt", "a") as file:
                file.write("Incorrect Array\n")