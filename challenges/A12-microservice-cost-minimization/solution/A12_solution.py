import numpy as np
import matplotlib.pyplot as plt
from MMcK import MMcKSolve

# System parameters
D = 0.1
Lambda = 100
H = 8

# Cost parameters
Cfix = 0.01
Cvar = 0.05
Cpen = 0.15

# Range of nodes to test
N = range(1, 21)
cost = [0.0] * len(N)

j = 0
for n in N:
    c = n 
    K = c + H
    
    # Solve M/M/c/K system
    sol = MMcKSolve(D, c, K, Lambda)
    
    # Calculate total cost
    cost[j] = n * (Cfix + sol['Uave'] * Cvar) + Cpen * sol['Dr']
    j = j + 1

# Find optimal N
optimal_idx = np.argmin(cost)
optimal_N = list(N)[optimal_idx]
optimal_cost = cost[optimal_idx]

print(f"Optimal number of nodes: {optimal_N}")
print(f"Minimum cost: ${optimal_cost:.4f}")

# Plot results
plt.figure()
plt.plot(N, cost, label='cost')
plt.axvline(x=optimal_N, color='red', label=f'optimal N={optimal_N}')
plt.xlabel('Number of nodes (N)')
plt.ylabel('Total cost ($)')
plt.title('Cost vs N')
plt.grid(True)
plt.legend()
plt.savefig('A12_cost_optimization.png')
print('Saved plot: A12_cost_optimization.png')
plt.show()
