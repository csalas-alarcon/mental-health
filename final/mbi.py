# mbi.py
import pandas as pd
import numpy as np

# Cambiamos 'path' por 'df' para no volver a leer el CSV
def cuantizar_mbi(df):
    conversion = {
        "Nunca": 1,
        "Algunas veces al Año": 2,
        "Algunas veces al Mes": 3,
        "Algunas veces a la Semana": 4,
        "Diariamente": 5
    }
    for col in df.columns[1:23]:
        df[col] = df[col].map(conversion)
    return df

def calcular_dimensiones_mbi(df): # Nombre corregido
    ae_cols = df.columns[[1, 2, 3, 6, 8, 13, 14, 16, 20]]
    dp_cols = df.columns[[5, 10, 11, 15, 22]]
    rp_cols = df.columns[[4, 7, 9, 12, 17, 18, 19, 21]]

    df["AE_total"] = df[ae_cols].sum(axis=1)
    df["DP_total"] = df[dp_cols].sum(axis=1)
    df["RP_total"] = df[rp_cols].sum(axis=1)
    return df

def asignar_niveles(df, col_total): # Nombre para coincidir con el main
    p25 = np.percentile(df[col_total], 25)
    p75 = np.percentile(df[col_total], 75)
    
    def categorizar(valor):
        if valor < p25: return "Bajo"
        if valor > p75: return "Alto"
        return "Medio"
    
    return df[col_total].apply(categorizar), p25, p75

def categorizar_por_limites(valor, bajo, alto):
    if valor < bajo: return "Bajo"
    if valor > alto: return "Alto"
    return "Medio"

def aplicar_niveles_estandar(df): # Nombre para coincidir con el main
    cortes = {
        "AE_total": (22, 26),
        "DP_total": (9, 11),
        "RP_total": (31, 34)
    }
    for col, (bajo, alto) in cortes.items():
        nombre_level = col.replace("_total", "_nivel2")
        df[nombre_level] = df[col].apply(categorizar_por_limites, args=(bajo, alto))
    return df

# Función principal que llamará main.py
def procesar_mbi(df):
    df = cuantizar_mbi(df)
    df = calcular_dimensiones_mbi(df)
    
    for dim in ["AE", "DP", "RP"]:
        df[f"{dim}_nivel"], _, _ = asignar_niveles(df, f"{dim}_total")
    
    df = aplicar_niveles_estandar(df)
    return df