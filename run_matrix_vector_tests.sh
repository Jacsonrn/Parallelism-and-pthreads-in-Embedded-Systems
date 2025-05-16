#!/bin/bash

# Variáveis para os tamanhos da matriz (m x n)
declare -a Ms=(8000000 8000 8)
declare -a Ns=(8 8000 8000000)

# Quantidade de threads para testar
declare -a THREADS=(1 4 8)

# Nome do executável
EXEC="./matrix_vector_parallel"

# Função para compilar o programa alterando THREAD_COUNT via macro
compile_program() {
    local threads=$1
    echo "Compilando com THREAD_COUNT=$threads"
    g++ -pthread -O2 -DTHREAD_COUNT=$threads -o matrix_vector_parallel matrix_vector_parallel.cpp
}

# Função para executar teste e extrair tempo
run_test() {
    local m=$1
    local n=$2
    local threads=$3

    # Executa 10 vezes e calcula média
    sum=0
    for i in {1..10}; do
        # Executa e captura tempo
        time_output=$($EXEC $m $n)
        # Extrai o tempo da saída (assumindo linha: Tempo de execucao: X.XXXXX segundos)
        time=$(echo "$time_output" | grep "Tempo de execucao" | awk '{print $3}')
        sum=$(echo "$sum + $time" | bc)
    done
    # Calcula média
    avg=$(echo "scale=6; $sum / 10" | bc)
    echo "$avg"
}

# Cabeçalho CSV
echo "M,N,Threads,Tempo_medio_s" > resultados.csv

# Loop principal
for idx in ${!Ms[@]}; do
    M=${Ms[$idx]}
    N=${Ns[$idx]}

    for T in "${THREADS[@]}"; do
        compile_program $T
        avg_time=$(run_test $M $N $T)
        echo "$M,$N,$T,$avg_time" >> resultados.csv
        echo "Testado: M=$M N=$N Threads=$T Média=$avg_time s"
    done
done

echo "Testes concluídos. Resultados salvos em resultados.csv"
