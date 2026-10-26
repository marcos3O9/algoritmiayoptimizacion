import math
import random
import numpy as np
import matplotlib.pyplot as plt

def tour_length(points, route):
    return sum(math.dist(points[route[i]], points[route[(i+1) % len(route)]]) for i in range(len(route)))

def two_opt_move(route, i, k):
    """Invierte el segmento route[i:k+1]."""
    return route[:i] + route[i:k+1][::-1] + route[k+1:]

def two_opt_local_search(points, initial_route):
    """Aplica 2-opt first-improvement hasta alcanzar el óptimo local."""
    route = list(initial_route)
    n = len(route)
    improvements = 0
    improved = True
    
    while improved:
        improved = False
        for i in range(1, n - 1):
            for k in range(i + 1, n):
                if k - i == 1:
                    continue
                p_prev, p_i = points[route[i-1]], points[route[i]]
                p_k, p_next = points[route[k]], points[route[(k+1) % n]]
                
                delta = (math.dist(p_prev, p_k) + math.dist(p_i, p_next)) - \
                        (math.dist(p_prev, p_i) + math.dist(p_k, p_next))
                        
                if delta < -1e-9:
                    route = two_opt_move(route, i, k)
                    improvements += 1
                    improved = True
                    break
            if improved:
                break
    return route, tour_length(points, route), improvements

def nearest_neighbour_tour(points, start_node=None):
    n = len(points)
    if start_node is None:
        start_node = random.randint(0, n - 1)
    unvisited = set(range(n))
    unvisited.remove(start_node)
    tour = [start_node]
    curr = start_node
    while unvisited:
        nxt = min(unvisited, key=lambda c: math.dist(points[curr], points[c]))
        unvisited.remove(nxt)
        tour.append(nxt)
        curr = nxt
    return tour

# Experimento sobre 60 instancias de 25 ciudades
random.seed(42)
num_instances = 60
num_cities = 25

improvements_random = []
improvements_nn = []
costs_random = []
costs_nn = []

for _ in range(num_instances):
    pts = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_cities)]
    
    # 1. Inicio Aleatorio
    rand_init = list(range(num_cities))
    random.shuffle(rand_init)
    _, final_cost_rand, imp_rand = two_opt_local_search(pts, rand_init)
    improvements_random.append(imp_rand)
    costs_random.append(final_cost_rand)
    
    # 2. Inicio Vecino Más Cercano (nodo inicial aleatorio)
    nn_init = nearest_neighbour_tour(pts)
    _, final_cost_nn, imp_nn = two_opt_local_search(pts, nn_init)
    improvements_nn.append(imp_nn)
    costs_nn.append(final_cost_nn)

# Visualización comparativa (Boxplots)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Gráfica de Número de Mejoras
box1 = ax1.boxplot([improvements_random, improvements_nn], tick_labels=['Aleatorio', 'Vecino Cercano'], patch_artist=True)
ax1.set_title('Número de Mejoras hasta Óptimo Local', fontsize=12, fontweight='bold')
ax1.set_ylabel('Pasos de Mejora (Swaps Aceptados)', fontsize=10)
ax1.grid(True, linestyle=':', alpha=0.6)
box1['boxes'][0].set_facecolor('#ff7f0e')
box1['boxes'][1].set_facecolor('#1f77b4')

# Gráfica de Calidad de la Solución Final
box2 = ax2.boxplot([costs_random, costs_nn], tick_labels=['Aleatorio', 'Vecino Cercano'], patch_artist=True)
ax2.set_title('Longitud Final del Recorrido', fontsize=12, fontweight='bold')
ax2.set_ylabel('Costo Euclidiano Total', fontsize=10)
ax2.grid(True, linestyle=':', alpha=0.6)
box2['boxes'][0].set_facecolor('#ff7f0e')
box2['boxes'][1].set_facecolor('#1f77b4')

plt.suptitle('Comparación de Inicializaciones en Búsqueda Local 2-opt (TSP)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

print(f"Promedio de Mejoras -> Aleatorio: {np.mean(improvements_random):.2f} | Vecino Más Cercano: {np.mean(improvements_nn):.2f}")
print(f"Costo Promedio      -> Aleatorio: {np.mean(costs_random):.2f} | Vecino Más Cercano: {np.mean(costs_nn):.2f}")