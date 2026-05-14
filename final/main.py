import pandas as pd
import numpy as np
from mbi import procesar_mbi
from uwes import procesar_uwes
from ambiental import cuantizar_ambientales
from reglas import ejecutar_inferencia_uwes
from estadísticas import generar_reporte_estadistico

def main():
    # Carga de datos
    try:
        df = pd.read_csv('encuesta.csv')
    except FileNotFoundError:
        print("Error: No se encontró encuesta.csv")
        return

    # Procesamiento de escalas y niveles
    df = procesar_mbi(df)
    df = procesar_uwes(df)
    df = cuantizar_ambientales(df)

    # Inferencia Difusa (UWES + Ambientales)
    # Se calculan los resultados usando las columnas de media y las ambientales (32, 35, 36)
    resultados_fuzzy = []
    for i, row in df.iterrows():
        try:
            res = ejecutar_inferencia_uwes(
                v_val=row['Vig_media'], 
                d_val=row['Ded_media'], 
                a_val=row['Abs_media'],
                t_val=row.iloc[32], 
                p_val=row.iloc[35], 
                e_val=row.iloc[36]
            )
            resultados_fuzzy.append(res)
        except Exception as e:
            resultados_fuzzy.append(np.nan)
    
    df['burnout_fuzzy'] = resultados_fuzzy

    # Generación de reportes estadísticos para las columnas ambientales
    indices_ambientales = [32, 33, 34, 35, 36]
    generar_reporte_estadistico(df, indices_ambientales)

    # Guardado de resultados finales
    df.to_csv('resultados_finales.csv', index=False)
    print("\nResultados guardados en 'resultados_finales.csv'")

if __name__ == "__main__":
    main()