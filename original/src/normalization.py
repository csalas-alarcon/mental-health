import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description='Normaliza datasets de Burnout.')
    parser.add_argument('archivos', nargs='+', help='Archivos CSV a procesar')
    parser.add_argument('-o', '--output', default='normalized_burnout_dataset.csv', help='Salida')
    args = parser.parse_args()

    column_mapping = {
        '1. (MBI) Me siento emocionalmente defraudado en mi trabajo.': 'MBI_Defraudado',
        '2. (MBI) Cuando termino mi jornada de trabajo me siento agotado.': 'MBI_Agotamiento_Jornada',
        '3. (MBI) Cuando me levanto por la mañana y me enfrento a otra jornada de trabajo me siento agotado.': 'MBI_Agotamiento_Manana',
        '4. (MBI) Siento que puedo entender fácilmente a las personas que tengo que atender.': 'MBI_Comprension_Facil',
        '5. (MBI) Siento que estoy tratando a algunos beneficiados de mí, como si fuesen objetos \nimpersonales.': 'MBI_Despersonalizacion',
        '6. (MBI) Siento que trabajar todo el día con la gente me cansa.': 'MBI_Cansancio_Gente',
        '7. (MBI) Siento que trato con mucha efectividad los problemas de las personas a las que tengo que atender.': 'MBI_Efectividad_Problemas',
        '8. (MBI) Siento que mi trabajo me está desgastando.': 'MBI_Desgaste',
        '9. (MBI) Siento que estoy influyendo positivamente en las vidas de otras personas a través \nde mi trabajo.': 'MBI_Influencia_Positiva',
        '10. (MBI) Siento que me he hecho más duro con la gente.': 'MBI_Endurecimiento',
        '11. (MBI) Me preocupa que este trabajo me está endureciendo emocionalmente.': 'MBI_Preocupacion_Endurecimiento',
        '12. (MBI) Me siento muy enérgico en mi trabajo.': 'MBI_Energico',
        '13. (MBI) Me siento frustrado por el trabajo.': 'MBI_Frustracion',
        '14. (MBI) Siento que estoy demasiado tiempo en mi trabajo.': 'MBI_Demasiado_Tiempo',
        '15. (MBI) Siento que realmente no me importa lo que les ocurra a las personas a las que tengo que atender profesionalmente.': 'MBI_Indiferencia',
        '16. (MBI) Siento que trabajar en contacto directo con la gente me cansa.': 'MBI_Cansancio_Contacto',
        '17. (MBI) Siento que puedo crear con facilidad un clima agradable en mi trabajo.': 'MBI_Clima_Agradable',
        '18. (MBI) Me siento estimulado después de haber trabajado íntimamente con quienes tengo que atender.': 'MBI_Estimulo_Atencion',
        '19. (MBI) Creo que consigo muchas cosas valiosas en este trabajo.': 'MBI_Cosas_Valiosas',
        ' 20. (MBI) Me siento como si estuviera al límite de mis posibilidades.': 'MBI_Limite_Posibilidades',
        '21. (MBI) Siento que en mi trabajo los problemas emocionales son tratados de forma adecuada.': 'MBI_Trato_Emocional',
        '22. (MBI) Me parece que los beneficiarios de mi trabajo me culpan de algunos problemas.': 'MBI_Culpa_Beneficiarios',
        '23. (UWES-9) En mi trabajo me siento lleno de energía.': 'UWES_Energia',
        '24. (UWES-9) Me siento con fuerza en mi trabajo.': 'UWES_Fuerza',
        '25. (UWES-9) Estoy ilusionado con mi trabajo.': 'UWES_Ilusion',
        '26. (UWES-9) Mi trabajo me inspira.': 'UWES_Inspiracion',
        '27. (UWES-9) Cuando me levanto por las mañanas tengo ganas de ir a trabajar.': 'UWES_Ganas_Manana',
        '28. (UWES-9) Estoy feliz cuando trabajo con intensidad.': 'UWES_Feliz_Intensidad',
        '29. (UWES-9) Estoy orgulloso de lo que hago.': 'UWES_Orgullo',
        '30. (UWES-9) Estoy inmerso en mi trabajo.': 'UWES_Inmerso',
        '31. (UWES-9) Me dejo llevar por el trabajo.': 'UWES_Dejarse_Llevar',
        '32. ¿Cuantas tareas críticas manejas simultaneamente?': 'NS_Tareas_Criticas',
        '33. ¿Que exposición a las pantallas tienes en el trabajo?': 'NS_Pantallas',
        '34. ¿Como describiría su sueño?': 'NS_Sueno',
        '35. ¿Dispones de Pausas Activas en el Trabajo?': 'NS_Pausas_Activas',
        '36. ¿Como describirías tu Entorno de Trabajo?': 'NS_Entorno'
    }

    dataframes = []
    for archivo in args.archivos:
        try:
            # Intentar leer asumiendo CSV estándar (comas) primero
            df_temp = pd.read_csv(archivo, sep=',')
            # Si solo saca 1 columna, es que estaba separado por tabulaciones (el simulado)
            if len(df_temp.columns) < 10:
                df_temp = pd.read_csv(archivo, sep='\t')
                
            df_temp.rename(columns=column_mapping, inplace=True)
            
            if 'Status' not in df_temp.columns:
                df_temp['Status'] = 'Healthy'
                
            dataframes.append(df_temp)
        except Exception as e:
            print(f"Error en {archivo}: {e}")

    if not dataframes:
        return

    df = pd.concat(dataframes, ignore_index=True)

    df['ID'] = range(1, len(df) + 1)
    columnas_utiles = ['ID', 'Status'] + list(column_mapping.values())
    df = df[[col for col in columnas_utiles if col in df.columns]]

    mbi_map = {"Nunca": 0, "Algunas veces al Año": 1, "Algunas veces al Mes": 2, "Algunas veces a la Semana": 3, "Diariamente": 4}
    mbi_inversas = ["MBI_Comprension_Facil", "MBI_Efectividad_Problemas", "MBI_Influencia_Positiva", "MBI_Energico", "MBI_Clima_Agradable", "MBI_Estimulo_Atencion", "MBI_Cosas_Valiosas", "MBI_Trato_Emocional"]
    uwes_map_invertido = {"Nunca": 6, "Algunas veces al Año": 5, "Una vez por Mes": 4, "Algunas veces al Mes": 3, "Una vez por Semana": 2, "Algunas veces a la Semana": 1, "Diariamente": 0}
    
    ns_maps = {
        "NS_Tareas_Criticas": {"Baja": 0, "Manejable": 1, "Saturada": 2, "Crítica": 3},
        "NS_Pantallas": {"Reducida (<4h)": 0, "Estándar (5-8h)": 1, "Excesiva (>10h)": 2},
        "NS_Sueno": {"Insuficiente": 3, "Pobre": 2, "Aceptable": 1, "Excelente y Reparador": 0},
        "NS_Pausas_Activas": {"Nulas": 2, "Esporádicas": 1, "Frecuentes": 0},
        "NS_Entorno": {"Hostil": 2, "Neutro Colaborativo": 1, "Colaborativo": 0}
    }

    for col in df.columns:
        if col in mbi_inversas:
            df[col] = (4 - df[col].map(mbi_map)) / 4.0
        elif col.startswith("MBI_"):
            df[col] = df[col].map(mbi_map) / 4.0
        elif col.startswith("UWES_"):
            df[col] = df[col].map(uwes_map_invertido) / 6.0
        elif col in ns_maps:
            mapping = ns_maps[col]
            df[col] = df[col].map(mapping) / max(mapping.values())

    df.to_csv(args.output, sep='\t', index=False, encoding='utf-8')
    print(f"Éxito: Guardado en {args.output}")

if __name__ == "__main__":
    main()