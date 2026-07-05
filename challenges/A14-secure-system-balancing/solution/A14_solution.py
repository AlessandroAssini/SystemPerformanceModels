import numpy as np
import matplotlib.pyplot as plt

# Given parameters
lambda1 = 2500
lambda2 = 1000

S_CPU = 0.05 / 1000
S_Storage1 = 0.15 / 1000
S_Storage2 = 0.25 / 1000

p_s2_cpu = 0.1
p_s2_exit = 0.9

def calculate_demands(alpha):
    P = np.array([[0.0,    1-alpha,  alpha    ],
                  [0.0,    0.0,      0.0      ],
                  [p_s2_cpu, 0.0,    0.0      ]])
    
    l = np.array([lambda1, lambda2, 0.0])
    
    Q = np.eye(3) - P
    Lambda = np.linalg.solve(Q.T, l)
    lambda0 = lambda1 + lambda2
    V = Lambda / lambda0

    S = np.array([S_CPU, S_Storage1, S_Storage2])
    
    D = V * S
    
    return D[0], D[1], D[2], V, Lambda

alpha_values = np.linspace(0, 1, 1000)

D_CPU_values = []
D_Storage1_values = []
D_Storage2_values = []

for alpha in alpha_values:
    D_CPU, D_Storage1, D_Storage2, V, Lambda = calculate_demands(alpha)
    D_CPU_values.append(D_CPU * 1000)
    D_Storage1_values.append(D_Storage1 * 1000)
    D_Storage2_values.append(D_Storage2 * 1000)

plt.figure(figsize=(8, 5))
plt.plot(alpha_values, D_CPU_values, 'b-', label='D_CPU')
plt.plot(alpha_values, D_Storage1_values, 'g-', label='D_Storage1')
plt.plot(alpha_values, D_Storage2_values, 'r-', label='D_Storage2')

# Find alpha where D_Storage1 = D_Storage2
differences = [abs(D_Storage1_values[i] - D_Storage2_values[i]) for i in range(len(alpha_values))]
min_idx = differences.index(min(differences))
alpha_optimal = alpha_values[min_idx]

D_CPU_verify, D_S1_verify, D_S2_verify, V_verify, Lambda_verify = calculate_demands(alpha_optimal)

plt.plot(alpha_optimal, D_S1_verify*1000, 'ko', markersize=6)
plt.axvline(x=alpha_optimal, color='gray', linestyle='--')
plt.axhline(y=D_S1_verify*1000, color='gray', linestyle='--')

plt.xlabel('alpha')
plt.ylabel('Demand (ms)')
plt.title('Demand vs alpha')
plt.legend()
plt.grid()
plt.savefig('A14_demands_vs_alpha.png')

print(f"alpha* = {alpha_optimal:.6f}")
print(f"D_CPU = {D_CPU_verify*1000:.6f} ms")
print(f"D_Storage1 = D_Storage2 = {D_S1_verify*1000:.6f} ms")

plt.show()
