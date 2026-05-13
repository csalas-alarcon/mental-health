import pandas as pd
import sys

def categorize_variables(input_path, output_path):
    df = pd.read_csv(input_path, sep='\t')
    df_cat = df.copy()

    # --- Lógica MBI (Método 2: Valores normalizados de 1 a 5) [cite: 412] ---
    def cat_mbi_ae(v):
        if v <= 21: return 'Bajo'
        if v <= 26: return 'Medio'
        return 'Alto'

    def cat_mbi_dp(v):
        if v <= 8: return 'Bajo'
        if v <= 11: return 'Medio'
        return 'Alto'

    def cat_mbi_rp(v):
        if v <= 30: return 'Bajo'
        if v <= 34: return 'Medio'
        return 'Alto'

    # --- Lógica UWES-9 (Puntajes normativos oficiales 0 a 6) [cite: 504] ---
    def cat_uwes_vigor(v):
        if v <= 2.00: return 'Muy bajo'
        if v <= 3.25: return 'Bajo'
        if v <= 4.80: return 'Medio'
        if v <= 5.65: return 'Alto'
        return 'Muy alto'

    def cat_uwes_dedic(v):
        if v <= 1.33: return 'Muy bajo'
        if v <= 2.90: return 'Bajo'
        if v <= 4.70: return 'Medio'
        if v <= 5.69: return 'Alto'
        return 'Muy alto'

    def cat_uwes_absor(v):
        if v <= 1.77: return 'Muy bajo'
        if v <= 2.33: return 'Bajo'
        if v <= 4.20: return 'Medio'
        if v <= 5.33: return 'Alto'
        return 'Muy alto'

    # Aplicar transformaciones
    df_cat['MBI_AE'] = df_cat['MBI_AE'].apply(cat_mbi_ae)
    df_cat['MBI_DP'] = df_cat['MBI_DP'].apply(cat_mbi_dp)
    df_cat['MBI_RP'] = df_cat['MBI_RP'].apply(cat_mbi_rp)
    
    df_cat['UWES_Vigor'] = df_cat['UWES_Vigor'].apply(cat_uwes_vigor)
    df_cat['UWES_Dedicacion'] = df_cat['UWES_Dedicacion'].apply(cat_uwes_dedic)
    df_cat['UWES_Absorcion'] = df_cat['UWES_Absorcion'].apply(cat_uwes_absor)
    
    # Guardado DENTRO de la función
    df_cat.to_csv(output_path, index=False, sep='\t')
    print(f"Categorización completada en: {output_path}")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    categorize_variables(input_file, output_file)