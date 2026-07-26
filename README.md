# [PEA Challenges](https://github.com/AlessandroAssini/SystemPerformanceModels)

> Worked solutions to performance-evaluation case studies, combining JMT/JMVA queueing models with Python analytical solvers.

## 🌟 Highlights

- 18 independent case studies, from staffing a medical center to sizing a hybrid-cloud deployment.
- Every challenge pairs a JMT/JMVA network model (`.jsimg`) with a Python script that solves the same problem analytically.
- Reusable queueing solvers for classic models: M/M/c/K, multiclass MVA, M/G/1.
- Each script generates its own plots (utilization, response time, cost curves) alongside the numerical results.
- A consistent folder layout across all challenges, so any solution can be reused as a template for a new problem.

## ℹ️ Overview

This repository collects solved assignments from the *Performance Evaluation and Applications* course. Each challenge starts from a short description of a real system — a medical center, a RAID array, an online shop, a car maintenance facility — and asks questions like: how many servers are needed? What response time can be expected? What's the optimal trade-off between cost and performance?

Every problem is worked out in two complementary ways: a queueing-network model built with JMT/JMVA (Java Modelling Tools), and a Python script that solves the same model analytically. The repository is meant for students and practitioners who want to see performance-evaluation techniques — queueing networks, mean value analysis, cost optimization — applied to concrete, end-to-end examples instead of isolated formulas.

## 🧩 How It Works

Each challenge follows the same pipeline:

1. **Assignment** — a short problem statement describes the system, its workload, and the questions to answer (see each challenge's own `README.md`).
2. **Modeling** — the system is represented as a queueing network, either as a JMT/JMVA model file (`.jsimg`) or as an analytical model in Python.
3. **Solving** — a Python solver (e.g. `MMcKSolve`, `MVAmcmsSolve`, `MG1Solve`) computes performance indices such as utilization, throughput, response time, and cost.
4. **Visualization** — results are plotted with `matplotlib` and saved as figures for quick inspection.

## 🚀 Usage

Run any challenge's solution script directly with Python:

```bash
cd challenges/A13-cache-performance/solution
python3 A13_solution.py
```

For example, the solver in `A05-car-maintenance-facility/solution` searches for the number of service nodes that minimizes total cost, using an M/M/c/K queueing model:

```python
from MMcK import MMcKSolve

sol = MMcKSolve(D, c, K, Lambda)   # solve the M/M/c/K queue
cost = n * (Cfix + sol['Uave'] * Cvar) + Cpen * sol['Dr']
```

Running the script prints the optimal configuration and saves a cost-vs-capacity plot in the same folder.

The `.jsimg` files under each challenge's `models/` folder are JMT (Java Modelling Tools) projects and can be opened with JMT itself.

## ⬇️ Installation

### Requirements

- Python 3.9+
- [NumPy](https://numpy.org/) and [Matplotlib](https://matplotlib.org/)
- JMT (Java Modelling Tools) and a Java runtime, only if you want to open the `.jsimg` model files

### Setup

```bash
git clone https://github.com/AlessandroAssini/SystemPerformanceModels.git
cd SystemPerformanceModels
pip install numpy matplotlib
```

There is no shared build step: each challenge is self-contained under `challenges/<challenge-name>/solution/`.

## 📁 Project Structure

```
SystemPerformanceModels/
├── challenges/
│   ├── A01-medical-center/
│   │   ├── README.md        # assignment description and folder contents
│   │   ├── models/          # JMT/JMVA .jsimg models
│   │   └── figures/         # generated plots
│   ├── A12-microservice-cost-minimization/
│   │   ├── notes/           # assignment notes
│   │   └── solution/        # Python solvers and scripts
│   └── ...                  # 18 challenges in total
└── README.md
```

## 🛠️ Technologies

- **Language:** Python 3
- **Numerical computing:** NumPy
- **Visualization:** Matplotlib
- **Queueing-network modeling:** JMT / JMVA (`.jsimg` model files)
- **Documentation:** Markdown

## ✍️ Authors

- [Alessandro Assini](https://github.com/AlessandroAssini)

Developed as part of the *Performance Evaluation and Applications* university course.

## 🤝 Contributing

This repository mainly documents solved coursework, but suggestions are welcome:

- Open an issue to report a mistake or suggest an improvement.
- Submit a pull request to propose a fix or an additional challenge.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 📖 Further Reading

Each challenge has its own `README.md` describing the specific problem and folder contents:

- [A01-medical-center](challenges/A01-medical-center/)
- [A02-local-versioning-service](challenges/A02-local-versioning-service/)
- [A03-3d-printing-service](challenges/A03-3d-printing-service/)
- [A04-electric-car-charging-facility](challenges/A04-electric-car-charging-facility/)
- [A05-car-maintenance-facility](challenges/A05-car-maintenance-facility/)
- [A06-microcontroller](challenges/A06-microcontroller/)
- [A07-insurance-backend](challenges/A07-insurance-backend/)
- [A08-raid-1-comparison](challenges/A08-raid-1-comparison/)
- [A09-city-transport-system](challenges/A09-city-transport-system/)
- [A10-production-plant-inspections](challenges/A10-production-plant-inspections/)
- [A11-server-on-off-features](challenges/A11-server-on-off-features/)
- [A12-microservice-cost-minimization](challenges/A12-microservice-cost-minimization/)
- [A13-cache-performance](challenges/A13-cache-performance/)
- [A14-secure-system-balancing](challenges/A14-secure-system-balancing/)
- [A15-media-decoder](challenges/A15-media-decoder/)
- [A16-hybrid-cloud](challenges/A16-hybrid-cloud/)
- [A17-online-shop](challenges/A17-online-shop/)
- [A18-secure-transaction-system](challenges/A18-secure-transaction-system/)

<!-- Note: course slides, examples, archived attempts, delivery packages, and assignment PDFs are intentionally excluded from this public repository. -->
