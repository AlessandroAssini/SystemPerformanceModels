import math
import itertools
import numpy as np
import matplotlib.pyplot as plt

# Service times in seconds
S = {
    'demux': 0.0005,
    'audio': 0.012,
    'ed': 0.0075,
    'db': 0.003,
    'mc': 0.008
}

# Visit probabilities
p_audio = 0.05
p_video = 1.0 - p_audio
p_mc_given_video = 5.0/6.0

p_ed = p_video
p_db = p_video
p_mc = p_video * p_mc_given_video

# Erlang C helper functions

def factorial(n):
    return math.factorial(n)


def erlang_c_waiting_time(lmbda, mu, m):
    # lmbda: arrival rate to node (jobs/s)
    # mu: service rate per server (jobs/s)
    # m: number of servers
    if m <= 0:
        return float('inf')
    a = lmbda / mu  # offered load
    rho = a / m
    if rho >= 1:
        return float('inf')
    # compute P0 (probability zero customers) and Erlang C
    # Using stable numeric approach
    sum_terms = 0.0
    for k in range(m):
        sum_terms += (a**k) / factorial(k)
    last = (a**m) / (factorial(m) * (1.0 - rho))
    p0 = 1.0 / (sum_terms + last)
    erlang_c = last * p0
    wq = erlang_c / (m * mu - lmbda)
    return wq


def mm_m_response_time(lmbda, S_service, m):
    # returns average time in system for a visit (S + Wq)
    mu = 1.0 / S_service
    if m == 1:
        rho = lmbda * S_service
        if rho >= 1.0:
            return float('inf')
        wq = rho / (mu - lmbda)
        return S_service + wq
    else:
        wq = erlang_c_waiting_time(lmbda, mu, m)
        return S_service + wq


def compute_demands_ms():
    D = {}
    D['demux'] = S['demux'] * 1000.0
    D['audio'] = p_audio * S['audio'] * 1000.0
    D['ed'] = p_ed * S['ed'] * 1000.0
    D['db'] = p_db * S['db'] * 1000.0
    D['mc'] = p_mc * S['mc'] * 1000.0
    return D


def find_minimal_combination(lmbda, max_servers=30, R_target=0.04):
    # lmbda in jobs/s (packets/sec)
    # search over m_ed, m_db, m_mc
    best = None
    best_servers = None
    # arrival rates to nodes
    lam_demux = lmbda
    lam_audio = lmbda * p_audio
    lam_ed = lmbda * p_ed
    lam_db = lmbda * p_db
    lam_mc = lmbda * p_mc

    # keep demux and audio as single-server
    R_demux = mm_m_response_time(lam_demux, S['demux'], 1)
    R_audio = mm_m_response_time(lam_audio, S['audio'], 1)

    # brute force search
    for m_ed in range(1, max_servers+1):
        R_ed = mm_m_response_time(lam_ed, S['ed'], m_ed)
        if R_ed == float('inf'):
            continue
        for m_db in range(1, max_servers+1):
            R_db = mm_m_response_time(lam_db, S['db'], m_db)
            if R_db == float('inf'):
                continue
            for m_mc in range(1, max_servers+1):
                R_mc = mm_m_response_time(lam_mc, S['mc'], m_mc)
                if R_mc == float('inf'):
                    continue
                # overall average response time (seconds)
                R_total = (
                    1.0 * R_demux +
                    p_audio * R_audio +
                    p_ed * R_ed +
                    p_db * R_db +
                    p_mc * R_mc
                )
                if R_total < R_target:
                    servers = m_ed + m_db + m_mc
                    if best is None or servers < best_servers or (servers == best_servers and (m_ed < best[0] or (m_ed==best[0] and m_db<best[1]))):
                        best = (m_ed, m_db, m_mc, R_total)
                        best_servers = servers
        # small optimization: if we already found a solution with m_ed==1 and small totals, continue
    return best


def main():
    demands = compute_demands_ms()
    print("Service demands (ms):")
    for k,v in demands.items():
        print(f"  {k}: {v:.4f} ms")

    lambdas = list(range(400, 801, 100))  # packets per second
    results = {}
    for lam in lambdas:
        print(f"\nComputing for arrival rate {lam} pkt/s")
        best = find_minimal_combination(lam, max_servers=40, R_target=0.04)
        if best is None:
            print("  No feasible combination up to 40 servers each meets R<40ms")
            results[lam] = None
        else:
            m_ed, m_db, m_mc, R = best
            print(f"  Found: ED={m_ed}, DB={m_db}, MC={m_mc}, R_total={(R*1000):.3f} ms")
            results[lam] = {'ed':m_ed, 'db':m_db, 'mc':m_mc, 'R':R}

    # Prepare data for plotting
    eds = [results[lam]['ed'] if results[lam] else np.nan for lam in lambdas]
    dbs = [results[lam]['db'] if results[lam] else np.nan for lam in lambdas]
    mcs = [results[lam]['mc'] if results[lam] else np.nan for lam in lambdas]
    Rs = [results[lam]['R']*1000.0 if results[lam] else np.nan for lam in lambdas]

    plt.figure()
    plt.plot(lambdas, eds, marker='o', label='ED-IQ-DCT units')
    plt.plot(lambdas, dbs, marker='s', label='DB units')
    plt.plot(lambdas, mcs, marker='^', label='MC units')
    plt.xlabel('Arrival rate (packets/s)')
    plt.ylabel('Required units')
    plt.title('Required parallel units vs arrival rate')
    plt.grid(True)
    plt.legend()
    plt.savefig('units_vs_lambda.png', dpi=150)
    print('\nSaved plot units_vs_lambda.png')

    plt.figure()
    plt.plot(lambdas, Rs, marker='o')
    plt.xlabel('Arrival rate (packets/s)')
    plt.ylabel('Average response time (ms)')
    plt.title('Average response time for chosen configurations')
    plt.grid(True)
    plt.savefig('response_vs_lambda.png', dpi=150)
    print('Saved plot response_vs_lambda.png')

    print('\nResults table:')
    for lam in lambdas:
        r = results[lam]
        if r is None:
            print(f" {lam} pkt/s: No feasible config up to search limits")
        else:
            print(f" {lam} pkt/s: ED={r['ed']} DB={r['db']} MC={r['mc']} R={(r['R']*1000):.3f} ms")

if __name__ == '__main__':
    main()
