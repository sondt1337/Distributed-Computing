#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void printMatrix(int** matrix, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

int** createMatrix(int rows, int cols) {
    int** matrix = (int**)malloc(rows * sizeof(int*));
    for (int i = 0; i < rows; i++) {
        matrix[i] = (int*)malloc(cols * sizeof(int));
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = rand() % 100;  // Random numbers between 0 and 99
        }
    }
    return matrix;
}

void printSubMatrices(int** matrix, int rows, int cols, int subRows, int subCols) {
    for (int i = 0; i < rows; i += subRows) {
        for (int j = 0; j < cols; j += subCols) {
            for (int x = i; x < i + subRows && x < rows; x++) {
                for (int y = j; y < j + subCols && y < cols; y++) {
                    printf("%d ", matrix[x][y]);
                }
                printf("\n");
            }
            printf("\n");
        }
    }
}

int main() {
    srand(time(0));  // Seed for random number generator

    int M, N, P, m, n, p;
    printf("Enter M, N, P: ");
    scanf("%d %d %d %d %d %d", &M, &N, &P, &m, &n, &p);

    int** matrix1 = createMatrix(M, N);
    int** matrix2 = createMatrix(N, P);

    printf("Matrix 1:\n");
    printMatrix(matrix1, M, N);

    printf("Matrix 2:\n");
    printMatrix(matrix2, N, P);

    printf("Submatrices of Matrix 1:\n");
    printSubMatrices(matrix1, M, N, M/m, N/n);

    printf("Submatrices of Matrix 2:\n");
    printSubMatrices(matrix2, N, P, N/n, P/p);


    // Free memory matrix 
    for (int i = 0; i < M; i++) {
        free(matrix1[i]);
    }
    free(matrix1);
    for (int i = 0; i < N; i++) {
        free(matrix2[i]);
    }
    free(matrix2);

    return 0;
}
