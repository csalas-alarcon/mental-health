import pandas as pd
import argparse
import itertools

def main():
    parser = argparse.ArgumentParser(description='Encuentra la mejor combinación de variables propias para predecir el Burnout.')
    parser.add_argument('archivo', help='Archivo CSV a leer')
    parser.add_argument('-p', '--print', action='store_true', help='Imprimir el ranking')
    parser.add_argument('-o', '--output', help='Nombre del archivo CSV de salida')
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.archivo, sep='\t')
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Hace la media directa de las variables ya normalizadas
    mbi_cols = ['VALOR_Cansancio_Emocional', 'VALOR_Despersonalizacion', 'VALOR_Realizacion_Personal']
    df['MBI_Media'] = df[mbi_cols].mean(axis=1)

    propias = ['NS_Tareas_Criticas', 'NS_Pantallas', 'NS_Sueno', 'NS_Pausas_Activas', 'NS_Entorno']
    propias_existentes = [col for col in propias if col in df.columns]
    
    if len(propias_existentes) < 2:
        print("No se encontraron suficientes variables 'NS_' en el archivo.")
        return

    pares = list(itertools.combinations(propias_existentes, 2))
    resultados = []

    for var1, var2 in pares:
        par_combinado = df[[var1, var2]].mean(axis=1)
        correlacion = par_combinado.corr(df['MBI_Media'])
        resultados.append({'Var1': var1, 'Var2': var2, 'Correlacion': round(correlacion, 4)})

    resultados = sorted(resultados, key=lambda x: abs(x['Correlacion']), reverse=True)
    mejor_par = resultados[0]

    if args.print:
        print("\n--- RANKING DE PREDICTORES (Correlación) ---")
        for i, res in enumerate(resultados, 1):
            print(f"{i}. {res['Var1']} + {res['Var2']} -> Correlación: {res['Correlacion']}")
        print("-" * 50)
        print(f"🏆 MEJOR COMBINACIÓN: {mejor_par['Var1']} y {mejor_par['Var2']}\n")

    if args.output:
        # Conservamos ID, Status, todas las variables calculadas (VALOR_), MBI_Media y el mejor par
        cols_valores = [col for col in df.columns if col.startswith('VALOR_')]
        columnas_salida = ['ID', 'Status'] + cols_valores + ['MBI_Media', mejor_par['Var1'], mejor_par['Var2']]
        
        df_salida = df[columnas_salida].copy()
        df_salida['MBI_Media'] = df_salida['MBI_Media'].round(3)
        df_salida.to_csv(args.output, sep='\t', index=False, encoding='utf-8')
        print(f"Archivo exportado con éxito: {args.output}")

if __name__ == "__main__":
    main()