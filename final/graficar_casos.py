import os
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz

from reglas import configurar_sistema_uwes_completo


def graficar_ejemplo_especifico(nombre, v, d, a, t, p, e):

    folder = "imagenes"
    os.makedirs(folder, exist_ok=True)

    simulador = configurar_sistema_uwes_completo()

    # ---------------------------
    # Entradas
    # ---------------------------
    simulador.input['Vig'] = v
    simulador.input['Ded'] = d
    simulador.input['Abs'] = a
    simulador.input['tareas'] = t
    simulador.input['pausas'] = p
    simulador.input['entorno'] = e

    simulador.compute()

    resultado = simulador.output['burnout']

    burnout_var = list(simulador.ctrl.consequents)[0]

    x = burnout_var.universe

    bajo = burnout_var['bajo'].mf
    medio = burnout_var['medio'].mf
    alto = burnout_var['alto'].mf

    # ---------------------------
    # Membresías
    # ---------------------------
    p_bajo = fuzz.interp_membership(x, bajo, resultado)
    p_medio = fuzz.interp_membership(x, medio, resultado)
    p_alto = fuzz.interp_membership(x, alto, resultado)

    # ---------------------------
    # FIGURA
    # ---------------------------
    fig, (ax_plot, ax_table) = plt.subplots(
        1,
        2,
        figsize=(15, 6),
        gridspec_kw={'width_ratios': [3, 1.2]},
        constrained_layout=True
    )

    # =========================================================
    # SUBPLOT 1 -> GRÁFICO DIFUSO
    # =========================================================

    # Colores modernos
    c_bajo = "#2ecc71"
    c_medio = "#f39c12"
    c_alto = "#e74c3c"

    # Curvas
    ax_plot.plot(x, bajo, color=c_bajo, linewidth=2.5, label='Bajo')
    ax_plot.plot(x, medio, color=c_medio, linewidth=2.5, label='Medio')
    ax_plot.plot(x, alto, color=c_alto, linewidth=2.5, label='Alto')

    # Rellenos
    ax_plot.fill_between(x, 0, bajo, color=c_bajo, alpha=0.25)
    ax_plot.fill_between(x, 0, medio, color=c_medio, alpha=0.25)
    ax_plot.fill_between(x, 0, alto, color=c_alto, alpha=0.25)

    # Resultado como línea moderna
    ax_plot.axvline(
        resultado,
        color="#34495e",
        linewidth=3,
        linestyle='--',
        alpha=0.9,
        label=f'Resultado: {resultado:.2f}'
    )

    # Punto destacado
    ax_plot.scatter(
        resultado,
        max(p_bajo, p_medio, p_alto),
        s=140,
        color="#2c3e50",
        zorder=10
    )

    # Estética
    ax_plot.set_title(
        f"Análisis Difuso: {nombre}",
        fontsize=16,
        fontweight='bold'
    )

    ax_plot.set_xlabel(
        "Riesgo de Burnout (0 - 10)",
        fontsize=12
    )

    ax_plot.set_ylabel(
        "Grado de pertenencia (μ)",
        fontsize=12
    )

    ax_plot.set_ylim(0, 1.05)

    ax_plot.grid(
        alpha=0.25,
        linestyle='--'
    )

    ax_plot.spines['top'].set_visible(False)
    ax_plot.spines['right'].set_visible(False)

    ax_plot.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.12),
        ncol=4,
        frameon=False
    )

    # =========================================================
    # SUBPLOT 2 -> TABLA
    # =========================================================

    ax_table.axis('off')

    columnas = ["Métrica", "Valor"]

    datos = [
        ["Índice Burnout", f"{resultado:.3f}"],
        ["μ Bajo", f"{p_bajo:.3f}"],
        ["μ Medio", f"{p_medio:.3f}"],
        ["μ Alto", f"{p_alto:.3f}"]
    ]

    tabla = ax_table.table(
        cellText=datos,
        colLabels=columnas,
        cellLoc='center',
        loc='center'
    )

    # Tamaño tabla
    tabla.scale(1.2, 2)

    # Estilos
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(11)

    for (row, col), cell in tabla.get_celld().items():

        cell.set_edgecolor("#dcdcdc")
        cell.set_linewidth(1)

        # Header
        if row == 0:
            cell.set_facecolor("#34495e")
            cell.set_text_props(color='white', weight='bold')

        else:

            # Alternar colores
            if row % 2 == 0:
                cell.set_facecolor("#f8f9fa")
            else:
                cell.set_facecolor("#ffffff")

            # Resaltar resultado
            if row == 1:
                cell.set_text_props(
                    color="#c0392b",
                    weight='bold'
                )

    ax_table.set_title(
        "Resumen",
        fontsize=14,
        fontweight='bold',
        pad=15
    )

    # =========================================================
    # GUARDAR
    # =========================================================

    nombre_archivo = os.path.join(
        folder,
        f"ejemplo_inferencia_{nombre.lower().replace(' ', '_')}.png"
    )

    plt.savefig(
        nombre_archivo,
        dpi=300,
        bbox_inches='tight'
    )

    plt.close()

    print(f"[OK] Caso '{nombre}' guardado.")


if __name__ == "__main__":

    print("Generando gráficas...")

    graficar_ejemplo_especifico(
        "Empleado Saludable",
        6.0, 6.0, 6.0,
        5.0, 10.0, 10.0
    )

    graficar_ejemplo_especifico(    
        "Riesgo Significativo - Agotamiento Crítico",
        0.5,  # Vigor: Casi inexistente
        2.0,  # Dedicación: Muy baja
        2.0,  # Absorción: Baja
        9.0,  # Tareas: Nivel Crítico (Escala 0-10)
        2.0,  # Pausas: Esporádicas/Nulas
        3.0   # Entorno: Hostil (Escala 0-10)
    )

    graficar_ejemplo_especifico(
        "Caso en Observacion",
        2.33, 3.67, 3.67,
        5.0, 5.0, 10.0
    )