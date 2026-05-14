import os
import matplotlib.pyplot as plt
from reglas import configurar_sistema_uwes_completo

def generar_graficas_individuales():
    # 1. Crear carpeta si no existe
    folder = "imagenes"
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Directorio '{folder}' creado.")

    # 2. Inicializar sistema
    simulador = configurar_sistema_uwes_completo()
    control_sys = simulador.ctrl
    
    # CORRECCIÓN: Convertir generadores a listas antes de sumar
    variables = list(control_sys.antecedents) + list(control_sys.consequents)
    
    print("Generando gráficas de funciones de pertenencia...")
    for var in variables:
        fig, ax = plt.subplots(figsize=(8, 5))
        
        # Visualizar la variable
        var.view(sim=simulador, ax=ax)
        
        ax.set_title(f"Funciones de Pertenencia: {var.label}", fontsize=14, fontweight='bold')
        ax.set_xlabel("Rango de Valores", fontsize=12)
        ax.set_ylabel("Grado de Pertenencia (μ)", fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.6)
        
        nombre_archivo = os.path.join(folder, f"pertenencia_{var.label.lower()}.png")
        plt.savefig(nombre_archivo, bbox_inches='tight', dpi=300)
        plt.close(fig)
        print(f" - [OK] Guardada: {nombre_archivo}")

if __name__ == "__main__":
    generar_graficas_individuales()