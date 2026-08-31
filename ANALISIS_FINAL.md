# Análisis Final - Taller Búsqueda Informada

## 1. ¿Cuál es la diferencia fundamental entre UCS y A*?
**UCS** usa solo el costo acumulado g(n) para priorizar nodos. **A*** usa f(n) = g(n) + h(n), donde h(n) es una heurística que estima el costo restante al objetivo. A* es "informado"; UCS es "no informado".

## 2. ¿Qué función cumple g(n)?
Representa el **costo real acumulado** desde el estado inicial hasta el nodo actual n. Es el costo del camino ya recorrido.

## 3. ¿Qué función cumple h(n)?
Es la **heurística**: una estimación del costo mínimo restante desde n hasta el objetivo. Debe ser admisible (nunca sobreestimar) para garantizar optimalidad.

## 4. ¿Qué ocurre cuando h(n) = 0?
A* se vuelve **equivalente a UCS**. f(n) = g(n) + 0 = g(n). Ambos expanden los mismos nodos y encuentran la misma solución (ver experimentos: 18 nodos en tinyMaze, 377 en tinyCorners).

## 5. ¿Cuál presentó mejores resultados: Manhattan o Euclidiana?
**Empate** en tinyMaze: ambas expandieron 10 nodos con costo 10. **Manhattan es preferible** porque modela exactamente los movimientos permitidos (4 direcciones, sin diagonales), mientras Euclidiana asume movimiento continuo.

## 6. ¿Una heurística más grande siempre es mejor? Justifique.
**No necesariamente.** Una heurística más grande (más informada) reduce nodos expandidos **solo si es admisible**. Si sobreestima (h(n) > h*(n)), A* puede perder optimalidad. Entre heurísticas admisibles, la que domina (h1 ≥ h2) expande ≤ nodos.

## 7. ¿Por qué una heurística que sobreestima puede ser problemática?
Si h(n) > h*(n) (costo real óptimo), A* puede **expandir nodos subóptimos primero** y encontrar una solución no óptima. Viola la garantía de optimalidad de A*.

## 8. ¿Por qué el estado de CornersProblem necesita almacenar más información que únicamente (x, y)?
Porque dos estados con la **misma posición (x,y)** pueden diferir en **qué esquinas ya fueron visitadas**. El estado debe ser `(posición, esquinas_visitadas)` para distinguir "estoy en (5,5) habiendo visitado 2 esquinas" vs "estoy en (5,5) habiendo visitado 3 esquinas".

## 9. ¿Por qué FoodSearchProblem presenta un espacio de estados considerablemente mayor?
El estado es `(pacmanPosition, foodGrid)`. Si hay F alimentos, cada uno puede estar `{presente, consumido}` → **2^F configuraciones** de foodGrid. Crecimiento exponencial vs. lineal en PositionSearchProblem.

## 10. ¿Qué relación encontró entre la calidad de la heurística y el número de nodos expandidos?
**Relación inversa fuerte**: 
- h=0 (nula): 2,598 nodos (testClassic)
- Max Manhattan: 702 nodos (3.7x reducción)
- **MST con caché: 111 nodos (23.4x reducción)**
Una heurística más informada (cercana a h* sin sobreestimar) **drásticamente reduce** la exploración manteniendo optimalidad.