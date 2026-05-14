import pandas as pd
import numpy as np

# Cambiamos 'path' por 'df' para evitar la re-lectura del archivo
def cuantizar_uwes(df):
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

def asignar_niveles_uwes(df, col_media):
    p = np.percentile(df[col_media], [5, 25, 75, 95])
    
    def categorizar(v):
        if v < p[0]: return "Muy Bajo"
        if v < p[1]: return "Bajo"
        if v < p[2]: return "Medio"
        if v < p[3]: return "Alto"
        return "Muy alto"
    
    return df[col_media].apply(categorizar), p

def aplicar_niveles_estandar_uwes(df):
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

# Función principal que ahora recibe el DataFrame del main.py
def procesar_uwes(df):
    df = cuantizar_uwes(df)
    df = calcular_dimensiones_uwes(df)
    
    # 1. Por percentiles (Relativo)
    for dim in ["Vig", "Ded", "Abs"]:
        df[f"{dim}_nivel"], _ = asignar_niveles_uwes(df, f"{dim}_media")
    
    # 2. Por baremos oficiales (Estándar)
    df = aplicar_niveles_estandar_uwes(df)
    
    return df