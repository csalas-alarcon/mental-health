import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description='Calcula variables MBI (solo medias) y elimina las preguntas originales.')
    parser.add_argument('archivos', nargs='+', help='Archivos CSV normalizados a procesar')
    parser.add_argument('-o', '--output', default='valores_mbi_dataset.csv', help='Archivo de salida')
    args = parser.parse_args()

    # 1. Cargar y combinar archivos
    dataframes = []
    for archivo in args.archivos:
        try:
            df_temp = pd.read_csv(archivo, sep='\t')
            dataframes.append(df_temp)
        except Exception as e:
            print(f"Error procesando {archivo}: {e}")

    if not dataframes:
        print("No hay datos para procesar.")
        return

    df = pd.concat(dataframes, ignore_index=True)

    # 2. Forzar el status a "Sano" por defecto
    df['Status'] = 'Sano'

    # 3. Definir los grupos del MBI
    mbi_agotamiento = [
        'MBI_Defraudado', 'MBI_Agotamiento_Jornada', 'MBI_Agotamiento_Manana', 
        'MBI_Cansancio_Gente', 'MBI_Desgaste', 'MBI_Frustracion', 
        'MBI_Demasiado_Tiempo', 'MBI_Cansancio_Contacto', 'MBI_Limite_Posibilidades'
    ]

    mbi_despersonalizacion = [
        'MBI_Despersonalizacion', 'MBI_Endurecimiento', 'MBI_Preocupacion_Endurecimiento', 
        'MBI_Indiferencia', 'MBI_Culpa_Beneficiarios'
    ]

    mbi_realizacion = [
        'MBI_Comprension_Facil', 'MBI_Efectividad_Problemas', 'MBI_Influencia_Positiva', 
        'MBI_Energico', 'MBI_Clima_Agradable', 'MBI_Estimulo_Atencion', 
        'MBI_Cosas_Valiosas', 'MBI_Trato_Emocional'
    ]

    # 4. MEDIA DIRECTA. Sin multiplicar por nada.
    df['VALOR_Cansancio_Emocional'] = df[mbi_agotamiento].mean(axis=1).round(4)
    df['VALOR_Despersonalizacion'] = df[mbi_despersonalizacion].mean(axis=1).round(4)
    df['VALOR_Realizacion_Personal'] = df[mbi_realizacion].mean(axis=1).round(4)

    # 5. Eliminar las columnas de las preguntas individuales del MBI
    todas_preguntas_mbi = mbi_agotamiento + mbi_despersonalizacion + mbi_realizacion
    columnas_a_borrar = [col for col in todas_preguntas_mbi if col in df.columns]
    df.drop(columns=columnas_a_borrar, inplace=True)

    # 6. Exportar
    df.to_csv(args.output, sep='\t', index=False, encoding='utf-8')
    print(f"Éxito: Procesados {len(args.archivos)} archivo(s). Valores guardados en {args.output}")

if __name__ == "__main__":
    main()