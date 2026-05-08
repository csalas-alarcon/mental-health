import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Cargar datos
df = pd.read_csv("normalized_burnout_dataset.csv", sep='\t')

# 2. Calcular la media de las escalas por usuario para simplificar el análisis
mbi_cols = [c for c in df.columns if c.startswith('MBI_')]
uwes_cols = [c for c in df.columns if c.startswith('UWES_')]

df['MBI_Global'] = df[mbi_cols].mean(axis=1)
df['UWES_Global'] = df[uwes_cols].mean(axis=1)

# 3. Análisis Estadístico (Media, Varianza y Sigma)
stats = df.groupby('Status')[['MBI_Global', 'UWES_Global']].agg(['mean', 'var', 'std']).round(3)
print("=== Análisis Estadístico (Media, Varianza, Sigma) ===")
print(stats)

# 4. Visualización Gráfica (Distribución con curva de densidad)
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Gráfico MBI
sns.histplot(data=df, x='MBI_Global', hue='Status', kde=True, element='step', ax=axes[0])
axes[0].set_title('Distribución de Puntuación MBI (Burnout)')
axes[0].set_xlabel('Puntuación Normalizada (0 a 1)')

# Gráfico UWES
sns.histplot(data=df, x='UWES_Global', hue='Status', kde=True, element='step', ax=axes[1])
axes[1].set_title('Distribución de Puntuación UWES (Engagement)')
axes[1].set_xlabel('Puntuación Normalizada (0 a 1)')

plt.tight_layout()
plt.savefig('distribucion_burnout.png')
print("\nGráfico guardado como 'distribucion_burnout.png'.")