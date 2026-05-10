import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description='Calcula las 4 variables del UWES-9 y elimina las originales.')
    parser.add_argument('archivos', nargs='+', help='Archivos CSV (preferiblemente los que ya pasaron por calcular_mbi.py)')
    parser.add_argument('-o', '--output', default='valores_uwes_dataset.csv', help='Archivo de salida')
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

    # 2. Definir los grupos del UWES-9 para las 4 variables
    uwes_vitalidad = ['UWES_Energia', 'UWES_Fuerza']
    uwes_motivacion = ['UWES_Ilusion', 'UWES_Ganas_Manana']
    uwes_proposito = ['UWES_Inspiracion', 'UWES_Orgullo']
    uwes_inmersion = ['UWES_Feliz_Intensidad', 'UWES_Inmerso', 'UWES_Dejarse_Llevar']

# 3. Cálculos: Calcular la media directa de los valores ya normalizados (0 a 1).
    df['VALOR_Vitalidad'] = df[uwes_vitalidad].mean(axis=1).round(4)
    df['VALOR_Motivacion'] = df[uwes_motivacion].mean(axis=1).round(4)
    df['VALOR_Proposito'] = df[uwes_proposito].mean(axis=1).round(4)
    df['VALOR_Inmersion'] = df[uwes_inmersion].mean(axis=1).round(4)

    # 4. Eliminar las columnas de las preguntas individuales del UWES
    todas_preguntas_uwes = uwes_vitalidad + uwes_motivacion + uwes_proposito + uwes_inmersion
    columnas_a_borrar = [col for col in todas_preguntas_uwes if col in df.columns]
    df.drop(columns=columnas_a_borrar, inplace=True)

    # 5. Exportar
    df.to_csv(args.output, sep='\t', index=False, encoding='utf-8')
    print(f"Éxito: Procesados {len(args.archivos)} archivo(s). Valores guardados en {args.output}")

if __name__ == "__main__":
    main()