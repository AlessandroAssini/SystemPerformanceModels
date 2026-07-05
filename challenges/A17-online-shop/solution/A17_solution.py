import numpy as np
import matplotlib.pyplot as plt
from OPENmcss import OPENmcssSolve

S = np.array([
    [0.05, 0.30],
    [0.21, 0.12],
    [0.08, 0.25],
    [0.00, 1.20]
])

P_b = [0.50, 0.30, 0.20, 0.00]
P_p = [0.30, 0.15, 0.25, 0.30]

NStations = 4
NClasses = 2
c = [1, 1, 1, 0]

V = np.zeros((NStations, NClasses))
V[0, 0] = 1.0 / P_b[0]
V[1, 0] = V[0, 0] * P_b[1]
V[2, 0] = V[0, 0] * P_b[2]
V[3, 0] = V[0, 0] * P_b[3]

V[0, 1] = 1.0 / P_p[0]
V[1, 1] = V[0, 1] * P_p[1]
V[2, 1] = V[0, 1] * P_p[2]
V[3, 1] = V[0, 1] * P_p[3]

D = V * S

print("\nQ1: Demands")
print("D = ", D)

mix_b = 0.90
mix_p = 0.10

D_avg = D[:, 0] * mix_b + D[:, 1] * mix_p
lambda_max = 1.0 / np.max(D_avg[:3])

print(f"\nQ2: Lambda_max = {lambda_max:.4f} req/s")

l_vals = np.linspace(0.1, 0.99 * lambda_max, 50)
R_sys = []
R_0 = []
R_1 = []

for lam in l_vals:
    l = [lam * mix_b, lam * mix_p]
    res = OPENmcssSolve(NStations, NClasses, D, c, l)
    R_sys.append(res['R'])
    R_0.append(np.sum(res['Rkc'][:, 0]))
    R_1.append(np.sum(res['Rkc'][:, 1]))

plt.plot(l_vals, R_sys)
plt.plot(l_vals, R_0)
plt.plot(l_vals, R_1)
plt.xlabel('Lambda')
plt.ylabel('R')
plt.show()

print("\nQ4a: Response Time vs Browsing Fraction (Dynamic Lambda)")
beta = np.linspace(0, 1.0, 50)
R = np.zeros((50, 3))

for n in range(0, 50):
    D_mix = D[:, 0] * beta[n] + D[:, 1] * (1 - beta[n])
    lam_max = 1.0 / np.max(D_mix[:3])
    lam = 0.75 * lam_max
    l = [lam * beta[n], lam * (1 - beta[n])]
    res = OPENmcssSolve(NStations, NClasses, D, c, l)
    R[n, 0] = res['R']
    R[n, 1] = np.sum(res['Rkc'][:, 0])
    R[n, 2] = np.sum(res['Rkc'][:, 1])

plt.plot(beta * 100, R)
plt.xlabel('Beta (%)')
plt.ylabel('R')
plt.show()

print("\nQ4b: Response Time vs Browsing Fraction (Fixed Lambda)")
lambda_total = 0.75 * lambda_max
R2 = np.zeros((50, 3))

for n in range(0, 50):
    lambda_b = max(beta[n] * lambda_total, 1e-10)
    lambda_p = max((1 - beta[n]) * lambda_total, 1e-10)
    l = [lambda_b, lambda_p]
    res = OPENmcssSolve(NStations, NClasses, D, c, l)
    R2[n, 0] = res['R']
    R2[n, 1] = np.sum(res['Rkc'][:, 0])
    R2[n, 2] = np.sum(res['Rkc'][:, 1])

plt.plot(beta * 100, R2)
plt.xlabel('Beta (%)')
plt.ylabel('R')
plt.show()