import pandas as pd
import numpy as np
from mbi import procesar_mbi
from uwes import procesar_uwes
from ambiental import cuantizar_ambientales
from reglas import ejecutar_inferencia_uwes
from estadísticas import generar_reporte_estadistico

def main():
    try:
        # Carga única del archivo
        df = pd.read_csv('encuesta.csv')
    except FileNotFoundError:
        print("Error: No se encontró encuesta.csv")
        return

    # Procesamiento encadenado usando el mismo DataFrame
    df = procesar_mbi(df)   # Procesa MBI
    df = procesar_uwes(df)  # Procesa UWES sin volver a leer el CSV
    df = cuantizar_ambientales(df)

    # Inferencia Difusa (UWES + Ambientales)
    # Se calculan los resultados usando las columnas de media y las ambientales (32, 35, 36)
    resultados_fuzzy = []
    print("\n--- INICIANDO DIAGNÓSTICO DE INFERENCIA ---")
    for i, row in df.iterrows():
        try:
            # 1. Extraemos los valores
            v = row['Vig_media']
            d = row['Ded_media']
            a = row['Abs_media']
            t = row.iloc[32] # Tareas
            p = row.iloc[35] # Pausas
            e = row.iloc[36] # Entorno

            # 2. Imprimimos el primer caso para ver qué está leyendo
            if i == 0:
                print(f"DEBUG Fila 0: Vig={v}, Ded={d}, Abs={a}, Tareas={t}, Pausas={p}, Entorno={e}")

            # 3. Ejecutamos la regla
            res = ejecutar_inferencia_uwes(v, d, a, t, p, e)
            resultados_fuzzy.append(res)

        except Exception as err:
            print(f"ERROR en fila {i}: {err}")
            # En lugar de nan, ponemos 5.0 (nivel medio) para no romper el análisis
            resultados_fuzzy.append(5.0)
    
    ### Acaba experimento 
    
    df['burnout_fuzzy'] = resultados_fuzzy
    df['burnout_fuzzy'] = df['burnout_fuzzy'].round(2)

    # Generación de reportes estadísticos para las columnas ambientales
    indices_ambientales = [32, 35, 36] # Eliminamos 33 y 34 que son texto
    generar_reporte_estadistico(df, indices_ambientales)

    # Guardado de resultados finales
    df.to_csv('resultados_finales.csv', index=False)
    print("\nResultados guardados en 'resultados_finales.csv'")

if __name__ == "__main__":
    main()