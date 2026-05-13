import pandas as pd
import sys

def normalize_to_range(input_path, output_path):
    df = pd.read_csv(input_path, sep='\t')
    df_norm = df.copy()

    # Definición de rangos teóricos según la memoria
    # MBI (Suma de 1 a 5)
    ranges = {
        'MBI_AE': (9, 45),   # 9 preguntas * [1,5] 
        'MBI_DP': (5, 25),   # 5 preguntas * [1,5] 
        'MBI_RP': (8, 40),   # 8 preguntas * [1,5] 
        # UWES (Media de 0 a 6) [cite: 483]
        'UWES_Vigor': (0, 6),
        'UWES_Dedicacion': (0, 6),
        'UWES_Absorcion': (0, 6),
        'UWES_Engagement_Total': (0, 6),
        # NS Variables (Escala 0 a 10 en Forms) [cite: 571]
        'NS_Tareas_Criticas': (0, 10),
        'NS_Exposicion_Pantallas': (0, 10),
        'NS_Calidad_Sueno': (0, 10),
        'NS_Pausas_Activas': (0, 10),
        'NS_Entorno_Laboral': (0, 10)
    }

    for col, (vmin, vmax) in ranges.items():
        if col in df_norm.columns:
            # Aplicamos formula Min-Max: (x - min) / (max - min) [cite: 390]
            df_norm[col] = (df_norm[col] - vmin) / (vmax - vmin)
            # Aseguramos que se mantengan en el rango [0, 1] por si hay outliers
            df_norm[col] = df_norm[col].clip(0, 1).round(4)

    # Guardado DENTRO de la función
    df_norm.to_csv(output_path, index=False, sep='\t')
    print(f"Normalización completada en: {output_path}")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    normalize_to_range(input_file, output_file)