import numpy as np
import matplotlib.pyplot as plt
from MVAmcms import MVAmcmsSolve


S = np.array([[14, 9], [40, 24], [10, 14], [20, 12], [25, 20]])
V = np.array([[1.4, 1.0], [1.0, 1.0], [0.8, 1.2], [1.2, 0.5], [1.0, 1.0]])
D = S * V

c = [3, 1, 2, 1, 0]
Z = [0.0, 0.0]

N1 = 25
N2 = 15
N = [N1, N2]

res = MVAmcmsSolve(5, 2, D, c, N, Z)

Xc = res['Xc']
Rkc = res['Rkc']

# Task 1: Utilization
print("Utilization:")
for k in range(4):
    U = (Xc[0] * D[k, 0] + Xc[1] * D[k, 1]) / c[k]
    print(f"  Station {k+1}: {U:.4f}")

# Task 2: Response time
R = np.zeros((3))
for k in range(4):
    R[0] = R[0] + Rkc[k, 0]
    R[1] = R[1] + Rkc[k, 1]
R[2] = (R[0] * Xc[0] + R[1] * Xc[1]) / (Xc[0] + Xc[1])

print("\nResponse Time (excluding buffer):")
print(f"  Normal:   {R[0]:.2f} s")
print(f"  Priority: {R[1]:.2f} s")
print(f"  Total:    {R[2]:.2f} s")

# Task 3: Plot
n2 = np.arange(5, 36)
Rplot = np.zeros((len(n2), 3))

for i in range(len(n2)):
    res = MVAmcmsSolve(5, 2, D, c, [N1, n2[i]], Z)
    Xc = res['Xc']
    Rkc = res['Rkc']
    for k in range(4):
        Rplot[i, 0] = Rplot[i, 0] + Rkc[k, 0]
        Rplot[i, 1] = Rplot[i, 1] + Rkc[k, 1]
    Rplot[i, 2] = (Rplot[i, 0] * Xc[0] + Rplot[i, 1] * Xc[1]) / (Xc[0] + Xc[1])

plt.plot(n2, Rplot)
plt.legend(['Normal', 'Priority', 'Total'])
plt.xlabel('N2 (Priority Users)')
plt.ylabel('Response Time (s)')
plt.show()
