# Algoritmos y Optimización: Ejercicios Prácticos

Implementaciones y análisis empírico de optimización, paralelismo y heurísticas.

## Estructura de Ejercicios

- **Ejercicio 1 (`problema1paralelos.py`):** Aceleración paralela de estimación Monte Carlo de $\pi$ (1, 2, 4 y 8 procesos) vs. speedup ideal y análisis por Ley de Amdahl.
- **Ejercicio 2 (`problema2greedy.py`):** Problema de la mochila 0/1 comparando el criterio voraz por menor peso frente a densidad de valor ($v/w$).
- **Ejercicio 3 (`problema3hillclimb.py`):** Búsqueda local 2-opt para TSP contrastando inicio aleatorio vs. Vecino Más Cercano (Nearest Neighbour).
- **Ejercicio 4 (`problema4recocidosimulado.py`):** Recocido simulado para TSP evaluando curvas de convergencia y tiempo con esquemas exponencial, lineal y logarítmico.
- **Ejercicio 5 (`problema5approximacion.py`):** Algoritmo de aproximación métrico 2-TSP con Prim (MST) y atajos en preorden sobre 100 instancias, verificando $\rho \le 2$ y refinamiento con 2-opt.

## Instalación y Ejecución

```bash
pip install -r requirements.txt
python problema1paralelos.py
python problema5aproximacion.py