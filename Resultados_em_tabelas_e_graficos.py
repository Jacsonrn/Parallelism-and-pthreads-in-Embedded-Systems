import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from IPython.display import HTML, display

# Definindo os dados
data = {
    'Teste': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Dimensões': ['8.000.000 × 8', '8.000.000 × 8', '8.000 × 8.000', '8.000 × 8.000', '8 × 8.000.000', '8 × 8.000.000'],
    'Descrição': ['Muitas linhas, poucas colunas', 'Muitas linhas, poucas colunas', 
                 'Matriz quadrada equilibrada', 'Matriz quadrada equilibrada',
                 'Poucas linhas, muitas colunas', 'Poucas linhas, muitas colunas'],
    'Threads': [1, 4, 1, 4, 1, 4],
    'Tempo (s)': [6.169000, 2.117436, 6.629000, 2.708000, 7.888000, 3.131400]
}

# Criando o DataFrame
df = pd.DataFrame(data)

# Calculando o speedup para cada teste
df_speedup = df.copy()
df_speedup['Speedup'] = 0.0

for teste in ['A', 'B', 'C']:
    tempo_1_thread = df[(df['Teste'] == teste) & (df['Threads'] == 1)]['Tempo (s)'].values[0]
    tempo_4_threads = df[(df['Teste'] == teste) & (df['Threads'] == 4)]['Tempo (s)'].values[0]
    speedup = tempo_1_thread / tempo_4_threads
    
    # Atualizando o DataFrame com os valores de speedup
    df_speedup.loc[(df_speedup['Teste'] == teste) & (df_speedup['Threads'] == 4), 'Speedup'] = speedup

# Formatando a coluna de Speedup para exibir apenas para 4 threads
df_speedup['Speedup'] = df_speedup['Speedup'].apply(lambda x: f'{x:.2f}x' if x > 0 else '')

# Estilizando a tabela
def highlight_rows(s):
    return ['background-color: #f2f2f2' if i % 2 == 0 else 'background-color: #e6e6e6' for i in range(len(s))]

styled_df = df_speedup.style.apply(highlight_rows, axis=0)
styled_df = styled_df.set_properties(**{'text-align': 'left'})
styled_df = styled_df.set_table_styles([
    {'selector': 'th', 'props': [('background-color', '#333'), ('color', 'white'), ('font-weight', 'bold')]},
    {'selector': 'caption', 'props': [('background-color', '#333'), ('color', 'white'), 
                                     ('font-size', '16px'), ('font-weight', 'bold'), ('padding', '10px')]}
])
styled_df = styled_df.set_caption('Tabela de Resultados – Atividade 3.2 (1 e 4 Threads)')

# Exibindo a tabela estilizada
display(styled_df)

# Criando visualização dos tempos de execução e speedup
plt.figure(figsize=(14, 10))

# Subplot para tempos de execução
plt.subplot(2, 1, 1)
bar_width = 0.35
index = np.arange(3)
labels = ['A (8M×8)\nMuitas linhas,\npoucas colunas', 'B (8K×8K)\nMatriz quadrada\nequilibrada', 'C (8×8M)\nPoucas linhas,\nmuitas colunas']

tempos_1_thread = [df[(df['Teste'] == t) & (df['Threads'] == 1)]['Tempo (s)'].values[0] for t in ['A', 'B', 'C']]
tempos_4_threads = [df[(df['Teste'] == t) & (df['Threads'] == 4)]['Tempo (s)'].values[0] for t in ['A', 'B', 'C']]

plt.bar(index, tempos_1_thread, bar_width, label='1 Thread', color='#ff7f0e', alpha=0.8)
plt.bar(index + bar_width, tempos_4_threads, bar_width, label='4 Threads', color='#1f77b4', alpha=0.8)

plt.ylabel('Tempo de Execução (s)')
plt.title('Comparação de Tempo de Execução por Número de Threads')
plt.xticks(index + bar_width/2, labels)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Subplot para speedup
plt.subplot(2, 1, 2)
speedups = [tempos_1_thread[i]/tempos_4_threads[i] for i in range(3)]

sns.barplot(x=labels, y=speedups, palette=['#2ca02c'])
plt.ylabel('Speedup (T1/T4)')
plt.title('Speedup Obtido com 4 Threads')
plt.axhline(y=4, color='r', linestyle='--', label='Speedup Teórico Ideal (4x)')
plt.text(2.1, 4.1, 'Speedup Ideal (4x)', color='r')

# Adicionando os valores de speedup nas barras
for i, v in enumerate(speedups):
    plt.text(i, v + 0.1, f'{v:.2f}x', ha='center')

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Exibindo o gráfico
plt.show()

# Mostrando estatísticas adicionais
print("\nEstatísticas de Desempenho:")
print("-" * 50)
print(f"Speedup Médio: {sum(speedups)/len(speedups):.2f}x")
print(f"Eficiência Média: {(sum(speedups)/len(speedups))/4*100:.2f}%")
print(f"Speedup Máximo: {max(speedups):.2f}x (Teste {['A', 'B', 'C'][speedups.index(max(speedups))]})")
print(f"Speedup Mínimo: {min(speedups):.2f}x (Teste {['A', 'B', 'C'][speedups.index(min(speedups))]})")
print("-" * 50)