# mbi.py

import pandas as pd
import numpy as np

# Str -> Int
def cuantizar_mbi(path):
    df = pd.read_csv(path)
    conversion = {
        "Nunca": 1,
        "Algunas veces al Año": 2,
        "Algunas veces al Mes": 3,
        "Algunas veces a la Semana": 4,
        "Diariamente": 5
    }
    # Mapeo de valores en las columnas de interés
    for col in df.columns[1:23]:
        df[col] = df[col].map(conversion)
    return df

# Sumar Variables
def calcular_variables_mbi(df):
    # Definición de columnas por dimensión
    ae_cols = df.columns[[1, 2, 3, 6, 8, 13, 14, 16, 20]]
    dp_cols = df.columns[[5, 10, 11, 15, 22]]
    rp_cols = df.columns[[4, 7, 9, 12, 17, 18, 19, 21]]

    # Sumas horizontales
    df["AE_total"] = df[ae_cols].sum(axis=1)
    df["DP_total"] = df[dp_cols].sum(axis=1)
    df["RP_total"] = df[rp_cols].sum(axis=1)
    return df

# Percentiles
def asignar_niveles_percentiles(df, col_total):
    p25 = np.percentile(df[col_total], 25)
    p75 = np.percentile(df[col_total], 75)
    
    def categorizar(valor):
        if valor < p25: return "Bajo"
        if valor > p75: return "Alto"
        return "Medio"
    
    return df[col_total].apply(categorizar), p25, p75

# Limites
def categorizar_por_limites(valor, bajo, alto):
    if valor < bajo: return "Bajo"
    if valor > alto: return "Alto"
    return "Medio"

def asignar_niveles_estandar(df):
    # Diccionario con los puntos de corte clínicos del MBI
    cortes = {
        "AE_total": (22, 26),
        "DP_total": (9, 11),
        "RP_total": (31, 34)
    }
    
    for col, (bajo, alto) in cortes.items():
        # Creamos la columna _nivel2 usando los cortes fijos
        nombre_nivel = col.replace("_total", "_nivel2")
        df[nombre_nivel] = df[col].apply(categorizar_por_limites, args=(bajo, alto))
    
    return df

# El Main
def procesar_mbi(input_csv):
    df = cuantizar_mbi(input_csv)
    df = calcular_dimensiones_mbi(df)
    
    # 1. Tus percentiles (Relativo)
    for dim in ["AE", "DP", "RP"]:
        df[f"{dim}_nivel"], _, _ = asignar_niveles(df, f"{dim}_total")
    
    # 2. Límites clínicos (Estandar)
    df = aplicar_niveles_estandar(df)
    
    print(df[["AE_nivel2", "AE_nivel", "DP_nivel2", "DP_nivel", "RP_nivel2", "RP_nivel"]])
    return df

if __name__ == "__main__":
    procesar_mbi("encuestas.csv")