import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import os
import sys

def find_best_trio(input_path):
    # Leemos los datos normalizados (0-1)
    df = pd.read_csv(input_path, sep='\t')
    
    # Definimos nuestras variables de interés
    # X: Las 5 variables de contexto (Nuestro Sistema)
    # y: El Agotamiento Emocional (MBI_AE) como objetivo principal
    ns_vars = [
        'NS_Tareas_Criticas', 
        'NS_Exposicion_Pantallas', 
        'NS_Calidad_Sueno', 
        'NS_Pausas_Activas', 
        'NS_Entorno_Laboral'
    ]
    
    X = df[ns_vars]
    y = df['MBI_AE']

    # Inicializamos el modelo Random Forest
    # Usamos 100 árboles y una semilla fija para que el resultado sea reproducible
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Extraemos la importancia de las variables (Feature Importance)
    importances = model.feature_importances_
    
    # Creamos un ranking
    feature_importance_df = pd.DataFrame({
        'Variable': ns_vars,
        'Importancia': importances
    }).sort_values(by='Importancia', ascending=False)

    print("--- Ranking de Importancia (Random Forest) ---")
    print(feature_importance_df)
    print("-" * 45)

    # Seleccionamos el Top 3
    top_3 = feature_importance_df.head(3)['Variable'].tolist()
    
    print(f"El trío más útil para predecir el Burnout es:")
    for i, var in enumerate(top_3, 1):
        print(f"{i}. {var}")
        
    return top_3

if __name__ == "__main__":
    input_file = sys.argv[1]
    find_best_trio(input_file)