import pandas as pd
import sys

def aggregate_variables(input_path, output_path):
    # Cargamos el archivo cuantificado
    df = pd.read_csv(input_path, sep='\t')    
    
    # Creamos un diccionario para almacenar los nuevos datos procesados
    # Esto asegura que "sustituimos" las columnas viejas por las nuevas
    processed_data = {}

    # --- MBI: CÁLCULO POR SUMA (Basado en memoria y paper) ---
    # Índices: AE(0,1,2,5,7,12,13,15,19), DP(4,9,10,14,21), RP(3,6,8,11,16,17,18,20)
    
    ae_cols = [0, 1, 2, 5, 7, 12, 13, 15, 19]
    dp_cols = [4, 9, 10, 14, 21]
    rp_cols = [3, 6, 8, 11, 16, 17, 18, 20]

    processed_data['MBI_AE'] = df.iloc[:, ae_cols].sum(axis=1)
    processed_data['MBI_DP'] = df.iloc[:, dp_cols].sum(axis=1)
    processed_data['MBI_RP'] = df.iloc[:, rp_cols].sum(axis=1)

    # --- UWES-9: CÁLCULO POR MEDIA (Escala 0-6 oficial) ---
    # Columnas 22 a 30 (índices 0-indexed después de limpiar MBI)
    
    vigor_cols = [22, 23, 26]
    dedic_cols = [24, 25, 28]
    absor_cols = [27, 29, 30]

    processed_data['UWES_Vigor'] = df.iloc[:, vigor_cols].mean(axis=1).round(2)
    processed_data['UWES_Dedicacion'] = df.iloc[:, dedic_cols].mean(axis=1).round(2)
    processed_data['UWES_Absorcion'] = df.iloc[:, absor_cols].mean(axis=1).round(2)
    processed_data['UWES_Engagement_Total'] = df.iloc[:, 22:31].mean(axis=1).round(2)

    # --- NS: VARIABLES DE CONTEXTO (Nuestro Sistema) ---
    # Mapeamos las últimas preguntas de la encuesta (32 a 36)
    
    processed_data['NS_Tareas_Criticas'] = df.iloc[:, 31]
    processed_data['NS_Exposicion_Pantallas'] = df.iloc[:, 32]
    processed_data['NS_Calidad_Sueno'] = df.iloc[:, 33]
    processed_data['NS_Pausas_Activas'] = df.iloc[:, 34]
    processed_data['NS_Entorno_Laboral'] = df.iloc[:, 35]

    # Crear el DataFrame final sustituyendo las preguntas por estas variables
    df_final = pd.DataFrame(processed_data)

    # Guardar el resultado final
    df_final.to_csv(output_path, index=False, sep='\t')
    print(f"Agregación completada en: {output_path}")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    aggregate_variables(input_file, output_file)