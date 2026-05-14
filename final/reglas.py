import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def configurar_sistema_uwes_completo():
    # 1. Definición de universos
    vigor = ctrl.Antecedent(np.arange(0, 7), 'Vig')
    dedicacion = ctrl.Antecedent(np.arange(0, 7), 'Ded')
    absorcion = ctrl.Antecedent(np.arange(0, 7), 'Abs')
    
    tareas = ctrl.Antecedent(np.arange(0, 11), 'tareas')
    pausas = ctrl.Antecedent(np.arange(0, 11), 'pausas')
    entorno = ctrl.Antecedent(np.arange(0, 11), 'entorno')

    burnout = ctrl.Consequent(np.arange(0, 11), 'burnout')

    # 2. Funciones de Pertenencia (UNIFICADAS)
    # Importante: Usamos 'medio' para evitar el error de 'media'
    for var in [vigor, dedicacion, absorcion]:
        var['muy_bajo'] = fuzz.trapmf(var.universe, [0, 0, 1.5, 2])
        var['bajo']     = fuzz.trapmf(var.universe, [1.7, 2.3, 2.7, 3.25])
        var['medio']    = fuzz.trapmf(var.universe, [2.95, 3.7, 4.3, 4.8]) # <--- UNIFICADO
        var['alto']     = fuzz.trapmf(var.universe, [4.5, 4.8, 5.2, 5.65])
        var['muy_alto'] = fuzz.trapmf(var.universe, [5.4, 5.7, 6, 6])

    # Variables Ambientales
    tareas['bajas']      = fuzz.trapmf(tareas.universe, [0, 0, 2, 4])
    tareas['manejables']  = fuzz.trimf(tareas.universe, [3, 5, 7])
    tareas['saturadas']   = fuzz.trimf(tareas.universe, [6, 8, 9])
    tareas['criticas']    = fuzz.trapmf(tareas.universe, [8, 9, 10, 10])

    pausas['nulas']       = fuzz.trapmf(pausas.universe, [0, 0, 1, 3])
    pausas['esporadicas'] = fuzz.trimf(pausas.universe, [2, 5, 8])
    pausas['frecuentes']  = fuzz.trapmf(pausas.universe, [7, 9, 10, 10])

    entorno['hostil']       = fuzz.trapmf(entorno.universe, [0, 0, 2, 4])
    entorno['neutro']       = fuzz.trimf(entorno.universe, [3, 5, 7])
    entorno['colaborativo'] = fuzz.trapmf(entorno.universe, [6, 8, 10, 10])

    # Salida
    burnout['bajo']  = fuzz.trapmf(burnout.universe, [0, 0, 2, 4])
    burnout['medio'] = fuzz.trapmf(burnout.universe, [3, 5, 5, 7])
    burnout['alto']  = fuzz.trapmf(burnout.universe, [6, 8, 10, 10])

    # 3. Reglas (Corregidas para usar 'medio')
    rules = [
        # Entorno
        ctrl.Rule(entorno['colaborativo'] & (dedicacion['muy_alto'] | dedicacion['alto']), burnout['bajo']),
        ctrl.Rule(entorno['colaborativo'] & dedicacion['medio'], burnout['medio']),
        ctrl.Rule(entorno['hostil'] & (dedicacion['muy_bajo'] | dedicacion['bajo'] | dedicacion['medio']), burnout['alto']),
        ctrl.Rule(entorno['neutro'] & dedicacion['medio'], burnout['medio']),
        ctrl.Rule(entorno['neutro'] & (dedicacion['muy_bajo'] | dedicacion['bajo']), burnout['alto']),

        # Tareas
        ctrl.Rule(tareas['bajas'] & (dedicacion['muy_alto'] | dedicacion['alto'] | dedicacion['medio']), burnout['bajo']),
        ctrl.Rule(tareas['bajas'] & (dedicacion['bajo'] | dedicacion['muy_bajo']), burnout['medio']),
        ctrl.Rule(tareas['manejables'] & (dedicacion['muy_alto'] | dedicacion['alto']), burnout['bajo']),
        ctrl.Rule(tareas['manejables'] & (dedicacion['medio'] | dedicacion['bajo'] | dedicacion['muy_bajo']), burnout['medio']),
        ctrl.Rule(tareas['saturadas'] & (dedicacion['muy_bajo'] | dedicacion['bajo']), burnout['alto']),
        ctrl.Rule(tareas['saturadas'] & dedicacion['medio'], burnout['medio']),
        ctrl.Rule(tareas['criticas'] & (dedicacion['muy_bajo'] | dedicacion['bajo'] | dedicacion['medio']), burnout['alto']),

        # Vigor (Repetir corrección 'medio')
        ctrl.Rule(entorno['colaborativo'] & (vigor['muy_alto'] | vigor['alto']), burnout['bajo']),
        ctrl.Rule(entorno['colaborativo'] & vigor['medio'], burnout['medio']),
        ctrl.Rule(entorno['hostil'] & (vigor['muy_bajo'] | vigor['bajo'] | vigor['medio']), burnout['alto']),
        ctrl.Rule(entorno['neutro'] & vigor['medio'], burnout['medio']),
        ctrl.Rule(entorno['neutro'] & (vigor['muy_bajo'] | vigor['bajo']), burnout['alto']),
        ctrl.Rule(tareas['bajas'] & (vigor['muy_alto'] | vigor['alto'] | vigor['medio']), burnout['bajo']),
        ctrl.Rule(tareas['bajas'] & (vigor['bajo'] | vigor['muy_bajo']), burnout['medio']),
        ctrl.Rule(tareas['manejables'] & (vigor['muy_alto'] | vigor['alto']), burnout['bajo']),
        ctrl.Rule(tareas['manejables'] & (vigor['medio'] | vigor['bajo'] | vigor['muy_bajo']), burnout['medio']),
        ctrl.Rule(tareas['saturadas'] & (vigor['muy_bajo'] | vigor['bajo']), burnout['alto']),
        ctrl.Rule(tareas['saturadas'] & vigor['medio'], burnout['medio']),
        ctrl.Rule(tareas['criticas'] & (vigor['muy_bajo'] | vigor['bajo'] | vigor['medio']), burnout['alto']),

        # Complejas
        ctrl.Rule(dedicacion['alto'] & tareas['saturadas'] & (absorcion['muy_alto'] | absorcion['alto']), burnout['bajo']),
        ctrl.Rule(dedicacion['alto'] & tareas['saturadas'] & (absorcion['medio'] | absorcion['bajo'] | absorcion['muy_bajo']), burnout['medio']),
        ctrl.Rule(dedicacion['alto'] & tareas['saturadas'] & (pausas['esporadicas'] | pausas['frecuentes']), burnout['bajo']),
        ctrl.Rule(dedicacion['alto'] & tareas['saturadas'] & pausas['nulas'], burnout['medio']),
        
        ctrl.Rule(dedicacion['muy_alto'] & tareas['criticas'] & (absorcion['muy_alto'] | absorcion['alto']), burnout['bajo']),
        ctrl.Rule(dedicacion['muy_alto'] & tareas['criticas'] & (absorcion['medio'] | absorcion['bajo'] | absorcion['muy_bajo']), burnout['medio']),
        ctrl.Rule(dedicacion['muy_alto'] & tareas['criticas'] & (pausas['esporadicas'] | pausas['frecuentes']), burnout['bajo']),
        ctrl.Rule(dedicacion['muy_alto'] & tareas['criticas'] & pausas['nulas'], burnout['medio']),

        # --- REGLAS DE SEGURIDAD (Para evitar errores en casos extremos) ---
        # Si el vigor y la dedicación son muy bajos, el burnout tiende a ser alto
        ctrl.Rule(vigor['muy_bajo'] | dedicacion['muy_bajo'], burnout['alto']),
        
        # Si el vigor y la dedicación son muy altos, el burnout tiende a ser bajo
        ctrl.Rule(vigor['muy_alto'] | dedicacion['muy_alto'], burnout['bajo']),
        
        # Regla comodín para cubrir cualquier hueco intermedio
        ctrl.Rule(vigor['medio'] | dedicacion['medio'] | absorcion['medio'], burnout['medio'])
    ]

    burnout_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(burnout_ctrl)

def ejecutar_inferencia_uwes(v_val, d_val, a_val, t_val, p_val, e_val):
    sim = configurar_sistema_uwes_completo()
    sim.input['Vig'] = v_val
    sim.input['Ded'] = d_val
    sim.input['Abs'] = a_val
    sim.input['tareas'] = t_val
    sim.input['pausas'] = p_val
    sim.input['entorno'] = e_val
    sim.compute()
    return sim.output['burnout']