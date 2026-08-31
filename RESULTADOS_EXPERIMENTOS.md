# Resultados Experimentales - Taller Búsqueda Informada

## tinyMaze (PositionSearchProblem)

| Método | Costo | Expandidos | Tiempo | Óptimo |
|--------|-------|------------|--------|--------|
| UCS | 10 | 18 | 0.0s | Sí |
| A* + h=0 (nullHeuristic) | 10 | 18 | 0.0s | Sí |
| A* + Manhattan | 10 | 10 | 0.0s | Sí |
| A* + Euclidiana | 10 | 10 | 0.0s | Sí |

## tinyCorners (CornersProblem)

| Método | Costo | Expandidos | Tiempo | Óptimo |
|--------|-------|------------|--------|--------|
| UCS | 22 | 377 | 0.0s | Sí |
| A* + h=0 (nullHeuristic) | 22 | 377 | 0.0s | Sí |
| A* + cornersHeuristic (propuesta) | 22 | 124 | 0.0s | Sí |

## FoodSearchProblem

### tinySearch (1 food)

| Método | Costo | Expandidos | Tiempo | Óptimo |
|--------|-------|------------|--------|--------|
| UCS | 8 | 16 | 0.0s | Sí |
| A* + h=0 | 8 | 16 | 0.0s | Sí |
| A* + Heurística 1 (Max Manhattan) | 8 | 8 | 0.0s | Sí |
| A* + Heurística 2 (MST) | 8 | 8 | 0.0s | Sí |

### testClassic (5 foods)

| Método | Costo | Expandidos | Tiempo | Óptimo | Victoria |
|--------|-------|------------|--------|--------|----------|
| UCS | 16 | 2,598 | 0.2s | Sí | No |
| A* + h=0 | 16 | 2,598 | 0.2s | Sí | No |
| A* + Heurística 1 (Max Manhattan) | 16 | 702 | 0.0s | Sí | No |
| **A* + Heurística 2 (MST)** | **16** | **111** | **0.0s** | **Sí** | **Sí** |

### smallClassic (muchos foods) - Límite 120s

| Método | Costo | Expandidos | Tiempo | Óptimo |
|--------|-------|------------|--------|--------|
| UCS | Timeout (>120s) | - | - | - |
| A* + Heurística 1 (Max Manhattan) | Timeout (>120s) | - | - | - |
| A* + Heurística 2 (MST) | 60 | 10,882 | 112.9s | Sí |

---

## Factor de Reducción de Expansiones (R = N_UCS / N_A*)

| Problema | Heurística | N_UCS | N_A* | R = N_UCS / N_A* |
|----------|------------|-------|------|------------------|
| tinyMaze | Manhattan | 18 | 10 | **1.8** |
| tinyMaze | Euclidiana | 18 | 10 | **1.8** |
| tinyCorners | cornersHeuristic | 377 | 124 | **3.04** |
| tinySearch | Max Manhattan | 16 | 8 | **2.0** |
| testClassic | Max Manhattan | 2,598 | 702 | **3.7** |
| **testClassic** | **MST** | **2,598** | **111** | **23.4** |

---

## Heurísticas Implementadas para FoodSearchProblem

### Heurística 1: Max Manhattan Distance
```python
def foodHeuristic(state, problem):
    position, foodGrid = state
    foodList = foodGrid.asList()
    if not foodList:
        return 0
    from util import manhattanDistance
    return max(manhattanDistance(position, food) for food in foodList)
```
- **Idea**: El costo mínimo es al menos la distancia al alimento más lejano
- **Admisible**: Sí, nunca sobreestima (distancia mínima ignorando paredes)
- **Consistente**: Sí, la distancia Manhattan es consistente

### Heurística 2: MST (Minimum Spanning Tree) con caché
```python
def foodHeuristicV2(state, problem):
    position, foodGrid = state
    foodList = foodGrid.asList()
    if not foodList:
        return 0
    
    # Caché de distancias entre pares de alimentos
    if 'foodDistances' not in problem.heuristicInfo:
        distances = {}
        for i, f1 in enumerate(foodList):
            for j, f2 in enumerate(foodList):
                if i < j:
                    d = manhattanDistance(f1, f2)
                    distances[(f1, f2)] = d
                    distances[(f2, f1)] = d
        problem.heuristicInfo['foodDistances'] = distances
    
    # Distancia al alimento más cercano
    minDistToFood = min(manhattanDistance(position, food) for food in foodList)
    
    # MST aproximado (Prim's algorithm)
    if len(foodList) == 1:
        mstCost = 0
    else:
        remaining = set(foodList)
        mstCost = 0
        current = foodList[0]
        remaining.remove(current)
        while remaining:
            minDist = float('inf')
            nearest = None
            for food in remaining:
                for mstFood in [f for f in foodList if f not in remaining]:
                    d = problem.heuristicInfo['foodDistances'].get((food, mstFood), manhattanDistance(food, mstFood))
                    if d < minDist:
                        minDist = d
                        nearest = food
            mstCost += minDist
            remaining.remove(nearest)
    
    return minDistToFood + mstCost
```
- **Idea**: Costo mínimo ≈ distancia al alimento más cercano + MST de alimentos restantes
- **Admisible**: Sí, MST es cota inferior del camino que visita todos los nodos
- **Consistente**: Aproximadamente (usa distancias Manhattan que son consistentes)
- **Optimización**: Usa `problem.heuristicInfo` para cachear distancias entre pares

---

## Conclusiones

1. **Heurísticas informadas reducen drásticamente la búsqueda**: En testClassic, MST reduce expansiones **23.4x** vs UCS
2. **Heurística MST es muy superior**: 111 vs 702 nodos (6.3x mejor que Max Manhattan)
3. **Caché mejora el tiempo**: En testClassic, MST con caché ejecuta en 0.0s vs UCS 0.2s
4. **Optimalidad mantenida**: Todas las heurísticas admisibles encuentran costo óptimo (16 en testClassic)
5. **Problemas grandes**: smallClassic sigue siendo difícil (>10k nodos, >110s) - requiere heurísticas más sofisticadas (ej. MST con distancias reales de laberinto, no Manhattan)

---

## Comandos Utilizados

```bash
# PositionSearchProblem - tinyMaze
python pacman.py -l tinyMaze -p SearchAgent -a fn=ucs --frameTime 0
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=nullHeuristic --frameTime 0
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic --frameTime 0
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=euclideanHeuristic --frameTime 0

# CornersProblem - tinyCorners
python pacman.py -l tinyCorners -p SearchAgent -a fn=ucs,prob=CornersProblem --frameTime 0
python pacman.py -l tinyCorners -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=nullHeuristic --frameTime 0
python pacman.py -l tinyCorners -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=cornersHeuristic --frameTime 0

# FoodSearchProblem
python pacman.py -l tinySearch -p SearchAgent -a fn=ucs,prob=FoodSearchProblem --frameTime 0
python pacman.py -l tinySearch -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=nullHeuristic --frameTime 0
python pacman.py -l tinySearch -p AStarFoodSearchAgent --frameTime 0

python pacman.py -l testClassic -p SearchAgent -a fn=ucs,prob=FoodSearchProblem --frameTime 0
python pacman.py -l testClassic -p SearchAgent -a fn=astar,prob=FoodSearchProblem,heuristic=nullHeuristic --frameTime 0
python pacman.py -l testClassic -p AStarFoodSearchAgent --frameTime 0  # Heurística 2 (MST)

python pacman.py -l smallClassic -p AStarFoodSearchAgent --frameTime 0
```