import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint

# Définition des symboles
t = sp.symbols('t')  # temps
u = sp.symbols('u')  # tension d'entrée
i = sp.Function('i')(t)  # courant
theta = sp.Function('theta')(t)  # position angulaire
omega = sp.Function('omega')(t)  # vitesse angulaire
tau = sp.symbols('tau')  # couple

# Paramètres du moteur
R = 1.0  # résistance
L = 0.1  # inductance
J = 0.01  # inertie
B = 0.1  # coefficient de frottement visqueux
K = 0.01  # constante de couple électromagnétique
Ke = 0.01  # constante de force contre-électromotrice

# Équations du modèle
eq1 = sp.Eq(u, R*i + L*sp.diff(i, t) + Ke*omega)
eq2 = sp.Eq(tau, K*i - B*omega - J*sp.diff(omega, t))
eq3 = sp.Eq(omega, sp.diff(theta, t))

# Résoudre les équations
solution = sp.dsolve([eq1, eq2, eq3], [i, omega, theta])

# Afficher les équations du modèle
print("Équations du modèle :")
for eq in solution:
    print(f'Equation : \t{eq}\n')

# # Simuler le modèle
# # Vous devrez utiliser une méthode numérique pour simuler le système, par exemple, odeint de la bibliothèque scipy.
# # Ceci est un exemple simple pour vous montrer comment vous pourriez simuler le système.

# # Définir les équations différentielles
# def system_equations(y, t):
#     i, omega, theta = y
#     du_dt = (R*i + L*sp.diff(i, t) + Ke*omega).subs({i: y[0], sp.diff(i, t): y[1]})
#     domega_dt = (K*i - B*omega - J*sp.diff(omega, t)).subs({i: y[0], sp.diff(omega, t): y[1]})
#     dtheta_dt = y[1]
#     return [du_dt, domega_dt, dtheta_dt]

# # Conditions initiales
# initial_conditions = [4.0, 1.0, 1.0]

# # Simuler le système
# time_points = np.linspace(0, 10, 1000)
# result = odeint(system_equations, initial_conditions, time_points)

# # Afficher les résultats
# plt.plot(time_points, result[:, 0], label='Courant (i)')
# plt.plot(time_points, result[:, 1], label='Vitesse angulaire (omega)')
# plt.plot(time_points, result[:, 2], label='Position angulaire (theta)')
# plt.xlabel('Temps')
# plt.ylabel('Valeurs')
# plt.legend()
# plt.show()
