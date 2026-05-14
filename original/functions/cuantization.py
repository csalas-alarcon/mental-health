import pandas as pd
import sys

def normalize_survey(input_path, output_path):
    # Cargar la encuesta
    df = pd.read_csv(input_path)
    
    # 1. Diccionario para MBI (Escala 1 a 5 según vuestra memoria)
    # Referencia: "Como nuestras preguntas van del 1 al 5" [cite: 384]
    mbi_map = {
        "Nunca": 1,
        "Algunas veces al Año": 2,
        "Algunas veces al Mes": 3,
        "Algunas veces a la Semana": 4,
        "Diariamente": 5
    }

    # 2. Diccionario para UWES-9 (Escala 0 a 6 oficial)
    # Referencia: "desde 0 a 6, así que hemos podido agregar más casos" 
    uwes_map = {
        "Nunca": 0,
        "Algunas veces al Año": 1,
        "Una vez por Mes": 2,
        "Algunas veces al Mes": 3,
        "Una vez por Semana": 4,
        "Algunas veces a la Semana": 5,
        "Diariamente": 6
    }

    # Columnas 1 a 22: MBI (Se asume que la columna 0 es la marca temporal)
    # Referencia: "de las columnas 1 a 22 ahora van a tener los valores numéricos" [cite: 364]
    for col in df.columns[1:23]:
        df[col] = df[col].map(mbi_map)

    # Columnas 23 a 31: UWES-9
    for col in df.columns[23:32]:
        df[col] = df[col].map(uwes_map)

    # Columnas 32 a 36: Variables de contexto (ya vienen como números 0-10 en el Forms)
    # Solo nos aseguramos de que sean tipo numérico
    for col in df.columns[32:37]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Anonimización: Eliminamos la marca temporal si existe
    if 'Marca temporal' in df.columns:
        df = df.drop(columns=['Marca temporal'])

    df.to_csv(output_path, index=False, sep='\t')
    print(f"Cuantización completada en: {output_path}")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    normalize_survey(input_file, output_file)