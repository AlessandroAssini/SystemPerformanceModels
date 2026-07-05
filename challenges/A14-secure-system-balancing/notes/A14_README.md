# A14 - Balancing Requests in a Secure System
## Performance Evaluation of a Cache

### Problem Description
A system composed of:
- 1 CPU
- 2 Storage devices
  - Storage 1: receives traffic from CPU and external arrivals
  - Storage 2: has security requirements, returns requests to CPU with probability 0.1

**Goal**: Find probability α of routing from CPU to Storage 2 such that the demands of both storage devices are equal.

### Given Parameters
- λ1 = 2500 req/s (arrival rate to CPU)
- λ2 = 1000 req/s (arrival rate to Storage 1)
- S_CPU = 0.05 ms
- S_Storage1 = 0.15 ms
- S_Storage2 = 0.25 ms
- p(Storage2 → CPU) = 0.1
- p(Storage2 → Exit) = 0.9

### Solution Methodology (Following L18 - Open Models)

#### 1. Routing Probability Matrix
The network is modeled as an open queueing network with routing matrix P:

```
P = [  0.0    (1-α)    α   ]  (from CPU)
    [  0.0     0.0    0.0  ]  (from Storage1 - exits)
    [  0.1     0.0    0.0  ]  (from Storage2)
```

#### 2. Visit Ratios Calculation
Using the formula from L18 slides:
- V = (I - P^T)^(-1) * λ_ext

Where:
- λ_ext = [2500, 1000, 0] (external arrivals to each station)
- V = visit ratios (total arrivals to each station / λ1)

#### 3. Demand Calculation
- D_i = V_i * S_i for each station i

#### 4. Finding Balance Point
Solve: D_Storage1 = D_Storage2

### Results

**Optimal Value: α* = 0.517241** (approximately 51.72%)

At this value:
- D_CPU = 0.052727 ms
- **D_Storage1 = 0.136364 ms**
- **D_Storage2 = 0.136364 ms**
- Difference < 10^-9 ms (essentially zero)

Visit ratios at optimal α:
- V_CPU = 1.0545
- V_Storage1 = 0.9091
- V_Storage2 = 0.5455

Total arrival rates at optimal α:
- Λ_CPU = 2636.36 req/s
- Λ_Storage1 = 2272.73 req/s
- Λ_Storage2 = 1363.64 req/s

### Interpretation
- When α = 0.517241, approximately 51.72% of requests from CPU are routed to Storage 2
- The remaining 48.28% go to Storage 1
- This balances the workload (demand) between the two storage devices
- Both storage devices have identical demand of 0.136364 ms

### Files Included
1. `A14_solution.py` - Complete Python solution
2. `A14_demands_vs_alpha.png` - Plot showing demands as function of α
3. `A14_demands_vs_alpha_zoomed.png` - Zoomed view around intersection point
4. `A14_README.md` - This summary document
