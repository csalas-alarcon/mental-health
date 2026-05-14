import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Genera gráficos de media y varianza.')
    parser.add_argument('archivo', help='Archivo CSV a procesar (ej. mejores_predictores.csv)')
    args = parser.parse_args()

    os.makedirs('images', exist_ok=True)
    df = pd.read_csv(args.archivo, sep='\t')

    # Identificar columnas relevantes (MBI_Media, VALOR_*, o las NS_*)
    cols_to_plot = [col for col in df.columns if col not in ['ID', 'Status']]

    sns.set_theme(style="whitegrid")
    
    # Crear grid dinámico
    n_cols = len(cols_to_plot)
    fig, axes = plt.subplots(1, n_cols, figsize=(5 * n_cols, 6))
    if n_cols == 1: axes = [axes]

    for i, col in enumerate(cols_to_plot):
        # Boxplot muestra la mediana, cuartiles (varianza) y valores atípicos
        sns.boxplot(data=df, x='Status', y=col, ax=axes[i], palette="Set2")
        # Añadir un punto para la media exacta
        sns.pointplot(data=df, x='Status', y=col, ax=axes[i], estimator='mean', color='black', markers='D', errorbar=None)
        
        axes[i].set_title(f'Distribución: {col}')
        axes[i].set_ylabel('Puntuación')

    plt.tight_layout()
    out_path = os.path.join('images', 'distribucion_variables.png')
    plt.savefig(out_path)
    print(f"Gráfico guardado en {out_path}")

if __name__ == "__main__":
    main()