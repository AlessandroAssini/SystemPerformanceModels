import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg

def OPENsolve(NStations, D, c, l, v):
    Rk = np.zeros(NStations)
    Nk = np.zeros(NStations)
    Uk = np.zeros(NStations)
    R = 0
    
    for k in range(NStations):
        U = l * D[k]
        Uk[k] = U / c[k] if c[k] > 0 else U
        
        if c[k] <= 0.0:
            Rk[k] = D[k]
        elif c[k] == 1.0:
            Rk[k] = D[k] / (1 - U)
        else:
            Fc = 1
            Sm = 1
            Tr = 1
            for j in range(1, int(c[k])):
                Tr = Tr * U / j
                Fc = Fc * j / U
                Sm = Sm + Tr
            Rk[k] = D[k] * (1 + 1 / (c[k] - U) / (1 + (c[k] - U) / U * Fc * Sm))
        
        R = R + Rk[k]
    
    X = l
    for k in range(NStations):
        Nk[k] = X * v[k] * Rk[k]
    
    return {'X': X, 'R': R, 'Nk': Nk, 'Rk': Rk, 'Uk': Uk}

S = np.array([0.0005, 0.012, 0.0075, 0.003, 0.008])
p_audio = 0.05
p_video = 0.95
p_mc_given_video = 5.0/6.0

P = np.array([
    [0.0, p_audio, p_video, 0.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 0.0, p_mc_given_video],
    [0.0, 0.0, 0.0, 0.0, 0.0]
])

Q = np.eye(5) - P
l = np.array([1.0, 0.0, 0.0, 0.0, 0.0])
v = linalg.solve(Q.T, l)
D = v * S

print("Service Demands (D = v * S):")
for i, name in enumerate(['demux', 'audio', 'ed', 'db', 'mc']):
    print(f"  {name:8s}: {D[i]*1000:.4f} ms")
print()

def find_optimal_config(l, D, v, max_servers=40):
    best = None
    best_total = float('inf')
    
    for m_ed in range(1, max_servers + 1):
        for m_db in range(1, max_servers + 1):
            for m_mc in range(1, max_servers + 1):
                c = np.array([1, 1, m_ed, m_db, m_mc])
                
                stable = True
                for k in range(len(c)):
                    U = l * D[k]
                    if (c[k] == 1 and U >= 1) or (c[k] > 1 and U / c[k] >= 1):
                        stable = False
                        break
                
                if not stable:
                    continue
                
                result = OPENsolve(5, D, c, l, v)
                
                if result['R'] < 0.040:
                    total_servers = m_ed + m_db + m_mc
                    if total_servers < best_total:
                        best_total = total_servers
                        best = {
                            'c': c.copy(),
                            'R': result['R'],
                            'ed': int(c[2]),
                            'db': int(c[3]),
                            'mc': int(c[4])
                        }
    
    return best

lambdas = [400, 500, 600, 700, 800]
results = []

for l in lambdas:
    optimal = find_optimal_config(l, D, v)
    if optimal:
        results.append({'lambda': l, **optimal})

lambdas_vals = [r['lambda'] for r in results]
eds = [r['ed'] for r in results]
dbs = [r['db'] for r in results]
mcs = [r['mc'] for r in results]
Rs = [r['R']*1000 for r in results]

plt.figure()
plt.plot(lambdas_vals, eds, marker='o', label='ED-IQ-DCT')
plt.plot(lambdas_vals, dbs, marker='s', label='DB')
plt.plot(lambdas_vals, mcs, marker='^', label='MC')
plt.xlabel('Arrival rate (packets/s)')
plt.ylabel('Required units')
plt.grid(True)
plt.legend()
plt.savefig('units_vs_lambda.png', dpi=150)

plt.figure()
plt.plot(lambdas_vals, Rs, marker='o')
plt.axhline(y=40, color='r', linestyle='--', label='Target')
plt.xlabel('Arrival rate (packets/s)')
plt.ylabel('Response time (ms)')
plt.grid(True)
plt.legend()
plt.savefig('response_vs_lambda.png', dpi=150)

print(f"{'Lambda':>8} {'ED':>4} {'DB':>4} {'MC':>4} {'R(ms)':>8}")
for r in results:
    print(f"{r['lambda']:>8} {r['ed']:>4} {r['db']:>4} {r['mc']:>4} {r['R']*1000:>8.2f}")