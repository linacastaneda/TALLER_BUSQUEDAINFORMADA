"""
medir_memoria.py

Mide la memoria pico utilizada por los algoritmos de búsqueda
de Pacman utilizando tracemalloc.

Se realizan 10 ejecuciones por prueba y se calcula:
- Memoria mínima
- Memoria máxima
- Memoria promedio
- Tiempo promedio
- Nodos expandidos promedio
- Costo encontrado
"""

import subprocess
import sys
import os
import re
import statistics
import json


# ============================================================
# CONFIGURACIÓN
# ============================================================

NUM_EJECUCIONES = 10

PYTHON = sys.executable

MEDIDOR_INTERNO = "medicion_interna.py"


# ============================================================
# PRUEBAS
# ============================================================

PRUEBAS = [

    {
        "nombre": "UCS - tinyMaze",
        "layout": "tinyMaze",
        "fn": "ucs",
        "prob": "PositionSearchProblem",
        "heuristic": None
    },

    {
        "nombre": "A* h=0 - tinyMaze",
        "layout": "tinyMaze",
        "fn": "astar",
        "prob": "PositionSearchProblem",
        "heuristic": "ZERO"
    },

    {
        "nombre": "A* Manhattan - tinyMaze",
        "layout": "tinyMaze",
        "fn": "astar",
        "prob": "PositionSearchProblem",
        "heuristic": "manhattanHeuristic"
    },

    {
        "nombre": "A* Euclidiana - tinyMaze",
        "layout": "tinyMaze",
        "fn": "astar",
        "prob": "PositionSearchProblem",
        "heuristic": "euclideanHeuristic"
    },

    {
        "nombre": "UCS - tinyCorners",
        "layout": "tinyCorners",
        "fn": "ucs",
        "prob": "CornersProblem",
        "heuristic": None
    },

    {
        "nombre": "A* h=0 - tinyCorners",
        "layout": "tinyCorners",
        "fn": "astar",
        "prob": "CornersProblem",
        "heuristic": "ZERO"
    },

    {
        "nombre": "A* cornersHeuristic - tinyCorners",
        "layout": "tinyCorners",
        "fn": "astar",
        "prob": "CornersProblem",
        "heuristic": "cornersHeuristic"
    },

    {
        "nombre": "UCS - tinySearch",
        "layout": "tinySearch",
        "fn": "ucs",
        "prob": "FoodSearchProblem",
        "heuristic": None
    },

    {
        "nombre": "A* h=0 - tinySearch",
        "layout": "tinySearch",
        "fn": "astar",
        "prob": "FoodSearchProblem",
        "heuristic": "ZERO"
    },

    {
        "nombre": "A* Max Manhattan - tinySearch",
        "layout": "tinySearch",
        "fn": "astar",
        "prob": "FoodSearchProblem",
        "heuristic": "foodHeuristic"
    },

    {
        "nombre": "A* MST - tinySearch",
        "layout": "tinySearch",
        "fn": "astar",
        "prob": "FoodSearchProblem",
        "heuristic": "foodHeuristicV2"
    },

]


# ============================================================
# CÓDIGO DEL MEDIDOR INTERNO
# ============================================================

CODIGO_INTERNO = r'''
import sys
import time
import tracemalloc

import pacman
import search
import searchAgents
import layout


# ============================================================
# RECIBIR ARGUMENTOS
# ============================================================

layout_name = sys.argv[1]
fn_name = sys.argv[2]
prob_name = sys.argv[3]
heuristic_name = sys.argv[4]


# ============================================================
# CARGAR LAYOUT
# ============================================================

lay = layout.getLayout(layout_name)

if lay is None:
    print("ERROR_LAYOUT")
    sys.exit(1)


# ============================================================
# CREAR GAMESTATE
# ============================================================

gameState = pacman.GameState()

gameState.initialize(lay, 0)


# ============================================================
# OBTENER FUNCIÓN DE BÚSQUEDA
# ============================================================

func = getattr(search, fn_name)


# ============================================================
# CREAR PROBLEMA
# ============================================================

problemClass = getattr(searchAgents, prob_name)

problem = problemClass(gameState)


# ============================================================
# CONFIGURAR FUNCIÓN DE BÚSQUEDA
# ============================================================

if heuristic_name == "NONE":

    def searchFunction(problem):
        return func(problem)


elif heuristic_name == "ZERO":

    # Heurística h(n) = 0.
    # Se utiliza como referencia para comparar A*
    # sin información heurística.

    def zeroHeuristic(state, problem=None):
        return 0

    def searchFunction(problem):
        return func(
            problem,
            heuristic=zeroHeuristic
        )


else:

    # Primero buscar en searchAgents.py
    if hasattr(searchAgents, heuristic_name):

        heuristic = getattr(
            searchAgents,
            heuristic_name
        )

    # Si no está allí, buscar en search.py
    elif hasattr(search, heuristic_name):

        heuristic = getattr(
            search,
            heuristic_name
        )

    else:

        raise AttributeError(
            "No se encontró la heurística: "
            + heuristic_name
        )

    def searchFunction(problem):
        return func(
            problem,
            heuristic=heuristic
        )


# ============================================================
# MEDICIÓN
# ============================================================

tracemalloc.start()

inicio = time.perf_counter()

acciones = searchFunction(problem)

fin = time.perf_counter()

current, peak = tracemalloc.get_traced_memory()

tracemalloc.stop()


# ============================================================
# CALCULAR RESULTADOS
# ============================================================

tiempo = fin - inicio


try:

    costo = problem.getCostOfActions(
        acciones
    )

except Exception:

    costo = -1


expandidos = getattr(
    problem,
    "_expanded",
    -1
)


memoria_kb = peak / 1024.0


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

print(
    "RESULTADO|"
    + str(memoria_kb)
    + "|"
    + str(tiempo)
    + "|"
    + str(expandidos)
    + "|"
    + str(costo)
)
'''


# ============================================================
# CREAR ARCHIVO TEMPORAL
# ============================================================

with open(
    MEDIDOR_INTERNO,
    "w",
    encoding="utf-8"
) as archivo:

    archivo.write(CODIGO_INTERNO)


# ============================================================
# EJECUTAR UNA PRUEBA
# ============================================================

def ejecutar_prueba(prueba):

    memorias = []
    tiempos = []
    expandidos = []
    costos = []

    print()
    print("=" * 75)
    print(prueba["nombre"])
    print("=" * 75)

    for ejecucion in range(
        1,
        NUM_EJECUCIONES + 1
    ):

        heuristic = prueba["heuristic"]

        if heuristic is None:
            heuristic = "NONE"


        comando = [

            PYTHON,

            MEDIDOR_INTERNO,

            prueba["layout"],

            prueba["fn"],

            prueba["prob"],

            heuristic

        ]


        try:

            resultado = subprocess.run(

                comando,

                capture_output=True,

                text=True,

                timeout=180

            )

        except subprocess.TimeoutExpired:

            print(
                f"Ejecución {ejecucion}: TIMEOUT"
            )

            continue


        salida = resultado.stdout


        coincidencia = re.search(

            r"RESULTADO\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)",

            salida

        )


        if not coincidencia:

            print(
                f"Ejecución {ejecucion}: ERROR"
            )

            if resultado.stderr:

                print(
                    resultado.stderr
                )

            continue


        memoria = float(
            coincidencia.group(1)
        )

        tiempo = float(
            coincidencia.group(2)
        )

        nodos = int(
            float(
                coincidencia.group(3)
            )
        )

        costo = int(
            float(
                coincidencia.group(4)
            )
        )


        memorias.append(
            memoria
        )

        tiempos.append(
            tiempo
        )

        expandidos.append(
            nodos
        )

        costos.append(
            costo
        )


        print(

            f"Ejecución {ejecucion:2d}: "

            f"{memoria:10.2f} KB | "

            f"{tiempo:8.4f} s | "

            f"{nodos:6d} nodos | "

            f"costo {costo}"

        )


    # ========================================================
    # VERIFICAR RESULTADOS
    # ========================================================

    if not memorias:

        print()
        print(
            "No se obtuvieron resultados válidos."
        )

        return None


    # ========================================================
    # CALCULAR PROMEDIOS
    # ========================================================

    resultado_final = {

        "nombre": prueba["nombre"],

        "memoria_min":
            min(memorias),

        "memoria_max":
            max(memorias),

        "memoria_promedio":
            statistics.mean(memorias),

        "tiempo_promedio":
            statistics.mean(tiempos),

        "nodos_promedio":
            statistics.mean(expandidos),

        "costo":
            costos[0],

        "ejecuciones_validas":
            len(memorias)

    }


    # ========================================================
    # MOSTRAR RESUMEN
    # ========================================================

    print()

    print(
        f"MEMORIA PROMEDIO: "
        f"{resultado_final['memoria_promedio']:.2f} KB"
    )

    print(
        f"MEMORIA MÍNIMA:   "
        f"{resultado_final['memoria_min']:.2f} KB"
    )

    print(
        f"MEMORIA MÁXIMA:   "
        f"{resultado_final['memoria_max']:.2f} KB"
    )

    print(
        f"TIEMPO PROMEDIO:  "
        f"{resultado_final['tiempo_promedio']:.4f} s"
    )

    print(
        f"NODOS PROMEDIO:   "
        f"{resultado_final['nodos_promedio']:.1f}"
    )

    print(
        f"EJECUCIONES:      "
        f"{resultado_final['ejecuciones_validas']}/"
        f"{NUM_EJECUCIONES}"
    )


    return resultado_final


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

resultados = []


print()
print("=" * 75)
print("       MEDICIÓN REAL DE MEMORIA - PACMAN")
print("=" * 75)
print()

print(
    f"Ejecuciones por prueba: "
    f"{NUM_EJECUCIONES}"
)

print(
    "Medición: memoria pico de Python mediante tracemalloc"
)

print()


for prueba in PRUEBAS:

    resultado = ejecutar_prueba(
        prueba
    )

    if resultado is not None:

        resultados.append(
            resultado
        )


# ============================================================
# GUARDAR RESULTADOS EN JSON
# ============================================================

with open(
    "resultados_memoria.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(

        resultados,

        archivo,

        indent=4,

        ensure_ascii=False

    )


# ============================================================
# TABLA FINAL
# ============================================================

print()
print()

print("=" * 120)
print("TABLA FINAL")
print("=" * 120)


print(

    f"{'Prueba':40} "

    f"{'Mem. promedio':15} "

    f"{'Mem. min':12} "

    f"{'Mem. max':12} "

    f"{'Tiempo':12} "

    f"{'Nodos':10}"

)


print("-" * 120)


for r in resultados:

    print(

        f"{r['nombre']:40} "

        f"{r['memoria_promedio']:12.2f} KB "

        f"{r['memoria_min']:10.2f} KB "

        f"{r['memoria_max']:10.2f} KB "

        f"{r['tiempo_promedio']:10.4f} s "

        f"{r['nodos_promedio']:8.1f}"

    )


# ============================================================
# INFORMACIÓN FINAL
# ============================================================

print()
print(
    "Archivo generado:"
)

print(
    "resultados_memoria.json"
)

print()


# ============================================================
# ELIMINAR ARCHIVO TEMPORAL
# ============================================================

try:

    os.remove(
        MEDIDOR_INTERNO
    )

except Exception:

    pass
