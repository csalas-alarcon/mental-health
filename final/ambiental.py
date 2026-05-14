# ambiental.py

def cuantizar_ambientales(df):
    """
    Convierte las respuestas de las columnas ambientales a la escala 0-10
    requerida por el sistema de lógica difusa.
    """
    
    # Mapeo para Col 32 (Tareas)
    mapa_tareas = {
        "Baja": 2,
        "Manejable": 5,
        "Saturada": 8,
        "Crítica": 10
    }
    
    # Mapeo para Col 35 (Pausas)
    mapa_pausas = {
        "Nulas": 0,
        "Esporádicas": 5,
        "Frecuentes": 10
    }
    
    # Mapeo para Col 36 (Entorno)
    mapa_entorno = {
        "Hostil": 0,
        "Neutro": 5,
        "Colaborativo": 10
    }

    # Aplicamos la conversión (usando los índices de columna que identificamos)
    df.iloc[:, 32] = df.iloc[:, 32].map(mapa_tareas).fillna(5) # Default Manejable
    df.iloc[:, 35] = df.iloc[:, 35].map(mapa_pausas).fillna(2)  # Default Esporádica
    df.iloc[:, 36] = df.iloc[:, 36].map(mapa_entorno).fillna(5) # Default Neutro

    return df