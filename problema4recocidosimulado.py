import math
import random
import time
import matplotlib.pyplot as plt
import numpy as np

def tour_length(points, route):
    return sum(math.dist(points[route[i]], points[route[(i+1) % len(route)]]) for i in range(len(route)))

def two_opt_move(route, i, k):
    return route[:i] + route[i:k+1][::-1] + route[k+1:]

def simulated_annealing(points, schedule_type='exponential', T0=150.0, alpha=0.995, max_iter=3500):
    n = len(points)
    current = list(range(n))
    random.shuffle(current)
    current_cost = tour_length(points, current)
    best = list(current)
    best_cost = current_cost
    
    T = T0
    history_cost = []
    
    t0 = time.perf_counter()
    for t in range(1, max_iter + 1):
        # Operador de movimiento 2-opt estocástico
        i, k = sorted(random.sample(range(n), 2))
        if i == 0 and k == n - 1:
            k -= 1
        neighbor = two_opt_move(current, i, k)
        neighbor_cost = tour_length(points, neighbor)
        
        delta = neighbor_cost - current_cost
        
        # Criterio de aceptación Metropolis
        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-8)):
            current = neighbor
            current_cost = neighbor_cost
            if current_cost < best_cost:
                best = list(current)
                best_cost = current_cost
                
        history_cost.append(current_cost)
        
        # Actualización de temperatura según esquema
        if schedule_type == 'exponential':
            T = T * alpha
        elif schedule_type == 'linear':
            T = max(1e-8, T0 * (1.0 - t / max_iter))
        elif schedule_type == 'logarithmic':
            T = T0 / (1.0 + alpha * math.log(1 + t))
            
    exec_time = time.perf_counter() - t0
    return best, best_cost, exec_time, history_cost

# Instancia fija para evaluación comparativa justa
random.seed(123)
cities_count = 30
pts = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(cities_count)]

schedules = ['exponential', 'linear', 'logarithmic']
results = {}

for sched in schedules:
    best_sol, b_cost, r_time, hist = simulated_annealing(pts, schedule_type=sched, max_iter=4000)
    results[sched] = {'cost': b_cost, 'time': r_time, 'history': hist}
    print(f"Esquema {sched:11s} -> Costo Final: {b_cost:.2f} | Tiempo: {r_time*1000:.2f} ms")

# Visualización
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# 1. Curvas de Convergencia
for sched in schedules:
    ax1.plot(results[sched]['history'], label=f"{sched.capitalize()} (Final: {results[sched]['cost']:.1f})", alpha=0.85)
ax1.set_title('Curvas de Convergencia: Costo vs. Iteraciones', fontsize=12, fontweight='bold')
ax1.set_xlabel('Iteraciones', fontsize=10)
ax1.set_ylabel('Costo del Recorrido Actual', fontsize=10)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend()

# 2. Tiempo de Ejecución vs. Calidad de la Solución
sched_names = [s.capitalize() for s in schedules]
final_costs = [results[s]['cost'] for s in schedules]
exec_times = [results[s]['time'] * 1000 for s in schedules]

ax2.scatter(exec_times, final_costs, s=120, c=['#2ca02c', '#1f77b4', '#d62728'], zorder=5)
for i, txt in enumerate(sched_names):
    ax2.annotate(txt, (exec_times[i] + 0.5, final_costs[i] + 5), fontsize=11, fontweight='bold')

ax2.set_title('Tiempo de Cómputo vs. Calidad de la Solución', fontsize=12, fontweight='bold')
ax2.set_xlabel('Tiempo de Ejecución (ms)', fontsize=10)
ax2.set_ylabel('Costo Final (Menor es mejor)', fontsize=10)
ax2.grid(True, linestyle=':', alpha=0.6)

plt.suptitle('Evaluación de Esquemas de Enfriamiento en Recocido Simulado', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()