#include <iostream>
#include <ctime>

using namespace std;

#define N 100000000  // número de termos da série de Leibniz

int main() {
    double pi = 0.0;
    double factor = 1.0;

    clock_t tstart = clock();

    for (int i = 0; i < N; i++, factor = -factor) {
        pi += factor / (2 * i + 1);
    }

    clock_t tend = clock();
    double elapsed = (double)(tend - tstart) / CLOCKS_PER_SEC;

    cout.precision(12);
    cout << fixed;
    cout << "PI estimate: " << 4 * pi << endl;
    cout << "Time: " << elapsed << " seconds" << endl;

    return 0;
}
