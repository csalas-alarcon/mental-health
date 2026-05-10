import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description='Calcula las 3 variables científicas del UWES-9 y elimina las originales.')
    parser.add_argument('archivos', nargs='+', help='Archivos CSV normalizados a procesar')
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

    # 2. Definir las 3 dimensiones oficiales según el estudio (UWES-9)
    # Vigor: Energía, Fuerza y Ganas por la mañana
    uwes_vigor = ['UWES_Energia', 'UWES_Fuerza', 'UWES_Ganas_Manana']
    
    # Dedicación: Ilusión (entusiasmo), Inspiración y Orgullo
    uwes_dedicacion = ['UWES_Ilusion', 'UWES_Inspiracion', 'UWES_Orgullo']
    
    # Absorción: Feliz intensidad, Inmerso y Dejarse llevar
    uwes_absorcion = ['UWES_Feliz_Intensidad', 'UWES_Inmerso', 'UWES_Dejarse_Llevar']

    # 3. Cálculo de la media directa (0 a 1)
    df['VALOR_Vigor'] = df[uwes_vigor].mean(axis=1).round(4)
    df['VALOR_Dedicacion'] = df[uwes_dedicacion].mean(axis=1).round(4)
    df['VALOR_Absorcion'] = df[uwes_absorcion].mean(axis=1).round(4)

    # 4. Eliminar las columnas de las preguntas individuales
    todas_preguntas_uwes = uwes_vigor + uwes_dedicacion + uwes_absorcion
    columnas_a_borrar = [col for col in todas_preguntas_uwes if col in df.columns]
    df.drop(columns=columnas_a_borrar, inplace=True)

    # 5. Exportar
    df.to_csv(args.output, sep='\t', index=False, encoding='utf-8')
    print(f"Éxito: Procesados {len(args.archivos)} archivo(s). Variables científicas (Vigor, Dedicación, Absorción) guardadas en {args.output}")

if __name__ == "__main__":
    main()