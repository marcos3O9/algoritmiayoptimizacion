import math
import itertools
import random
import numpy as np
import matplotlib.pyplot as plt

def tour_length(points, tour):
    """Calcula la distancia total euclidiana del ciclo cerrado."""
    n = len(tour)
    return sum(
        math.dist(points[tour[i]], points[tour[(i + 1) % n]])
        for i in range(n)
    )

def mst_prim(points):
    """
    Algoritmo de Prim.
    Construye el árbol de adyacencia (padre -> lista de hijos).
    """
    n = len(points)
    best = {v: (math.dist(points[0], points[v]), 0) for v in range(1, n)}
    children = {v: [] for v in range(n)}
    
    while best:
        v = min(best, key=lambda u: best[u][0])
        cost, parent = best.pop(v)
        children[parent].append(v)
        
        for u in best:
            d = math.dist(points[v], points[u])
            if d < best[u][0]:
                best[u] = (d, v)
                
    return children

def preorder(children, root=0):
    """Recorrido en preorden (DFS) garantizando una lista plana sin duplicados."""
    tour = []
    def dfs(u):
        tour.append(u)
        for child in children[u]:
            dfs(child)
    dfs(root)
    return tour

def two_opt(points, route):
    """2-opt local search determinista."""
    tour = list(route)
    n = len(tour)
    improved = True
    
    while improved:
        improved = False
        for i in range(n - 1):
            for k in range(i + 1, n):
                if i == 0 and k == n - 1:
                    continue
                
                p_prev, p_i = points[tour[i - 1]], points[tour[i]]
                p_k, p_next = points[tour[k]], points[tour[(k + 1) % n]]
                
                d_actual = math.dist(p_prev, p_i) + math.dist(p_k, p_next)
                d_nuevo = math.dist(p_prev, p_k) + math.dist(p_i, p_next)
                
                if d_nuevo < d_actual - 1e-9:
                    tour[i:k + 1] = reversed(tour[i:k + 1])
                    improved = True
                    break
            if improved:
                break
                
    return tour, tour_length(points, tour)

def solve_optimal_bruteforce(points):
    """Calcula el optimo global exacto para 9 ciudades mediante fuerza bruta."""
    n = len(points)
    best_cost = float('inf')
    best_tour = None
    
    for perm in itertools.permutations(range(1, n)):
        candidate = (0,) + perm
        cost = tour_length(points, candidate)
        if cost < best_cost:
            best_cost = cost
            best_tour = candidate
            
    return list(best_tour), best_cost

def main():
    random.seed(42)
    num_instances = 100
    num_cities = 9
    
    ratios = []
    costs_opt = []
    costs_mst = []
    costs_mst_2opt = []
    
    for _ in range(num_instances):
        points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cities)]
        
        # 1. Optimo Exacto
        _, opt_len = solve_optimal_bruteforce(points)
        costs_opt.append(opt_len)
        
        # 2. MST Puro
        tree = mst_prim(points)
        mst_tour = preorder(tree, root=0)
        
        assert len(mst_tour) == num_cities, "Error: Faltan ciudades en el recorrido"
        
        mst_len = tour_length(points, mst_tour)
        costs_mst.append(mst_len)
        
        ratio = mst_len / opt_len
        ratios.append(ratio)
        
        # 3. MST + 2-opt
        _, mst_2opt_len = two_opt(points, mst_tour)
        costs_mst_2opt.append(mst_2opt_len)
        
    # --- VISUALIZACION ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Grafica 1: Histograma con cadenas 'raw' (r'...') para evitar el ParseException
    ax1.hist(ratios, bins=15, color='#2b5c8f', edgecolor='black', alpha=0.75, density=True)
    ax1.axvline(2.0, color='red', linestyle='--', linewidth=2.5, label=r'Cota Teórica ($\rho = 2.0$)')
    ax1.axvline(np.mean(ratios), color='#e67e22', linestyle='-', linewidth=2, label=f'Media ({np.mean(ratios):.3f})')
    ax1.set_title(r'Razón de Aproximación ($C_{MST} / C_{Óptimo}$)', fontsize=12, fontweight='bold')
    ax1.set_xlabel(r'Razón de Aproximación $\rho$')
    ax1.set_ylabel('Densidad')
    ax1.set_xlim(0.9, 2.1)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend()
    
    # Grafica 2: Comparativa de Calidad (Diagrama de Caja)
    box_data = [costs_opt, costs_mst, costs_mst_2opt]
    labels = ['Óptimo', 'MST Puro', 'MST + 2-opt']
    colors = ['#27ae60', '#c0392b', '#2980b9']
    
    bp = ax2.boxplot(box_data, tick_labels=labels, patch_artist=True)
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
        
    ax2.set_title('Impacto de 2-opt en 100 Instancias (9 Ciudades)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Costo del Recorrido')
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plt.show()
    
    print("=== RESULTADOS VERIFICADOS ===")
    print(f"Razón de Aproximación -> Mínimo: {min(ratios):.3f} | Media: {np.mean(ratios):.3f} | Máximo: {max(ratios):.3f}")
    print(f"Costo Promedio        -> Óptimo: {np.mean(costs_opt):.2f} | MST Puro: {np.mean(costs_mst):.2f} | MST+2-opt: {np.mean(costs_mst_2opt):.2f}")

if __name__ == '__main__':
    main()