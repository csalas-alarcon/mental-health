# ambiental.py

def cuantizar_ambientales(df):
    """
    Convierte las respuestas de las columnas ambientales a la escala 0-10
    sustituyendo las columnas para evitar conflictos de tipo (dtype 'str').
    """
    
    # Mapeos según las etiquetas identificadas
    mapa_tareas = {
        "Baja": 2,
        "Manejable": 5,
        "Saturada": 8,
        "Crítica": 10
    }
    
    mapa_pausas = {
        "Nulas": 0,
        "Esporádicas": 5,
        "Frecuentes": 10
    }
    
    mapa_entorno = {
        "Hostil": 0,
        "Neutro": 5,
        "Colaborativo": 10
    }

    # Obtenemos los nombres de las columnas por su índice
    col_tareas = df.columns[32]
    col_pausas = df.columns[35]
    col_entorno = df.columns[36]

    # Sustituimos la columna entera asignando la nueva serie mapeada
    # Esto fuerza a Pandas a aceptar el nuevo tipo numérico (float)
    df[col_tareas] = df[col_tareas].map(mapa_tareas).fillna(5).astype(float)
    df[col_pausas] = df[col_pausas].map(mapa_pausas).fillna(2).astype(float)
    df[col_entorno] = df[col_entorno].map(mapa_entorno).fillna(5).astype(float)

    return df