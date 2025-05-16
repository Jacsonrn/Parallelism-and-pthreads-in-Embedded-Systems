#include <iostream>
#include <pthread.h>
#include <cstdlib>    // srand, rand, atoi
#include <ctime>      // clock
#include <iomanip>    // setprecision

using namespace std;

#ifndef THREAD_COUNT
#define THREAD_COUNT 4
#endif

int m, n;              // dimensões da matriz

double **A;            // matriz dinâmica m x n
double *x;             // vetor n x 1
double *y;             // vetor resultado m x 1

pthread_t threads[THREAD_COUNT];

// Função para gerar número aleatório entre 0 e 5
double randomDouble() {
    return ((double)rand() / RAND_MAX) * 5.0;
}

// Aloca matriz dinâmica
double** allocateMatrix(int rows, int cols) {
    double **matrix = new double*[rows];
    for (int i = 0; i < rows; i++) {
        matrix[i] = new double[cols];
    }
    return matrix;
}

// Libera matriz dinâmica
void freeMatrix(double **matrix, int rows) {
    for (int i = 0; i < rows; i++) {
        delete[] matrix[i];
    }
    delete[] matrix;
}

// Inicializa matriz e vetor com valores aleatórios
void initializeData() {
    srand(time(NULL));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            A[i][j] = randomDouble();
        }
    }
    for (int i = 0; i < n; i++) {
        x[i] = randomDouble();
    }
}

// Função que cada thread vai executar
void* multMatrixVectorParallel(void* rank) {
    int my_rank = (int)(long)rank;
    int local_m = m / THREAD_COUNT;  // linhas por thread
    int start = my_rank * local_m;
    int end = (my_rank == THREAD_COUNT - 1) ? m : start + local_m;  // último pode pegar resto

    for (int i = start; i < end; i++) {
        y[i] = 0.0;
        for (int j = 0; j < n; j++) {
            y[i] += A[i][j] * x[j];
        }
    }
    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cout << "Uso: " << argv[0] << " <m> <n>\n";
        return 1;
    }

    m = atoi(argv[1]);
    n = atoi(argv[2]);

    A = allocateMatrix(m, n);
    x = new double[n];
    y = new double[m];

    initializeData();

    clock_t start_time = clock();

    for (long i = 0; i < THREAD_COUNT; i++) {
        pthread_create(&threads[i], NULL, multMatrixVectorParallel, (void*)i);
    }

    for (int i = 0; i < THREAD_COUNT; i++) {
        pthread_join(threads[i], NULL);
    }

    clock_t end_time = clock();

    double elapsed = (double)(end_time - start_time) / CLOCKS_PER_SEC;

    cout << fixed << setprecision(6);
    cout << "Tempo de execucao: " << elapsed << " segundos" << endl;

    // Imprimir alguns valores para validação
    cout << "y[0] = " << y[0] << endl;
    cout << "y[" << m-1 << "] = " << y[m-1] << endl;

    freeMatrix(A, m);
    delete[] x;
    delete[] y;

    return 0;
}
