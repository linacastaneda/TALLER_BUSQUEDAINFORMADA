import subprocess
import sys
import json
import os
import re


# ============================================================
# CONFIGURACIÓN
# ============================================================

NUM_EJECUCIONES = 10


# ============================================================
# PRUEBAS
# ============================================================

PRUEBAS = [
    {
        "nombre": "UCS - tinyMaze",
        "layout": "tinyMaze",
        "problem": "PositionSearchProblem",
        "algoritmo": "uniformCostSearch",
        "heuristica": "NONE"
    },

    {
        "nombre": "A* h=0 - tinyMaze",
        "layout": "tinyMaze",
        "problem": "PositionSearchProblem",
        "algoritmo": "aStarSearch",
        "heuristica": "nullHeuristic"
    },

    {
        "nombre": "A* Manhattan - tinyMaze",
        "layout": "tinyMaze",
        "problem": "PositionSearchProblem",
        "algoritmo": "aStarSearch",
        "heuristica": "manhattanHeuristic"
    },

    {
        "nombre": "A* Euclidiana - tinyMaze",
        "layout": "tinyMaze",
        "problem": "PositionSearchProblem",
        "algoritmo": "aStarSearch",
        "heuristica": "euclideanHeuristic"
    },

    {
        "nombre": "UCS - tinyCorners",
        "layout": "tinyCorners",
        "problem": "CornersProblem",
        "algoritmo": "uniformCostSearch",
        "heuristica": "NONE"
    },

    {
        "nombre": "A* h=0 - tinyCorners",
        "layout": "tinyCorners",
        "problem": "CornersProblem",
        "algoritmo": "aStarSearch",
        "heuristica": "nullHeuristic"
    },

    {
        "nombre": "A* cornersHeuristic - tinyCorners",
        "layout": "tinyCorners",
        "problem": "CornersProblem",
        "algoritmo": "aStarSearch",
        "heuristica": "cornersHeuristic"
    },

    {
        "nombre": "UCS - tinySearch",
        "layout": "tinySearch",
        "problem": "FoodSearchProblem",
        "algoritmo": "uniformCostSearch",
        "heuristica": "NONE"
    },

    {
        "nombre": "A* h=0 - tinySearch",
        "layout": "tinySearch",
        "problem": "FoodSearchProblem",
        "algoritmo": "aStarSearch",
        "heuristica": "nullHeuristic"
    },

    {
        "nombre": "A* Max Manhattan - tinySearch",
        "layout": "tinySearch",
        "problem": "FoodSearchProblem",
        "algoritmo": "aStarSearch",
        "heuristica": "foodHeuristic"
    },

    {
        "nombre": "A* MST - tinySearch",
        "layout": "tinySearch",
        "problem": "FoodSearchProblem",
        "algoritmo": "aStarSearch",
        "heuristica": "foodHeuristicV2"
    }
]


# ============================================================
# CÓDIGO INTERNO QUE SE EJECUTA EN CADA PRUEBA
# ============================================================

CODIGO_INTERNO = r'''
import tracemalloc
import time
import sys

import pacman
import search
import searchAgents
import layout


layout_name = "__LAYOUT__"
problem_name = "__PROBLEM__"
algorithm_name = "__ALGORITHM__"
heuristic_name = "__HEURISTIC__"


# ------------------------------------------------------------
# Obtener algoritmo
# ------------------------------------------------------------

func = getattr(search, algorithm_name)


# ------------------------------------------------------------
# Obtener heurística
#
# nullHeuristic está en search.py
# Las demás heurísticas están en searchAgents.py
# ------------------------------------------------------------

if heuristic_name != "NONE":

    if hasattr(searchAgents, heuristic_name):
        heuristic = getattr(searchAgents, heuristic_name)

    elif hasattr(search, heuristic_name):
        heuristic = getattr(search, heuristic_name)

    else:
        raise AttributeError(
            "No se encontró la heurística '"
            + heuristic_name
            + "' ni en searchAgents.py ni en search.py."
        )

    def searchFunction(problem):
        return func(problem, heuristic=heuristic)

else:

    def searchFunction(problem):
        return func(problem)


# ------------------------------------------------------------
# Cargar layout
# ------------------------------------------------------------

lay = layout.getLayout(layout_name)

if lay is None:
    raise Exception(
        "No se pudo cargar el layout: " + layout_name
    )


# ------------------------------------------------------------
# Crear problema
# ------------------------------------------------------------

if problem_name == "PositionSearchProblem":

    problem = searchAgents.PositionSearchProblem(
        lay,
        warn=False,
        visualize=False
    )

elif problem_name == "CornersProblem":

    problem = searchAgents.CornersProblem(
        lay,
        warn=False,
        visualize=False
    )

elif problem_name == "FoodSearchProblem":

    problem = searchAgents.FoodSearchProblem(
        lay,
        warn=False,
        visualize=False
    )

else:

    raise Exception(
        "Problema desconocido: " + problem_name
    )


# ------------------------------------------------------------
# Medición real de memoria
#
# Se mide únicamente la memoria Python utilizada durante
# la ejecución del algoritmo de búsqueda.
# ------------------------------------------------------------

tracemalloc.start()

inicio = time.perf_counter()

resultado = searchFunction(problem)

fin = time.perf_counter()

memoria_actual, memoria_pico = tracemalloc.get_traced_memory()

tracemalloc.stop()


# ------------------------------------------------------------
# Obtener costo
# ------------------------------------------------------------

costo = problem.getCostOfActions(resultado)


# ------------------------------------------------------------
# Obtener cantidad de nodos expandidos
# ------------------------------------------------------------

nodos = getattr(problem, "_expanded", 0)


# ------------------------------------------------------------
# Convertir memoria a KB
# ------------------------------------------------------------

memoria_kb = memoria_pico / 1024.0


# ------------------------------------------------------------
# Resultado
# ------------------------------------------------------------

print(
    "RESULTADO|"
    + str(memoria_kb)
    + "|"
    + str(fin - inicio)
    + "|"
    + str(nodos)
    + "|"
    + str(costo)
)
'''


# ============================================================
# FUNCIÓN PARA EJECUTAR UNA PRUEBA
# ============================================================

def ejecutar_prueba(prueba):

    resultados = []

    print()
    print("=" * 70)
    print(prueba["nombre"])
    print("=" * 70)

    for i in range(1, NUM_EJECUCIONES + 1):

        codigo = CODIGO_INTERNO

        codigo = codigo.replace(
            "__LAYOUT__",
            prueba["layout"]
        )

        codigo = codigo.replace(
            "__PROBLEM__",
            prueba["problem"]
        )

        codigo = codigo.replace(
            "__ALGORITHM__",
            prueba["algoritmo"]
        )

        codigo = codigo.replace(
            "__HEURISTIC__",
            prueba["heuristica"]
        )

        archivo_interno = "medicion_interna.py"

        try:

            with open(
                archivo_interno,
                "w",
                encoding="utf-8"
            ) as archivo:

                archivo.write(codigo)


            proceso = subprocess.run(
                [
                    sys.executable,
                    archivo_interno
                ],
                capture_output=True,
                text=True,
                timeout=180
            )


            salida = proceso.stdout.strip()
            error = proceso.stderr.strip()


            # ------------------------------------------------
            # Buscar resultado
            # ------------------------------------------------

            coincidencia = re.search(
                r"RESULTADO\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)",
                salida
            )


            if coincidencia:

                memoria = float(
                    coincidencia.group(1)
                )

                tiempo = float(
                    coincidencia.group(2)
                )

                nodos = float(
                    coincidencia.group(3)
                )

                costo = float(
                    coincidencia.group(4)
                )


                resultados.append(
                    {
                        "memoria": memoria,
                        "tiempo": tiempo,
                        "nodos": nodos,
                        "costo": costo
                    }
                )


                print(
                    f"Ejecución {i:2d}: "
                    f"{memoria:10.2f} KB | "
                    f"{tiempo:8.4f} s | "
                    f"{nodos:6.0f} nodos | "
                    f"costo {costo:g}"
                )


            else:

                print(
                    f"Ejecución {i}: ERROR"
                )

                if error:
                    print(error)

                elif salida:
                    print(salida)

                else:
                    print(
                        "No se recibió ninguna salida."
                    )


        except subprocess.TimeoutExpired:

            print(
                f"Ejecución {i}: TIMEOUT "
                f"(más de 180 segundos)"
            )


        except Exception as e:

            print(
                f"Ejecución {i}: ERROR"
            )

            print(str(e))


    # --------------------------------------------------------
    # Eliminar archivo temporal
    # --------------------------------------------------------

    if os.path.exists("medicion_interna.py"):

        try:
            os.remove("medicion_interna.py")

        except Exception:
            pass


    # --------------------------------------------------------
    # Calcular estadísticas
    # --------------------------------------------------------

    if not resultados:

        print()
        print("No se obtuvieron resultados.")

        return None


    memorias = [
        r["memoria"]
        for r in resultados
    ]

    tiempos = [
        r["tiempo"]
        for r in resultados
    ]

    nodos = [
        r["nodos"]
        for r in resultados
    ]

    costos = [
        r["costo"]
        for r in resultados
    ]


    memoria_promedio = sum(memorias) / len(memorias)

    memoria_minima = min(memorias)

    memoria_maxima = max(memorias)

    tiempo_promedio = sum(tiempos) / len(tiempos)

    nodos_promedio = sum(nodos) / len(nodos)

    costo_promedio = sum(costos) / len(costos)


    print()

    print(
        f"MEMORIA PROMEDIO: "
        f"{memoria_promedio:.2f} KB"
    )

    print(
        f"MEMORIA MÍNIMA:   "
        f"{memoria_minima:.2f} KB"
    )

    print(
        f"MEMORIA MÁXIMA:   "
        f"{memoria_maxima:.2f} KB"
    )

    print(
        f"TIEMPO PROMEDIO:  "
        f"{tiempo_promedio:.4f} s"
    )

    print(
        f"NODOS PROMEDIO:   "
        f"{nodos_promedio:.1f}"
    )


    return {
        "nombre": prueba["nombre"],
        "memoria_min": memoria_minima,
        "memoria_max": memoria_maxima,
        "memoria_promedio": memoria_promedio,
        "tiempo_promedio": tiempo_promedio,
        "nodos_promedio": nodos_promedio,
        "costo": costo_promedio,
        "ejecuciones_validas": len(resultados)
    }


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print()
    print("=" * 60)
    print("   MEDICIÓN REAL DE MEMORIA - PACMAN")
    print("=" * 60)

    print()
    print(
        f"Ejecuciones por prueba: "
        f"{NUM_EJECUCIONES}"
    )

    print(
        "Medición: memoria pico de Python "
        "mediante tracemalloc"
    )

    resultados_finales = []


    # --------------------------------------------------------
    # Ejecutar todas las pruebas
    # --------------------------------------------------------

    for prueba in PRUEBAS:

        resultado = ejecutar_prueba(
            prueba
        )

        if resultado is not None:

            resultados_finales.append(
                resultado
            )


    # --------------------------------------------------------
    # Tabla final
    # --------------------------------------------------------

    print()
    print()
    print("=" * 110)
    print("TABLA FINAL")
    print("=" * 110)

    print(
        f"{'Prueba':40s} "
        f"{'Mem. promedio':>15s} "
        f"{'Mem. min':>13s} "
        f"{'Mem. max':>13s} "
        f"{'Tiempo':>12s} "
        f"{'Nodos':>10s}"
    )

    print("-" * 110)


    for resultado in resultados_finales:

        print(
            f"{resultado['nombre']:40s} "
            f"{resultado['memoria_promedio']:10.2f} KB "
            f"{resultado['memoria_min']:10.2f} KB "
            f"{resultado['memoria_max']:10.2f} KB "
            f"{resultado['tiempo_promedio']:9.4f} s "
            f"{resultado['nodos_promedio']:9.1f}"
        )


    # --------------------------------------------------------
    # Guardar JSON
    # --------------------------------------------------------

    archivo_json = "resultados_memoria.json"

    with open(
        archivo_json,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            resultados_finales,
            archivo,
            indent=4,
            ensure_ascii=False
        )


    print()
    print()
    print(
        "Archivo generado:"
    )

    print(
        archivo_json
    )


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":
    main()
