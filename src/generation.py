import pandas as pd
import numpy as np
import random
import argparse

def main():
    parser = argparse.ArgumentParser(description='Genera un dataset simulado de respuestas MBI/UWES.')
    parser.add_argument('-r', '--rows', type=int, default=83, help='Número total de filas')
    parser.add_argument('-b', '--burnout-ratio', type=float, default=0.15, help='Proporción de burnout (ej. 0.15)')
    parser.add_argument('-o', '--output', default='simulated_burnout_dataset.csv', help='Ruta del archivo de salida')
    args = parser.parse_args()

    burnout_count = int(args.rows * args.burnout_ratio)
    mbi_options = ["Nunca", "Algunas veces al Año", "Algunas veces al Mes", "Algunas veces a la Semana", "Diariamente"]
    uwes_options = ["Nunca", "Algunas veces al Año", "Una vez por Mes", "Algunas veces al Mes", "Una vez por Semana", "Algunas veces a la Semana", "Diariamente"]

    questions = [
        {"col": "MBI_Defraudado", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Agotamiento_Jornada", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Agotamiento_Manana", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Comprension_Facil", "worst": [mbi_options[0]], "med": mbi_options[1:4], "best": [mbi_options[4]]},
        {"col": "MBI_Despersonalizacion", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Cansancio_Gente", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Efectividad_Problemas", "worst": [mbi_options[0]], "med": mbi_options[1:4], "best": [mbi_options[4]]},
        {"col": "MBI_Desgaste", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Influencia_Positiva", "worst": [mbi_options[0]], "med": mbi_options[1:4], "best": [mbi_options[4]]},
        {"col": "MBI_Endurecimiento", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Preocupacion_Endurecimiento", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Energico", "worst": [mbi_options[0]], "med": mbi_options[1:4], "best": [mbi_options[4]]},
        {"col": "MBI_Frustracion", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Demasiado_Tiempo", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Indiferencia", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Cansancio_Contacto", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Clima_Agradable", "worst": [mbi_options[0]], "med": mbi_options[1:4], "best": [mbi_options[4]]},
        {"col": "MBI_Estimulo_Atencion", "worst": [mbi_options[0]], "med": mbi_options[1:4], "best": [mbi_options[4]]},
        {"col": "MBI_Cosas_Valiosas", "worst": [mbi_options[0]], "med": mbi_options[1:4], "best": [mbi_options[4]]},
        {"col": "MBI_Limite_Posibilidades", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        {"col": "MBI_Trato_Emocional", "worst": [mbi_options[0]], "med": mbi_options[1:4], "best": [mbi_options[4]]},
        {"col": "MBI_Culpa_Beneficiarios", "worst": [mbi_options[4]], "med": mbi_options[1:4], "best": [mbi_options[0]]},
        
        {"col": "UWES_Energia", "worst": [uwes_options[0]], "med": uwes_options[1:6], "best": [uwes_options[6]]},
        {"col": "UWES_Fuerza", "worst": [uwes_options[0]], "med": uwes_options[1:6], "best": [uwes_options[6]]},
        {"col": "UWES_Ilusion", "worst": [uwes_options[0]], "med": uwes_options[1:6], "best": [uwes_options[6]]},
        {"col": "UWES_Inspiracion", "worst": [uwes_options[0]], "med": uwes_options[1:6], "best": [uwes_options[6]]},
        {"col": "UWES_Ganas_Manana", "worst": [uwes_options[0]], "med": uwes_options[1:6], "best": [uwes_options[6]]},
        {"col": "UWES_Feliz_Intensidad", "worst": [uwes_options[0]], "med": uwes_options[1:6], "best": [uwes_options[6]]},
        {"col": "UWES_Orgullo", "worst": [uwes_options[0]], "med": uwes_options[1:6], "best": [uwes_options[6]]},
        {"col": "UWES_Inmerso", "worst": [uwes_options[0]], "med": uwes_options[1:6], "best": [uwes_options[6]]},
        {"col": "UWES_Dejarse_Llevar", "worst": [uwes_options[0]], "med": uwes_options[1:6], "best": [uwes_options[6]]},
        
        {"col": "NS_Tareas_Criticas", "worst": ["Crítica"], "med": ["Manejable", "Saturada"], "best": ["Baja"]},
        {"col": "NS_Pantallas", "worst": ["Excesiva (>10h)"], "med": ["Estándar (5-8h)"], "best": ["Reducida (<4h)"]},
        {"col": "NS_Sueno", "worst": ["Insuficiente"], "med": ["Pobre", "Aceptable"], "best": ["Excelente y Reparador"]},
        {"col": "NS_Pausas_Activas", "worst": ["Nulas"], "med": ["Esporádicas"], "best": ["Frecuentes"]},
        {"col": "NS_Entorno", "worst": ["Hostil"], "med": ["Neutro Colaborativo"], "best": ["Colaborativo"]}
    ]

    data = []
    for i in range(args.rows):
        status = "Burnout" if i < burnout_count else "Healthy"
        probs = [0.60, 0.30, 0.10] if status == "Burnout" else [0.10, 0.50, 0.40]
        row = {"ID": i + 1, "Status": status}
        for item in questions:
            choice_category = np.random.choice(["worst", "med", "best"], p=probs)
            row[item["col"]] = random.choice(item[choice_category])
        data.append(row)

    df = pd.DataFrame(data)
    df.to_csv(args.output, sep='\t', index=False, encoding='utf-8')
    print(f"Generado dataset en {args.output}")

if __name__ == "__main__":
    main()