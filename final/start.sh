#!/bin/bash

# 1. Crear entorno virtual
python3 -m venv .venv

# 2. Activar entorno
source .venv/bin/activate

# 3. Actualizar herramientas base e instalar dependencias
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 4. Ejecutar el orquestador
python3 main.py

# 5. Desactivar y borrar el entorno
deactivate
rm -rf .venv

echo "Proceso finalizado y entorno virtual eliminado."