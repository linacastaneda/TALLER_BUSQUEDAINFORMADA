# TALLER BÚSQUEDA INFORMADA - Pac-Man

Implementación de algoritmos de búsqueda informada y no informada

---

## Estructura del Repositorio

```
TALLER_BUSQUEDAINFORMADA/
├── PCMAN/
│   └── PCMAN/
│       ├── search.py              # Algoritmos de búsqueda (DFS, BFS, UCS, A*)
│       ├── searchAgents.py        # Problemas de búsqueda y heurísticas
│       ├── pacman.py              # Motor principal del juego
│       ├── game.py                # Lógica del juego
│       ├── util.py                # Estructuras de datos (Stack, Queue, PriorityQueue)
│       ├── layout.py              # Parsing de layouts
│       ├── graphics*.py           # Visualización
│       ├── ghostAgents.py         # Agentes fantasma
│       ├── keyboardAgents.py      # Control manual
│       ├── sanityAgents.py        # Agentes de prueba
│       ├── textDisplay.py         # Display en terminal
│       └── layouts/               # Mapas (.lay)
│           ├── tinyMaze.lay
│           ├── tinyCorners.lay
│           ├── tinySearch.lay
│           ├── testClassic.lay
│           ├── smallClassic.lay
│           └── ... (otros layouts)
├── RESULTADOS_EXPERIMENTOS.md     # Tablas de resultados experimentales
├── ANALISIS_FINAL.md              # Respuestas a preguntas de análisis
└── README.md                      # Este archivo
```

---

## Actividades Implementadas

### Punto 1 - Exploración del Entorno
**Archivo:** `searchAgents.py` (`PositionSearchProblem`)

**Qué se hizo:** Análisis del espacio de estados de Pac-Man.

**Conceptos:**
- **Estado**: Posición (x, y) de Pac-Man en el laberinto
- **Estado inicial**: Posición donde aparece Pac-Man al iniciar
- **Acciones**: Norte, Sur, Este, Oeste (si no hay pared)
- **Función sucesor**: Genera estados vecinos válidos con costo 1
- **Objetivo**: Llegar a (1, 1) en tinyMaze / visitar 4 esquinas / comer toda la comida
- **Costo**: Suma de pasos (cada movimiento = 1)

---

### Punto 2 - Búsqueda de Costo Uniforme (UCS)
**Archivo:** `search.py` → `uniformCostSearch()`

**Qué se hizo:** Implementación de UCS usando `util.PriorityQueue`.

**Conceptos:**
- Frontera: Cola de prioridad ordenada por costo acumulado g(n)
- Expande siempre el nodo con menor costo de camino desde el inicio
- Garantiza optimalidad si costos ≥ 0
- **Resultado tinyMaze**: Costo 10, 21 nodos expandidos (según PDF), 18 en nuestra ejecución

---

### Punto 3 - Implementación de A*
**Archivo:** `search.py` → `aStarSearch()`

**Qué se hizo:** Implementación de A* con función de evaluación f(n) = g(n) + h(n).

**Conceptos:**
- g(n) = costo real acumulado desde inicio
- h(n) = heurística (estimación costo restante al objetivo)
- f(n) = prioridad en cola de prioridad
- Usa `util.PriorityQueue` con prioridad f(n)

---

### Punto 4 - A* sin Información (h = 0)
**Archivo:** `search.py` → `nullHeuristic()` + `aStarSearch()`

**Qué se hizo:** Análisis de A* con heurística nula.

**Conceptos:**
- h(n) = 0 para todo n
- f(n) = g(n) + 0 = g(n)
- **Comportamiento idéntico a UCS**
- **Resultado**: Mismo costo (10) y mismos nodos expandidos (18 en tinyMaze, 377 en tinyCorners)

---

### Punto 5 - Heurística Manhattan
**Archivo:** `searchAgents.py` → `manhattanHeuristic()`

**Qué se hizo:** Implementación de distancia Manhattan.

**Fórmula:** h(n) = |x₁ - x₂| + |y₁ - y₂|

**Conceptos:**
- Admisible: nunca sobreestima (ignora paredes, distancia mínima posible)
- Consistente: cumple desigualdad triangular
- **Resultado tinyMaze**: Costo 10, **10 nodos** (vs 18 con h=0) → reducción 44%

---

### Punto 6 - Heurística Euclidiana
**Archivo:** `searchAgents.py` → `euclideanHeuristic()`

**Qué se hizo:** Implementación de distancia Euclidiana.

**Fórmula:** h(n) = √((x₁ - x₂)² + (y₁ - y₂)²)

**Conceptos:**
- Admisible y consistente
- **Resultado tinyMaze**: Igual que Manhattan (10 nodos)
- Manhattan preferible: modela exactamente movimientos 4-direccionales de Pac-Man

---

### Punto 7 - Problema de las Cuatro Esquinas (CornersProblem)
**Archivo:** `searchAgents.py` → `class CornersProblem`

**Qué se hizo:** Definición completa del problema de visita de esquinas.

**Representación del estado:**
```
estado = (posición_actual, esquinas_visitadas)
posición_actual = (x, y)
esquinas_visitadas = tupla de coordenadas ya visitadas
```

**Métodos implementados:**
- `getStartState()`: Posición inicial + esquinas visitadas al inicio
- `isGoalState()`: True si len(esquinas_visitadas) == 4
- `getSuccessors()`: Genera movimientos válidos, actualiza esquinas visitadas
- `getCostOfActions()`: Costo = número de acciones

**Resultado BFS tinyCorners**: Costo 22, 374 nodos expandidos, Victoria ✓

---

### Punto 8 - Heurística para Cuatro Esquinas
**Archivo:** `searchAgents.py` → `cornersHeuristic()`

**Qué se hizo:** Heurística admisible para CornersProblem.

**Fórmula:** h(n) = max{ dManhattan(pos_actual, esquina) | esquina ∉ visitadas }

**Conceptos:**
- **Admisible**: Manhattan ignora paredes → distancia mínima real
- **Consistente**: Cambia ≤ 1 por movimiento de costo 1
- **Resultado A* tinyCorners**: Costo 22, **124 nodos** (vs 374 BFS) → **reducción 66.8%**

---

### Punto 9 - Experimento Comparativo
**Archivo:** `RESULTADOS_EXPERIMENTOS.md`

**Qué se hizo:** Ejecución sistemática y tabulación de resultados.

**Tablas generadas:**
| Problema | Métodos comparados |
|----------|-------------------|
| tinyMaze (PositionSearch) | UCS, A*+h=0, A*+Manhattan, A*+Euclidiana |
| tinyCorners (CornersProblem) | UCS, A*+h=0, A*+cornersHeuristic |
| tinySearch (FoodSearch) | UCS, A*+h=0, A*+MaxManhattan, A*+MST |
| testClassic (FoodSearch) | UCS, A*+h=0, A*+MaxManhattan, **A*+MST** |

**Factor de reducción R = N_UCS / N_A*:**
- tinyMaze: 1.8x
- tinyCorners: 3.04x
- testClassic (MST): **23.4x**

---

### Punto 10 - Búsqueda de Todos los Alimentos (FoodSearchProblem)
**Archivo:** `searchAgents.py` → `class FoodSearchProblem` (ya existía)

**Qué se hizo:** Análisis del espacio de estados exponencial.

**Representación del estado:**
```
estado = (pacmanPosition, foodGrid)
pacmanPosition = (x, y)
foodGrid = Grid[Boolean] indicando comida restante
```

**Complejidad:** Si hay F alimentos → 2^F configuraciones posibles de foodGrid.

**Objetivo:** `foodGrid.count() == 0` (toda comida consumida)

---

### Punto 11 - Diseño de foodHeuristic
**Archivo:** `searchAgents.py` → `foodHeuristic()` y `foodHeuristicV2()`

**Qué se hizo:** Dos heurísticas para FoodSearchProblem con comparación.

#### Heurística 1: Max Manhattan Distance
```python
def foodHeuristic(state, problem):
    position, foodGrid = state
    foodList = foodGrid.asList()
    if not foodList: return 0
    return max(manhattanDistance(position, food) for food in foodList)
```
- **Idea**: Costo mínimo ≥ distancia al alimento más lejano
- **Admisible**: Sí
- **Resultado testClassic**: 702 nodos (3.7x reducción vs UCS)

#### Heurística 2: MST con Caché (Propuesta Ganadora)
```python
def foodHeuristicV2(state, problem):
    # Cache distancias entre pares en problem.heuristicInfo
    # minDistToFood + MST(alimentos_restantes)
```
- **Idea**: Costo ≈ ir al más cercano + conectar todos (MST)
- **Admisible**: MST es cota inferior del camino que visita todos
- **Optimización**: `problem.heuristicInfo['foodDistances']` cachea distancias pares
- **Resultado testClassic**: **111 nodos (23.4x reducción)**, **Victoria ✓**
- **Resultado smallClassic**: 10,882 nodos, 112.9s (vs timeout UCS)

---

## Cómo Ejecutar

```bash
cd PCMAN/PCMAN

# Punto 2 - UCS
python pacman.py -l tinyMaze -p SearchAgent -a fn=ucs --frameTime 0

# Punto 4 - A* con h=0
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=nullHeuristic --frameTime 0

# Punto 5 - A* Manhattan
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic --frameTime 0

# Punto 6 - A* Euclidiana
python pacman.py -l tinyMaze -p SearchAgent -a fn=astar,heuristic=euclideanHeuristic --frameTime 0

# Punto 7 - BFS Corners
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem --frameTime 0

# Punto 8 - A* Corners
python pacman.py -l tinyCorners -p SearchAgent -a fn=astar,prob=CornersProblem,heuristic=cornersHeuristic --frameTime 0

# Punto 10-11 - Food Search (usa foodHeuristicV2 = MST)
python pacman.py -l tinySearch -p AStarFoodSearchAgent --frameTime 0
python pacman.py -l testClassic -p AStarFoodSearchAgent --frameTime 0
python pacman.py -l smallClassic -p AStarFoodSearchAgent --frameTime 0
```

---

## Resultados Clave

| Métrica | UCS | A* (h=0) | A* (Manhattan) | A* (MST) |
|---------|-----|----------|----------------|----------|
| tinyMaze nodos | 18 | 18 | **10** | - |
| tinyCorners nodos | 377 | 377 | - | **124** |
| testClassic nodos | 2,598 | 2,598 | 702 | **111** |
| testClassic Victoria | ✗ | ✗ | ✗ | **✓** |

**Conclusión:** Heurísticas más informadas (admisibles) reducen drásticamente la exploración manteniendo optimalidad. MST con caché es la mejor para FoodSearchProblem.

---

## Autores
- Lina Castañeda
- Jorge García
- Brayan Hernandez

