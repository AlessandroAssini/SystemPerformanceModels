import numpy as np
import matplotlib.pyplot as plt
from MG1 import MG1Solve

def hit_ratio_approx(C):
    """ 
    Approximate LFU hit ratio for Zipf(alpha=1.5) with N=10000, 
    using a rational quadratic/quadratic fit: 
        H(C) ≈ (a + b*C + d*C^2) / (1 + f*C + g*C^2) 
    """ 
    a = 0.806616281 
    b = 1.719068781e-02 
    d = 5.050374574e-06 
    f = 1.740607985e-02 
    g = 5.026959698e-06 
 
    C = float(C)  # ensure numeric 
    return (a + b*C + d*C*C) / (1 + f*C + g*C*C)

def access_time_stats(P, H, K): 
    """ 
    Computes the mean and variance of cache access time. 
     
    Parameters: 
        P : hit ratio (0 <= P <= 1) 
        H : hit latency (seconds) 
        K : miss latency (seconds) 
     
    Returns: 
        mean_time, variance_time 
    """ 
    mean_time = P * H + (1 - P) * K 
    var_time = ( 
        P * (H - mean_time)**2 + 
        (1 - P) * (K - mean_time)**2 
    ) 
    return mean_time, var_time

def calculate_response_time(cache_size, arrival_rate, Dhit, Dmiss):

    # Hit probability: per C <= 0, nessuna cache → nessun hit
    if cache_size <= 0:
        P = 0.0
    else:
        P = hit_ratio_approx(cache_size)
    
    # Mean and variance of service time
    mean_service_time, var_service_time = access_time_stats(P, Dhit, Dmiss)
    
    if mean_service_time <= 0:
        return np.inf
    
    # Coefficient of variation
    if var_service_time > 0:
        cv = np.sqrt(var_service_time) / mean_service_time
    else:
        cv = 0.0
    
    # Utilization check (stabilità)
    U = arrival_rate * mean_service_time
    if U >= 1.0:
        # sistema instabile → tempo di risposta infinito
        return np.inf
    
    # M/G/1 response time
    result = MG1Solve(mean_service_time, cv, arrival_rate)
    
    return result['R']

def find_minimum_cache_size(arrival_rate, Dhit, Dmiss, target_response_time):

    low, high = 0, 10000
    result = high
    
    while low <= high:
        mid = (low + high) // 2
        R = calculate_response_time(mid, arrival_rate, Dhit, Dmiss)
        
        if R <= target_response_time:
            result = mid
            high = mid - 1
        else:
            low = mid + 1
    
    return result

def main():
    # Parameters from assignment
    Dhit = 0.1e-3  # 0.1 ms in seconds
    Dmiss = 5e-3   # 5 ms in seconds
    arrival_rates = [500, 1000, 2000]  # requests/second
    labels = ['A = 500 j/s', 'B = 1000 j/s', 'C = 2000 j/s']
    
    # Cache sizes to evaluate
    cache_sizes = np.arange(0, 1001, 10)
    
    # Plot response times
    plt.figure(figsize=(10, 6))
    
    for i, arrival_rate in enumerate(arrival_rates):
        response_times = []
        for C in cache_sizes:
            R = calculate_response_time(C, arrival_rate, Dhit, Dmiss)
            if not np.isfinite(R):
                R_ms = np.nan
            else:
                R_ms = R * 1000  # Convert to ms
            response_times.append(R_ms)
        
        plt.plot(cache_sizes, response_times, label=labels[i], linewidth=2)
    
    plt.xlabel('Cache Size', fontsize=12)
    plt.ylabel('Average Response Time (ms)', fontsize=12)
    plt.title('Response Time vs Cache Size for Different Arrival Rates', fontsize=14)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 1000)
    plt.ylim(0, 4)  # 0–4 ms as richiesto
    plt.tight_layout()
    plt.savefig('response_time_vs_cache_size.png', dpi=300)
    plt.show()
    
    print("=" * 60)
    print("MINIMUM CACHE SIZES FOR RESPONSE TIME < 1 ms")
    print("=" * 60)
    
    # Find minimum cache sizes
    target_response_time = 1e-3  # 1 ms in seconds
    
    for i, arrival_rate in enumerate(arrival_rates):
        min_cache = find_minimum_cache_size(arrival_rate, Dhit, Dmiss, target_response_time)
        actual_response_time = calculate_response_time(min_cache, arrival_rate, Dhit, Dmiss)
        
        print(f"\n{labels[i]}:")
        print(f"  Minimum cache size: {min_cache}")
        print(f"  Actual response time: {actual_response_time * 1000:.4f} ms")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
