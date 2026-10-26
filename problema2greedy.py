import matplotlib.pyplot as plt
import numpy as np

def greedy_knapsack(items, values, weights, W, criterion='density'):
    """
    Algoritmo voraz para la mochila 0/1.
    criterion: 'density' (v/w descendente) o 'min_weight' (w ascendente)
    """
    n = len(items)
    indices = list(range(n))
    
    if criterion == 'density':
        indices.sort(key=lambda i: values[i] / weights[i], reverse=True)
    elif criterion == 'min_weight':
        indices.sort(key=lambda i: weights[i])
    else:
        raise ValueError("Criterio no soportado")
        
    chosen = []
    total_val = 0
    total_w = 0
    
    for i in indices:
        if total_w + weights[i] <= W:
            chosen.append(items[i])
            total_w += weights[i]
            total_val += values[i]
            
    return chosen, total_w, total_val

# Definición de la instancia
items = ['A', 'B', 'C', 'D']
weights = [6, 10, 14, 40]
values = [12, 25, 28, 240]
capacity = 50

# Ejecuciones
chosen_mw, w_mw, v_mw = greedy_knapsack(items, values, weights, capacity, criterion='min_weight')
chosen_den, w_den, v_den = greedy_knapsack(items, values, weights, capacity, criterion='density')

print(f"Criterio Menor Peso     -> Items: {chosen_mw}, Capacidad Usada: {w_mw}/{capacity}, Valor: {v_mw}")
print(f"Criterio Densidad (v/w) -> Items: {chosen_den}, Capacidad Usada: {w_den}/{capacity}, Valor: {v_den}")

# Visualización comparativa
methods = ['Menor Peso (w)', 'Densidad (v/w)']
values_obtained = [v_mw, v_den]
weights_used = [w_mw, w_den]

x = np.arange(len(methods))
width = 0.35

fig, ax1 = plt.subplots(figsize=(8, 5))

rects1 = ax1.bar(x - width/2, values_obtained, width, label='Valor Total', color='#2ca02c')
ax1.set_ylabel('Valor Total Obtenido', fontsize=11, fontweight='bold', color='#2ca02c')
ax1.set_xticks(x)
ax1.set_xticklabels(methods, fontsize=11, fontweight='bold')
ax1.set_ylim(0, 300)

ax2 = ax1.twinx()
rects2 = ax2.bar(x + width/2, weights_used, width, label='Capacidad Usada', color='#1f77b4', alpha=0.85)
ax2.axhline(capacity, color='red', linestyle='--', linewidth=1.5, label=f'Capacidad Máxima ({capacity})')
ax2.set_ylabel('Peso Consumido', fontsize=11, fontweight='bold', color='#1f77b4')
ax2.set_ylim(0, 60)

ax1.bar_label(rects1, padding=3, fmt='%d pts', fontweight='bold')
ax2.bar_label(rects2, padding=3, fmt='%d kg', fontweight='bold')

plt.title('Comparativa de Estrategias Voraces en la Mochila 0/1', fontsize=13, fontweight='bold')
fig.tight_layout()
plt.show()