# uwes.py 

import pandas as pd
import numpy as np

# Cuantizar
def cuantizar_uwes(path):
    df = pd.read_csv(path)
    conversion = {
        "Nunca": 0,
        "Algunas veces al Año": 1,
        "Una vez por Mes": 2,
        "Algunas veces al Mes": 3,
        "Una vez por Semana": 4,
        "Algunas veces a la Semana": 5,
        "Diariamente": 6
    }
    # Mapeo de columnas UWES (23 a 31 inclusive)
    cols_uwes = df.columns[23:32]
    for col in cols_uwes:
        df[col] = df[col].map(conversion).fillna(0)
    return df

# Conseguir Variables
def calcular_dimensiones_uwes(df):
    # Definición por índices
    vig_cols = df.columns[[23, 24, 27]]
    ded_cols = df.columns[[25, 26, 29]]
    abs_cols = df.columns[[28, 30, 31]]

    # Calculamos medias redondeadas a 2 decimales
    df["Vig_media"] = df[vig_cols].mean(axis=1).round(2)
    df["Ded_media"] = df[ded_cols].mean(axis=1).round(2)
    df["Abs_media"] = df[abs_cols].mean(axis=1).round(2)
    return df

# Categorizar por Percentiles
def asignar_niveles_uwes(df, col_media):
    # Obtenemos los 4 percentiles necesarios
    p = np.percentile(df[col_media], [5, 25, 75, 95])
    
    def categorizar(v):
        if v < p[0]: return "Muy Bajo"
        if v < p[1]: return "Bajo"
        if v < p[2]: return "Medio"
        if v < p[3]: return "Alto"
        return "Muy alto"
    
    return df[col_media].apply(categorizar), p

# Categorizar por Límites
def aplicar_niveles_estandar_uwes(df):
    # Diccionario con los baremos oficiales del UWES
    cortes = {
        "Vig_media": [2.0, 3.25, 4.80, 5.65],
        "Ded_media": [1.33, 2.90, 4.70, 5.69],
        "Abs_media": [1.77, 2.33, 4.20, 5.33]
    }
    
    def categorizar_estandar(v, limites):
        if v <= limites[0]: return "Muy Bajo"
        if v < limites[1]:  return "Bajo"
        if v < limites[2]:  return "Medio"
        if v < limites[3]:  return "Alto"
        return "Muy alto"

    for col, limites in cortes.items():
        nombre_nivel2 = col.replace("_media", "_nivel2")
        df[nombre_nivel2] = df[col].apply(categorizar_estandar, limites=limites)
    
    return df

# El Main
def procesar_uwes(input_csv):
    df = cuantizar_uwes(input_csv)
    df = calcular_dimensiones_uwes(df)
    
    # 1. Por tus percentiles (Relativo)
    for dim in ["Vig", "Ded", "Abs"]:
        df[f"{dim}_nivel"], _ = asignar_niveles_uwes(df, f"{dim}_media")
    
    # 2. Por baremos oficiales (Estándar)
    df = aplicar_niveles_estandar_uwes(df)
    
    print(df[["Vig_nivel2", "Vig_nivel", "Ded_nivel2", "Ded_nivel", "Abs_nivel2", "Abs_nivel"]])
    return df

if __name__ == "__main__":
    procesar_uwes("encuestas.csv")