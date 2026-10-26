import multiprocessing as mp
import random
import time
import matplotlib.pyplot as plt

def estimate_pi(seed: int, samples: int = 1_500_000) -> float:
    """Estimación Monte Carlo de Pi según el documento."""
    rng = random.Random(seed)
    inside = sum(rng.random()**2 + rng.random()**2 <= 1.0 for _ in range(samples))
    return 4 * inside / samples

def run_experiment():
    total_runs = 8
    seeds = list(range(total_runs))
    
    # 1. Ejecución Secuencial Base
    t0 = time.perf_counter()
    seq_results = [estimate_pi(s) for s in seeds]
    t_seq = time.perf_counter() - t0
    
    process_counts = [1, 2, 4, 8]
    times = []
    speedups = []
    
    # 2. Ejecución Paralela con diferentes configuraciones de procesos
    for p in process_counts:
        t0 = time.perf_counter()
        with mp.Pool(processes=p) as pool:
            par_results = pool.map(estimate_pi, seeds)
        t_par = time.perf_counter() - t0
        times.append(t_par)
        speedups.append(t_seq / t_par)
        print(f"Procesos: {p:2d} | Tiempo: {t_par:.3f} s | Speedup: {t_seq / t_par:.2f}x")

    # 3. Visualización: Speedup real vs. Speedup ideal
    plt.figure(figsize=(8, 5))
    plt.plot(process_counts, speedups, marker='o', linewidth=2, color='#1f77b4', label='Speedup Experimental')
    plt.plot(process_counts, process_counts, linestyle='--', color='#d62728', label='Speedup Lineal Ideal ($S(p)=p$)')
    
    plt.title('Aceleración Paralela (Parallel Speedup) en estimate_pi', fontsize=13, fontweight='bold')
    plt.xlabel('Número de Procesos ($p$)', fontsize=11)
    plt.ylabel('Aceleración ($S_p = T_1 / T_p$)', fontsize=11)
    plt.xticks(process_counts)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    run_experiment()