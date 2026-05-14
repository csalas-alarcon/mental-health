# difusa.py

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def obtener_sistema_burnout():
    # 1. Definición de variables de entrada y salida
    AE = ctrl.Antecedent(np.arange(9, 46), 'AE')
    DP = ctrl.Antecedent(np.arange(5, 26), 'DP')
    RP = ctrl.Antecedent(np.arange(8, 41), 'RP')
    burnout = ctrl.Consequent(np.arange(0, 11), 'burnout')

    # 2. Funciones de pertenencia (Trapecios)
    AE['bajo']  = fuzz.trapmf(AE.universe, [9,  9,  17, 22])
    AE['medio'] = fuzz.trapmf(AE.universe, [20, 25, 30, 35])
    AE['alto']  = fuzz.trapmf(AE.universe, [34, 39, 45, 45])

    DP['bajo']  = fuzz.trapmf(DP.universe, [5, 5, 6, 8])
    DP['medio'] = fuzz.trapmf(DP.universe, [7, 10, 13, 16])
    DP['alto']  = fuzz.trapmf(DP.universe, [15, 19, 25, 25])

    RP['bajo']  = fuzz.trapmf(RP.universe, [8, 8, 14, 28])
    RP['medio'] = fuzz.trapmf(RP.universe, [26, 29, 33, 36])
    RP['alto']  = fuzz.trapmf(RP.universe, [35, 37, 40, 40])

    burnout['bajo']  = fuzz.trapmf(burnout.universe, [0, 0, 2, 4])
    burnout['medio'] = fuzz.trapmf(burnout.universe, [3, 5, 5, 7])
    burnout['alto']  = fuzz.trapmf(burnout.universe, [6, 8, 10, 10])

    # 3. Definición de Reglas
    rule1 = ctrl.Rule(AE['alto'] & DP['alto'] & RP['bajo'], burnout['alto'])
    rule2 = ctrl.Rule(AE['bajo'] & DP['bajo'] & RP['alto'], burnout['bajo'])
    rule3 = ctrl.Rule(AE['medio'] | DP['medio'] | RP['medio'], burnout['medio'])
    rule4 = ctrl.Rule(AE['alto'] & DP['bajo'], burnout['medio'])
    rule5 = ctrl.Rule(RP['alto'] & AE['alto'], burnout['medio'])
    rule6 = ctrl.Rule(AE['bajo'] & DP['alto'], burnout['medio'])
    rule7 = ctrl.Rule(RP['bajo'] & AE['bajo'], burnout['medio'])
    rule8 = ctrl.Rule(AE['alto'] & RP['bajo'], burnout['alto'])
    rule9 = ctrl.Rule(DP['alto'] & RP['bajo'], burnout['alto'])

    # 4. Sistema de control y simulación
    burnout_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    return ctrl.ControlSystemSimulation(burnout_ctrl)

def calcular_burnout_individual():
    simulador = obtener_sistema_burnout()
    
    simulador.input['AE'] = int(input('Agotamiento emocional (9-45): '))
    simulador.input['DP'] = int(input('Despersonalización (5-25): '))
    simulador.input['RP'] = int(input('Realización personal (8-40): '))
    
    simulador.compute()
    print('Resultado Burnout (0-10):', round(simulador.output['burnout'], 2))

if __name__ == "__main__":
    calcular_burnout_individual()