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

print("="*80)
print("BALANCING REQUESTS IN A SECURE SYSTEM - DEBUG MODE")
print("="*80)
print(f"\nGiven Parameters:")
print(f"  λ1 (arrival to CPU) = {lambda1} req/s")
print(f"  λ2 (arrival to Storage1) = {lambda2} req/s")
print(f"  S_CPU = {S_CPU*1000} ms")
print(f"  S_Storage1 = {S_Storage1*1000} ms")
print(f"  S_Storage2 = {S_Storage2*1000} ms")
print(f"  p(Storage2 → CPU) = {p_s2_cpu}")
print(f"  p(Storage2 → Exit) = {p_s2_exit}")

def calculate_demands(alpha):
    P = np.array([[0.0,    1-alpha,  alpha    ],
                  [0.0,    0.0,      0.0      ],
                  [p_s2_cpu, 0.0,    0.0      ]])
    
    l = np.array([lambda1, lambda2, 0.0])
    
    Q = np.eye(3) - P
    Lambda = np.linalg.solve(Q.T, l)
    
    V = Lambda / lambda1

    S = np.array([S_CPU, S_Storage1, S_Storage2])
    
    D = V * S
    
    return D[0], D[1], D[2], V, Lambda

print("\n" + "="*80)
print("STEP 1: Build Routing Probability Matrix P")
print("="*80)
print("\nNetwork structure:")
print("  CPU → Storage1 with probability (1-α)")
print("  CPU → Storage2 with probability α")
print("  Storage2 → CPU with probability 0.1")
print("  Storage2 → Exit with probability 0.9")

print("\n" + "="*80)
print("STEP 2: Test with α = 0.5")
print("="*80)
alpha_test = 0.5
D_CPU_test, D_S1_test, D_S2_test, V_test, Lambda_test = calculate_demands(alpha_test)
print(f"\nWith α = {alpha_test}:")
print(f"  Total arrival rates:")
print(f"    Λ_CPU = {Lambda_test[0]:.2f} req/s")
print(f"    Λ_Storage1 = {Lambda_test[1]:.2f} req/s")
print(f"    Λ_Storage2 = {Lambda_test[2]:.2f} req/s")
print(f"  Visit ratios:")
print(f"    V_CPU = {V_test[0]:.4f}")
print(f"    V_Storage1 = {V_test[1]:.4f}")
print(f"    V_Storage2 = {V_test[2]:.4f}")
print(f"  Demands:")
print(f"    D_CPU = {D_CPU_test*1000:.6f} ms")
print(f"    D_Storage1 = {D_S1_test*1000:.6f} ms")
print(f"    D_Storage2 = {D_S2_test*1000:.6f} ms")

print("\n" + "="*80)
print("STEP 3: Plot Demands vs α")
print("="*80)

alpha_values = np.linspace(0, 0.99, 1000)

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

print("\n" + "="*80)
print("STEP 4: Find α* where D_Storage1 = D_Storage2")
print("="*80)

alpha_analytical = 15.0 / 29.0
D_CPU_verify, D_S1_verify, D_S2_verify, V_verify, Lambda_verify = calculate_demands(alpha_analytical)

print(f"\nAnalytical solution: α* = 15/29 = {alpha_analytical:.6f}")
print(f"\nVerification with α* = {alpha_analytical:.6f}:")
print(f"  Total arrival rates:")
print(f"    Λ_CPU = {Lambda_verify[0]:.2f} req/s")
print(f"    Λ_Storage1 = {Lambda_verify[1]:.2f} req/s")
print(f"    Λ_Storage2 = {Lambda_verify[2]:.2f} req/s")
print(f"  Visit ratios:")
print(f"    V_CPU = {V_verify[0]:.6f}")
print(f"    V_Storage1 = {V_verify[1]:.6f}")
print(f"    V_Storage2 = {V_verify[2]:.6f}")
print(f"  Demands:")
print(f"    D_CPU = {D_CPU_verify*1000:.6f} ms")
print(f"    D_Storage1 = {D_S1_verify*1000:.6f} ms")
print(f"    D_Storage2 = {D_S2_verify*1000:.6f} ms")
print(f"  Difference = {abs(D_S1_verify - D_S2_verify)*1000:.9f} ms")

plt.plot(alpha_analytical, D_S1_verify*1000, 'ko', markersize=6)
plt.axvline(x=alpha_analytical, color='gray', linestyle='--')
plt.axhline(y=D_S1_verify*1000, color='gray', linestyle='--')

plt.xlabel('alpha')
plt.ylabel('Demand (ms)')
plt.title('Demand vs alpha')
plt.legend()
plt.grid()
plt.savefig('A14_demands_vs_alpha_debug.png')

print("\n" + "="*80)
print("FINAL RESULT")
print("="*80)
print(f"alpha* = {alpha_analytical:.6f}")
print(f"D_CPU = {D_CPU_verify*1000:.6f} ms")
print(f"D_Storage1 = D_Storage2 = {D_S1_verify*1000:.6f} ms")
print("="*80)

plt.show()
