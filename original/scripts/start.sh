#!/bin/bash

# Crear directorios para los resultados (CSVs y gráficos)
mkdir -p output images

echo "Iniciando entorno virtual..."
python -m venv .venv
source .venv/bin/activate

echo "Instalando dependencias..."
pip install -r requirements.txt

# 1. Generar datos simulados
echo "Generando datos simulados..."
python src/generation.py -o output/simulated.csv

# 2. Normalizar e integrar (usando form/RBI_FORM.csv si existe)
echo "Normalizando datos..."
if [ -f "form/RBI_FORM.csv" ]; then
    python src/normalization.py output/simulated.csv form/RBI_FORM.csv -o output/normalized.csv
else
    python src/normalization.py output/simulated.csv -o output/normalized.csv
fi

# 3. Calcular MBI
echo "Calculando MBI..."
python src/calcular_mbi.py output/normalized.csv -o output/mbi_calculated.csv

# 4. Calcular UWES
echo "Calculando UWES..."
python src/calcular_uwes.py output/mbi_calculated.csv -o output/uwes_calculated.csv

# 5. Relación/Predicción de variables propias
echo "Evaluando predictores..."
python src/relacion_burnout.py output/uwes_calculated.csv -p -o output/mejores_predictores.csv

# 6. Visualización
echo "Generando visualizaciones..."
python src/visualization.py output/mejores_predictores.csv

echo "Limpiando..."
deactivate
rm -rf .venv

echo "¡Proceso completado exitosamente! Los CSVs están en 'output/' y los gráficos en 'imgs/'."