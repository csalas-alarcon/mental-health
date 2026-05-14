# estadisticas.py

import pandas as pd

def generar_reporte_estadistico(df, indices_columnas_objetivo):
    """
    indices_columnas_objetivo: lista de índices, ej. [32, 33, 34, 35, 36]
    """
    orden_niveles = {"Bajo": 1, "Medio": 2, "Alto": 3}
    dimensiones = ["AE", "DP", "RP"]

    for idx in indices_columnas_objetivo:
        col_objetivo = df.columns[idx]
        print(f"\n\n" + "#" * 40)
        print(f" REPORTE PARA COLUMNA: {col_objetivo} (Índice {idx})")
        print("#" * 40)

        for dim in dimensiones:
            col_nivel = f"{dim}_nivel"
            
            # Ordenar y mostrar datos crudos
            df['temp_sort'] = df[col_nivel].map(orden_niveles)
            df_ordenado = df.sort_values(['temp_sort', col_objetivo])
            
            print(f"\n--- Detalle {dim} vs {col_objetivo} ---")
            print(df_ordenado[[col_nivel, col_objetivo]].to_string(index=False, header=False))

            # Calcular estadísticas con GroupBy
            stats = df.groupby(col_nivel)[col_objetivo].agg(['sum', 'count', 'mean']).round(2)

            for nivel in ["Bajo", "Medio", "Alto"]:
                if nivel in stats.index:
                    print(f"\n{dim} - {nivel}")
                    print(f"Suma: {stats.loc[nivel, 'sum']}")
                    print(f"Cantidad: {int(stats.loc[nivel, 'count'])}")
                    print(f"Media: {stats.loc[nivel, 'mean']}")

            # Limpiar columna temporal tras cada dimensión
            df.drop(columns=['temp_sort'], inplace=True)

    return df

def reporte_visual_ordenado(df, col_etiqueta_idx, col_valor_idx):
    """
    Imprime una lista ordenada por nivel y luego por valor numérico.
    """
    orden_niveles = {"Bajo": 1, "Medio": 2, "Alto": 3}
    
    col_etiqueta = df.columns[col_etiqueta_idx]
    col_valor = df.columns[col_valor_idx]
    
    # Crear peso para ordenar
    df['temp_sort'] = df[col_etiqueta].map(orden_niveles)
    
    # Ordenar por el peso del nivel y luego por el valor numérico
    df_final = df.sort_values(['temp_sort', col_valor])
    
    # Imprimir resultado limpio
    print(f"\n--- Reporte Ordenado: {col_etiqueta} y {col_valor} ---")
    print(df_final[[col_etiqueta, col_valor]].to_string(index=False, header=False))
    
    # Limpieza
    df.drop(columns=['temp_sort'], inplace=True)