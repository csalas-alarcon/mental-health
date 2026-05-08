import pandas as pd

# 1. Cargar el dataset original
df = pd.read_csv("simulated_burnout_dataset.csv", sep='\t')

# 2. Barajar todas las filas
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# 3. Diccionarios de mapeo
mbi_map = {
    "Nunca": 0,
    "Algunas veces al Año": 1,
    "Algunas veces al Mes": 3, # Mantengo los valores del script anterior
    "Algunas veces a la Semana": 5,
    "Diariamente": 6
}

# UWES invertido directamente en el mapa (0 es máximo burnout)
uwes_map_invertido = {
    "Nunca": 6,
    "Algunas veces al Año": 5,
    "Una vez por Mes": 4,
    "Algunas veces al Mes": 3,
    "Una vez por Semana": 2,
    "Algunas veces a la Semana": 1,
    "Diariamente": 0
}

# Mapas NS con las inversiones solicitadas
ns_maps = {
    "NS_Tareas_Criticas": {"Baja": 0, "Manejable": 1, "Saturada": 2, "Crítica": 3},
    "NS_Pantallas": {"Reducida (<4h)": 0, "Estándar (5-8h)": 1, "Excesiva (>10h)": 2},
    # Invertidos:
    "NS_Sueno": {"Insuficiente": 3, "Pobre": 2, "Aceptable": 1, "Excelente y Reparador": 0},
    "NS_Pausas_Activas": {"Nulas": 2, "Esporádicas": 1, "Frecuentes": 0},
    "NS_Entorno": {"Hostil": 2, "Neutro Colaborativo": 1, "Colaborativo": 0}
}

# Columnas MBI que deben invertirse (Preguntas 4, 7, 9, 12, 17, 18, 19, 21)
mbi_inversas = [
    "MBI_Comprension_Facil", "MBI_Efectividad_Problemas", "MBI_Influencia_Positiva",
    "MBI_Energico", "MBI_Clima_Agradable", "MBI_Estimulo_Atencion",
    "MBI_Cosas_Valiosas", "MBI_Trato_Emocional"
]

# 4. Aplicar mapeo y normalización
for col in df.columns:
    if col in mbi_inversas:
        # Mapear e invertir (6 - valor) y normalizar
        df[col] = (6 - df[col].map(mbi_map)) / 6.0
        
    elif col.startswith("MBI_"):
        # Mapeo normal
        df[col] = df[col].map(mbi_map) / 6.0
    
    elif col.startswith("UWES_"):
        # Mapeo ya invertido en el diccionario
        df[col] = df[col].map(uwes_map_invertido) / 6.0
        
    elif col in ns_maps:
        # Mapear según diccionario propio y normalizar por su valor máximo
        mapping = ns_maps[col]
        max_val = max(mapping.values())
        df[col] = df[col].map(mapping) / max_val

# 5. Guardar en un NUEVO archivo CSV
output_filename = "normalized_burnout_dataset.csv"
df.to_csv(output_filename, sep='\t', index=False, encoding='utf-8')

print(f"Datos normalizados y corregidos guardados en: {output_filename}")