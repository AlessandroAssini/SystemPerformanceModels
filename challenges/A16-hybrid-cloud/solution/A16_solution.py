import numpy as np
import matplotlib.pyplot as plt

PCLOUD_MIN = 0.01

def MVAscmsSolve(NStations, D, c, N, Z):
    Rk  = np.zeros(NStations)
    Nk  = np.zeros(NStations)
    Pki = np.zeros((NStations, N+1))
    for k in range(0, NStations):
        Pki[k, 0] = 1

    for n in range(1, N+1):
        R = 0

        for k in range(0, NStations):
            if (c[k] <= 0.0):
                Rk[k] = D[k]
            elif (c[k] >= 2.0):
                Rk[k] = 0
                for j in range(1, n+1):
                    cd = min(float(j), c[k])
                    Rk[k] = Rk[k] + float(j) / cd * Pki[k, j-1]
                Rk[k] = Rk[k] * D[k]
            else:
                Rk[k] = D[k] * (1 + Nk[k])
            R = R + Rk[k]

        X = n / (R + Z)

        for k in range(0, NStations):
            if (c[k] >= 2.0):
                spk = 0
                for j in range(n, 0, -1):
                    cd = min(float(j), c[k])
                    Pki[k, j] = X * D[k] / cd * Pki[k, j-1]
                    spk = spk + Pki[k, j]
                Pki[k, 0] = 1 - spk
            Nk[k] = X * Rk[k]
    
    return {'X':X, 'R':R, 'Nk':Nk, 'Rk':Rk}


def solve_hybrid_cloud(N, Z, S_dispatcher, S_private, S_public, c_private, P, pcloud):
    NStations = 3
    V_dispatcher = 1.0
    V_private = 1.0 - pcloud
    V_public = pcloud
    
    D = np.array([
        V_dispatcher * S_dispatcher,
        V_private * S_private,
        V_public * S_public
    ])
    
    c = np.array([1, c_private, P])
    result = MVAscmsSolve(NStations, D, c, N, Z)
    
    return result


def main():
    N = 200
    Z = 50
    S_dispatcher = 0.1
    S_private = 2.0
    S_public = 2.5
    c_private = 8
    target_R = 4.0
    
    P_max = 20
    pcloud_values = np.linspace(PCLOUD_MIN, 1.0, 100)
    P_values_plot = [1, 2, 4, 6, 8, 10]
    
    best_solution = None
    
    for P in range(1, P_max + 1):
        found_valid = False
        best_for_this_P = None
        
        for pcloud in pcloud_values:
            result = solve_hybrid_cloud(N, Z, S_dispatcher, S_private, S_public, 
                                       c_private, P, pcloud)
            R = result['R']
            
            if R > 0 and R < target_R:
                found_valid = True
                if best_for_this_P is None or R < best_for_this_P['R']:
                    best_for_this_P = {
                        'P': P, 
                        'pcloud': pcloud, 
                        'R': R, 
                        'X': result['X'],
                        'result': result
                    }
        
        if found_valid:
            best_solution = best_for_this_P
            break
    
    if best_solution is None:
        print(f"No solution found with P up to {P_max}")
        return
    
    plt.figure(figsize=(10, 6))
    
    for P in P_values_plot:
        R_values = []
        pcloud_filtered = []
        
        for pcloud in pcloud_values:
            result = solve_hybrid_cloud(N, Z, S_dispatcher, S_private, S_public, 
                                       c_private, P, pcloud)
            R = result['R']
            if R >= 5.0:
                break
            R_values.append(R)
            pcloud_filtered.append(pcloud)
        
        if P == best_solution['P']:
            plt.plot(pcloud_filtered, R_values, linewidth=2,
                    label=f'P = {P} (Optimal)', color='green')
        else:
            plt.plot(pcloud_filtered, R_values, label=f'P = {P}')
    
    plt.plot(best_solution['pcloud'], best_solution['R'], 'r*', 
            markersize=15, label=f"Solution: P={best_solution['P']}, pcloud={best_solution['pcloud']:.3f}")
    
    plt.axhline(y=target_R, color='r', linestyle='--', linewidth=1.5, 
               label=f'Target R = {target_R} s')
    
    plt.xlabel('pcloud')
    plt.ylabel('Response Time R (s)')
    plt.title('Response Time vs Routing Probability')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, target_R * 1.5)
    plt.tight_layout()
    
    plt.savefig('A16_response_time_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n" + "="*70)
    print("OPTIMAL SOLUTION")
    print("="*70)
    print(f"Minimum P: {best_solution['P']}")
    print(f"Optimal pcloud: {best_solution['pcloud']:.4f}")
    print(f"Response time R: {best_solution['R']:.4f} s")
    print("="*70)


if __name__ == "__main__":
    main()
