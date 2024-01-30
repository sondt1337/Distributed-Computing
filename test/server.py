import numpy as np
import math

def printMatrix(matrix):
    for row in matrix:
        for val in row:
            print(val, end=" ")
        print()

def createMatrix(rows, cols):
    matrix = np.random.randint(100, size=(rows, cols))
    return matrix

def printSubMatrices1(matrix, submatrix_rows, submatrix_cols):
    num_rows, num_cols = matrix.shape 
    submatrices = {}  # create list of submatrices
    for i in range(0, num_rows, submatrix_rows):
        for j in range(0, num_cols, submatrix_cols):
            submatrix = matrix[i:i+submatrix_rows, j:j+submatrix_cols]
            submatrix_name = f"A_{i//submatrix_rows +1}_{j//submatrix_cols+ 1}"
            submatrices[submatrix_name] = submatrix  # save to list submatrices
    return submatrices 

def printSubMatrices2(matrix, submatrix_rows, submatrix_cols):
    num_rows, num_cols = matrix.shape 
    submatrices = {}  # create list of submatrices
    for i in range(0, num_rows, submatrix_rows):
        for j in range(0, num_cols, submatrix_cols):
            submatrix = matrix[i:i+submatrix_rows, j:j+submatrix_cols]
            submatrix_name = f"B_{i//submatrix_rows +1}_{j//submatrix_cols+ 1}"
            submatrices[submatrix_name] = submatrix  # save to list submatrices
    return submatrices 

def createAdditionalMatrices1(submatrix_rows, submatrix_cols, n, deltaPc):
    submatrices = {}  # create list of submatrices
    for i in range(1, deltaPc+1):
        for j in range(1, n +1):
            submatrix = createMatrix(submatrix_rows, submatrix_cols)
            submatrix_name = f"R_{i}_{j}"  # include loop indices in the name
            submatrices[submatrix_name] = submatrix  # save to list submatrices
    return submatrices

def createAdditionalMatrices2(submatrix_rows, submatrix_cols, n, deltaPc):
    submatrices = {}  # create list of submatrices
    for i in range(n, 0, -1):
        for j in range(1, deltaPc +1):
            submatrix = createMatrix(submatrix_rows, submatrix_cols)
            submatrix_name = f"R'_{i}_{j}"  # include loop indices in the name
            submatrices[submatrix_name] = submatrix  # save to list submatrices
    return submatrices

# M, N, P, m, n, p = map(int, input("Enter M, N, P, m, n, p: ").split())
M = 4
N = 6
P = 8
m = 2
n = 2 
p = 4
Pc = 3
deltaPc = math.ceil(Pc / n)
matrix1 = createMatrix(M, N)
matrix2 = createMatrix(N, P)

print("Matrix 1:")
printMatrix(matrix1)

print("Matrix 2:")
printMatrix(matrix2)

submatrices1 = printSubMatrices1(matrix1, M//m, N//n)
additional_matrices1 = createAdditionalMatrices1(M//m, N//n, n, deltaPc)

submatrices2 = printSubMatrices2(matrix2, N//n, P//p)
additional_matrices2 = createAdditionalMatrices2(N//n, P//p, n, deltaPc)

print(additional_matrices1)
print(submatrices1)
print(additional_matrices2)
print(submatrices2)