import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg

# Balancing requests in a secure system
# Given parameters
lambda1 = 2500  # req/s - arrival rate to CPU (station 1)
lambda2 = 1000  # req/s - arrival rate to Storage 1 (station 2)

S_CPU = 0.05 / 1000  # Convert ms to seconds (station 1)
S_Storage1 = 0.15 / 1000  # Station 2
S_Storage2 = 0.25 / 1000  # Station 3

p_s2_cpu = 0.1  # Probability of returning from Storage 2 to CPU
p_s2_exit = 0.9  # Probability of exiting from Storage 2

print("="*80)
print("BALANCING REQUESTS IN A SECURE SYSTEM")
print("="*80)
print(f"\nGiven Parameters:")
print(f"  λ1 (arrival to CPU) = {lambda1} req/s")
print(f"  λ2 (arrival to Storage 1) = {lambda2} req/s")
print(f"  S_CPU (S1) = {S_CPU*1000} ms")
print(f"  S_Storage1 (S2) = {S_Storage1*1000} ms")
print(f"  S_Storage2 (S3) = {S_Storage2*1000} ms")
print(f"  p(Storage2 → CPU) = {p_s2_cpu}")
print(f"  p(Storage2 → Exit) = {p_s2_exit}")

print("\n" + "="*80)
print("STEP 1: Build Routing Probability Matrix P and Solve for Visit Ratios")
print("="*80)

print("\nNetwork Structure:")
print("  Station 1 (CPU): receives external arrivals λ1 + feedback from Storage2")
print("  Station 2 (Storage1): receives external arrivals λ2 + routing from CPU")
print("  Station 3 (Storage2): receives routing from CPU + returns to CPU with prob 0.1")
print("\nRouting from CPU: probability (1-α) to Storage1, probability α to Storage2")

def calculate_visits_matrix(alpha):
    """
    Calculate visit ratios using matrix approach (following L18 slides)
    
    Routing Probability Matrix P:
    P[i][j] = probability of going from station i to station j
    
    Station indices: 0=CPU, 1=Storage1, 2=Storage2
    """
    # Ensure alpha is a scalar
    if isinstance(alpha, np.ndarray):
        alpha_val = alpha.item()
    else:
        alpha_val = float(alpha)
    
    # Construct routing probability matrix P (3x3)
    # From CPU: go to Storage1 with prob (1-α), to Storage2 with prob α
    # From Storage1: exit (no internal routing)
    # From Storage2: return to CPU with prob 0.1, exit with prob 0.9
    
    P = np.array([
        [0.0,    1-alpha_val,  alpha_val    ],  # From CPU
        [0.0,    0.0,      0.0      ],  # From Storage1 (exits)
        [p_s2_cpu, 0.0,    0.0      ]   # From Storage2
    ])
    
    # External arrival rates vector
    # λ_ext[i] = external arrival rate to station i
    lambda_ext = np.array([lambda1, lambda2, 0])
    
    # Solve for visit ratios: V = (I - P^T)^(-1) * λ_ext
    # This gives absolute visit rates (arrivals/sec) for each station
    I = np.eye(3)
    Q = I - P.T
    
    # Total arrival rates to each station
    Lambda = linalg.solve(Q, lambda_ext)
    
    # Visit ratios relative to λ1 (throughput of class entering at CPU)
    V = Lambda / lambda1
    
    return V, Lambda, P

def calculate_demands(alpha):
    """Calculate demands as function of alpha"""
    V, Lambda, P = calculate_visits_matrix(alpha)
    
    # Service times array
    S = np.array([S_CPU, S_Storage1, S_Storage2])
    
    # Demands: D_i = V_i * S_i
    D = V * S
    
    return D[0], D[1], D[2], V, Lambda

print("\nFor open networks with multiple entry points:")
print("  V = (I - P^T)^(-1) * λ_ext")
print("  where λ_ext is the vector of external arrivals")
print("  D_i = V_i * S_i")

print("\nFor open networks with multiple entry points:")
print("  V = (I - P^T)^(-1) * λ_ext")
print("  where λ_ext is the vector of external arrivals")
print("  D_i = V_i * S_i")

# Test at alpha = 0.5
alpha_test = 0.5
D_CPU_test, D_S1_test, D_S2_test, V_test, Lambda_test = calculate_demands(alpha_test)

print(f"\nExample calculation at α = {alpha_test}:")
print(f"  Total arrival rates: Λ_CPU = {Lambda_test[0]:.2f}, Λ_Storage1 = {Lambda_test[1]:.2f}, Λ_Storage2 = {Lambda_test[2]:.2f} req/s")
print(f"  Visit ratios (relative to λ1): V_CPU = {V_test[0]:.4f}, V_Storage1 = {V_test[1]:.4f}, V_Storage2 = {V_test[2]:.4f}")
print(f"  D_CPU = {D_CPU_test*1000:.6f} ms")
print(f"  D_Storage1 = {D_S1_test*1000:.6f} ms")
print(f"  D_Storage2 = {D_S2_test*1000:.6f} ms")

print("\n" + "="*80)
print("STEP 3: Plot Demands vs α")
print("="*80)

# Create array of alpha values
alpha_values = np.linspace(0, 0.99, 1000)

# Calculate demands for each alpha
D_CPU_values = []
D_Storage1_values = []
D_Storage2_values = []

for alpha in alpha_values:
    D_CPU, D_Storage1, D_Storage2, V, Lambda = calculate_demands(alpha)
    D_CPU_values.append(D_CPU * 1000)  # Convert to ms
    D_Storage1_values.append(D_Storage1 * 1000)
    D_Storage2_values.append(D_Storage2 * 1000)

# Create the plot
plt.figure(figsize=(12, 8))
plt.plot(alpha_values, D_CPU_values, 'b-', linewidth=2, label='D_CPU')
plt.plot(alpha_values, D_Storage1_values, 'g-', linewidth=2, label='D_Storage1')
plt.plot(alpha_values, D_Storage2_values, 'r-', linewidth=2, label='D_Storage2')

plt.xlabel('α (Probability of routing to Storage 2)', fontsize=12)
plt.ylabel('Demand (ms)', fontsize=12)
plt.title('Demand of Three Stations as Function of α', fontsize=14, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)
plt.xlim(0, 1)

print("\nPlot created showing demands as function of α")

print("\n" + "="*80)
print("STEP 4: Find α where D_Storage1 = D_Storage2")
print("="*80)

# Find intersection point where D_Storage1 = D_Storage2
# We need to solve: V_Storage1_total * S_Storage1 = V_Storage2 * S_Storage2

print("\nSetting D_Storage1 = D_Storage2:")
print("  V_Storage1 * S_Storage1 = V_Storage2 * S_Storage2")
print("\nUsing matrix formulation to find α where demands are equal")

# Numerical solution: find where difference is minimized
differences = []
for i, alpha in enumerate(alpha_values):
    diff = abs(D_Storage1_values[i] - D_Storage2_values[i])
    differences.append(diff)

min_diff_idx = np.argmin(differences)
alpha_optimal = alpha_values[min_diff_idx]
D_CPU_opt = D_CPU_values[min_diff_idx]
D_Storage1_opt = D_Storage1_values[min_diff_idx]
D_Storage2_opt = D_Storage2_values[min_diff_idx]

print(f"\nNumerical Solution:")
print(f"  α* = {alpha_optimal:.6f}")
print(f"  D_CPU = {D_CPU_opt:.6f} ms")
print(f"  D_Storage1 = {D_Storage1_opt:.6f} ms")
print(f"  D_Storage2 = {D_Storage2_opt:.6f} ms")
print(f"  Difference = {abs(D_Storage1_opt - D_Storage2_opt):.9f} ms")

# For analytical solution, we need to solve the system more carefully
# Using the matrix approach:
# V = (I - P^T)^(-1) * λ_ext
# For D_Storage1 = D_Storage2:
# V_Storage1 * S_Storage1 = V_Storage2 * S_Storage2

print(f"\nAnalytical Solution:")
print(f"  Solving D_Storage1 = D_Storage2 using numerical optimization...")

# Use scipy to find exact solution
from scipy.optimize import fsolve

def balance_equation(alpha):
    """Returns difference between D_Storage1 and D_Storage2"""
    D_CPU, D_Storage1, D_Storage2, V, Lambda = calculate_demands(alpha)
    return D_Storage1 - D_Storage2

# Find root starting from numerical estimate
alpha_analytical = fsolve(balance_equation, alpha_optimal)[0]

print(f"  α* = {alpha_analytical:.6f}")

# Verify
D_CPU_verify, D_S1_verify, D_S2_verify, V_verify, Lambda_verify = calculate_demands(alpha_analytical)
print(f"\nVerification with α* = {alpha_analytical:.6f}:")
print(f"  Visit ratios: V_CPU = {V_verify[0]:.4f}, V_Storage1 = {V_verify[1]:.4f}, V_Storage2 = {V_verify[2]:.4f}")
print(f"  Total arrivals: Λ_CPU = {Lambda_verify[0]:.2f}, Λ_Storage1 = {Lambda_verify[1]:.2f}, Λ_Storage2 = {Lambda_verify[2]:.2f} req/s")
print(f"  D_CPU = {D_CPU_verify*1000:.6f} ms")
print(f"  D_Storage1 = {D_S1_verify*1000:.6f} ms")
print(f"  D_Storage2 = {D_S2_verify*1000:.6f} ms")
print(f"  Difference = {abs(D_S1_verify - D_S2_verify)*1000:.9f} ms")

# Add intersection point to plot
plt.plot(alpha_analytical, D_S1_verify*1000, 'ko', markersize=10, 
         label=f'Intersection: α = {alpha_analytical:.4f}')
plt.axvline(x=alpha_analytical, color='black', linestyle='--', alpha=0.5)
plt.axhline(y=D_S1_verify*1000, color='black', linestyle='--', alpha=0.5)

plt.legend(fontsize=11, loc='best')
plt.tight_layout()
plt.savefig('A14_demands_vs_alpha.png', dpi=150, bbox_inches='tight')
print("\nPlot saved as: A14_demands_vs_alpha.png")

# Create a zoomed-in view around the intersection
plt.figure(figsize=(12, 8))
alpha_zoom = np.linspace(max(0, alpha_analytical - 0.1), min(1, alpha_analytical + 0.1), 500)

D_CPU_zoom = []
D_Storage1_zoom = []
D_Storage2_zoom = []

for alpha in alpha_zoom:
    D_CPU, D_Storage1, D_Storage2, V, Lambda = calculate_demands(alpha)
    D_CPU_zoom.append(D_CPU * 1000)
    D_Storage1_zoom.append(D_Storage1 * 1000)
    D_Storage2_zoom.append(D_Storage2 * 1000)

plt.plot(alpha_zoom, D_CPU_zoom, 'b-', linewidth=2, label='D_CPU')
plt.plot(alpha_zoom, D_Storage1_zoom, 'g-', linewidth=2, label='D_Storage1')
plt.plot(alpha_zoom, D_Storage2_zoom, 'r-', linewidth=2, label='D_Storage2')
plt.plot(alpha_analytical, D_S1_verify*1000, 'ko', markersize=12, 
         label=f'Intersection: α = {alpha_analytical:.6f}')
plt.axvline(x=alpha_analytical, color='black', linestyle='--', alpha=0.5)
plt.axhline(y=D_S1_verify*1000, color='black', linestyle='--', alpha=0.5)

plt.xlabel('α (Probability of routing to Storage 2)', fontsize=12)
plt.ylabel('Demand (ms)', fontsize=12)
plt.title('Demand of Three Stations - Zoomed View Around Intersection', fontsize=14, fontweight='bold')
plt.legend(fontsize=11, loc='best')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('A14_demands_vs_alpha_zoomed.png', dpi=150, bbox_inches='tight')
print("Zoomed plot saved as: A14_demands_vs_alpha_zoomed.png")

print("\n" + "="*80)
print("FINAL ANSWER")
print("="*80)
print(f"\nThe value of α that balances the demand of the two storage devices is:")
print(f"  α* = {alpha_analytical:.6f}")
print(f"\nAt this value:")
print(f"  D_CPU = {D_CPU_verify*1000:.6f} ms")
print(f"  D_Storage1 = D_Storage2 = {D_S1_verify*1000:.6f} ms")
print("="*80)

plt.show()
