#include <iostream>
#include <pthread.h>
#include <ctime>

using namespace std;

#define N 100000000  // Menor que o original por limitação do Raspberry Pi 2
#define T 4          // 4 threads, pois são 4 núcleos físicos (1 thread/core)

double pi = 0.0;  // variável global que armazenará o resultado
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;  // inicializa o mutex

void* calculate_pi(void* id) {
    int my_id = (int)(long)id;  // converte o ponteiro para inteiro (compatível com 32 bits)

    int length_per_thread = N / T;
    int start = my_id * length_per_thread;
    int end = start + length_per_thread;

    double factor = (start % 2 == 0) ? 1.0 : -1.0;

    for (int i = start; i < end; i++, factor = -factor) {
        double term = factor / (2 * i + 1);

        pthread_mutex_lock(&lock);  // protege a região crítica
            pi += term;
        pthread_mutex_unlock(&lock);
    }

    return NULL;
}

int main() {
    pthread_t tid[T];  // vetor de threads

    clock_t tstart = clock();  // tempo de início

    for (int i = 0; i < T; i++) {
        pthread_create(&tid[i], NULL, calculate_pi, (void*)(long)i);
    }

    for (int i = 0; i < T; i++) {
        pthread_join(tid[i], NULL);
    }

    clock_t tend = clock();  // tempo de fim
    double elapsed = (double)(tend - tstart) / CLOCKS_PER_SEC;

    cout.precision(12);
    cout << fixed;
    cout << "PI estimate: " << 4 * pi << endl;
    cout << "Time: " << elapsed << " seconds" << endl;

    return 0;
}
