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

def printSubMatrices(matrix, subRows, subCols):
    rows, cols = matrix.shape
    for i in range(0, rows, subRows):
        for j in range(0, cols, subCols):
            for x in range(i, min(i + subRows, rows)):
                for y in range(j, min(j + subCols, cols)):
                    print(matrix[x][y], end=" ")
                print()
            print()

M, N, P, m, n, p = map(int, input("Enter M, N, P, m, n, p: ").split())
Pc = 2
deltaPc = math.ceil(Pc / n)
# print(deltaPc)

matrix1 = createMatrix(M, N)
matrix2 = createMatrix(N, P)

print("Matrix 1:")
printMatrix(matrix1)

print("Matrix 2:")
printMatrix(matrix2)

print("Submatrices of Matrix 1:")
printSubMatrices(matrix1, M//m, N//n)

print("Submatrices of Matrix 2:")
printSubMatrices(matrix2, N//n, P//p)
