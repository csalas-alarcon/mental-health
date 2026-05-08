#!/bin/bash

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
python generation.py
python normalization.py
python visualization.py

deactivate
rm -rf .venv