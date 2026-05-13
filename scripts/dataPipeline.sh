#!/bin/bash

# 1. Preparación del entorno
echo "--- Iniciando Pipeline de Datos ---"

# Crear carpeta de salida si no existe
mkdir -p data/output

# Instalar dependencias
echo "[1/6] Instalando dependencias desde requirements.txt..."
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --quiet

# 2. Ejecución de la cadena de procesamiento
# Nota: Pasamos las rutas como argumentos para que los scripts de Python sean flexibles

echo "[2/6] Cuantización: Convirtiendo respuestas de texto a números..."
python3 functions/cuantization.py data/encuesta.csv data/output/encuesta_procesada.csv

echo "[3/6] Agregación: Calculando variables MBI, UWES y NS..."
python3 functions/aggregator.py data/output/encuesta_procesada.csv data/output/encuesta_final.csv

echo "[4/6] Normalización: Escalando variables al intervalo [0, 1]..."
python3 functions/normalizer.py data/output/encuesta_final.csv data/output/encuesta_normalizada.csv

echo "[5/6] Categorización: Asignando etiquetas lingüísticas (Bajo, Medio, Alto)..."
python3 functions/categorizer.py data/output/encuesta_final.csv data/output/encuesta_categorias.csv

echo "[6/6] Feature Selection: Identificando el mejor trío con Random Forest..."
python3 functions/feature_selection.py data/output/encuesta_normalizada.csv

echo "--- Pipeline Finalizada con Éxito ---"
echo "Resultados disponibles en: data/output/"

deactivate
rm -rf .venv