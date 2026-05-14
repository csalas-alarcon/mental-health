import pandas as pd
import argparse
import itertools

def main():
    parser = argparse.ArgumentParser(description='Encuentra la mejor combinación de 3 variables propias para predecir el Burnout.')
    parser.add_argument('archivo', help='Archivo CSV a leer')
    parser.add_argument('-p', '--print', action='store_true', help='Imprimir el ranking')
    parser.add_argument('-o', '--output', help='Nombre del archivo CSV de salida')
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.archivo, sep='\t')
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Comprobar que las columnas del MBI calculadas existen
    mbi_cols = ['VALOR_Cansancio_Emocional', 'VALOR_Despersonalizacion', 'VALOR_Realizacion_Personal']
    if not all(col in df.columns for col in mbi_cols):
        print("Error: No se encuentran las variables VALOR_ del MBI en el archivo.")
        return

    # Hace la media directa de las variables MBI ya normalizadas
    df['MBI_Media'] = df[mbi_cols].mean(axis=1)

    propias = ['NS_Tareas_Criticas', 'NS_Pantallas', 'NS_Sueno', 'NS_Pausas_Activas', 'NS_Entorno']
    propias_existentes = [col for col in propias if col in df.columns]
    
    if len(propias_existentes) < 3:
        print("No se encontraron suficientes variables 'NS_' en el archivo (mínimo 3).")
        return

    # Generar todas las combinaciones de 3 variables
    trios = list(itertools.combinations(propias_existentes, 3))
    resultados = []

    for var1, var2, var3 in trios:
        trio_combinado = df[[var1, var2, var3]].mean(axis=1)
        correlacion = trio_combinado.corr(df['MBI_Media'])
        resultados.append({'Var1': var1, 'Var2': var2, 'Var3': var3, 'Correlacion': round(correlacion, 4)})

    # Ordenar por el valor absoluto de la correlación (la más fuerte primero)
    resultados = sorted(resultados, key=lambda x: abs(x['Correlacion']), reverse=True)
    mejor_trio = resultados[0]

    if args.print:
        print("\n--- RANKING DE PREDICTORES (Correlación de Pearson) ---")
        for i, res in enumerate(resultados, 1):
            print(f"{i}. {res['Var1']} + {res['Var2']} + {res['Var3']} -> Correlación: {res['Correlacion']}")
        print("-" * 75)
        print(f"MEJOR COMBINACIÓN: {mejor_trio['Var1']}, {mejor_trio['Var2']} y {mejor_trio['Var3']}\n")

    if args.output:
        # Conservamos ID, Status, todas las variables calculadas (VALOR_), MBI_Media y el mejor trío
        cols_valores = [col for col in df.columns if col.startswith('VALOR_')]
        columnas_salida = ['ID', 'Status'] + cols_valores + ['MBI_Media', mejor_trio['Var1'], mejor_trio['Var2'], mejor_trio['Var3']]
        
        df_salida = df[columnas_salida].copy()
        df_salida['MBI_Media'] = df_salida['MBI_Media'].round(3)
        df_salida.to_csv(args.output, sep='\t', index=False, encoding='utf-8')
        print(f"Archivo exportado con éxito: {args.output}")

if __name__ == "__main__":
    main()