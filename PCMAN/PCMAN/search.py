"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  # La frontera guarda los estados que faltan por explorar.
  frontier = util.PriorityQueue()

  # Estado inicial del problema.
  startState = problem.getStartState()

  # Contador para evitar problemas cuando dos nodos tienen la misma prioridad.
  counter = 0

  # Cada elemento contiene:
  # contador, estado, acciones realizadas y costo acumulado.
  frontier.push((counter, startState, [], 0), 0)

  # Guarda el menor costo conocido para llegar a cada estado.
  bestCosts = {startState: 0}

  while not frontier.isEmpty():

    # Se extrae el nodo con menor costo acumulado.
    _, state, actions, cost = frontier.pop()

    # Ignora una entrada si ya se encontró un camino más barato.
    if cost != bestCosts.get(state):
      continue

    # Si se alcanzó el objetivo, retorna el camino.
    if problem.isGoalState(state):
      return actions

    # Explora los movimientos posibles desde el estado actual.
    for successor, action, stepCost in problem.getSuccessors(state):

      newCost = cost + stepCost

      # Solamente guarda el sucesor si encontró un camino más barato.
      if newCost < bestCosts.get(successor, float('inf')):

        bestCosts[successor] = newCost
        newActions = actions + [action]

        counter += 1
        frontier.push(
          (counter, successor, newActions, newCost),
          newCost
        )

  # Se retorna una lista vacía si no existe solución.
  return []

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."

  # Cola de prioridad utilizada como frontera.
  frontier = util.PriorityQueue()

  # Estado inicial del problema.
  startState = problem.getStartState()

  # Contador para diferenciar nodos con la misma prioridad.
  counter = 0

  # El costo real inicial g(n) es 0.
  startCost = 0

  # La prioridad inicial es:
  # f(n) = g(n) + h(n)
  startPriority = startCost + heuristic(startState, problem)

  frontier.push(
    (counter, startState, [], startCost),
    startPriority
  )

  # Menor costo conocido para llegar a cada estado.
  bestCosts = {startState: 0}

  while not frontier.isEmpty():

    # Extraer el nodo con menor f(n).
    _, state, actions, cost = frontier.pop()

    # Ignorar entradas para las que ya existe un camino más barato.
    if cost != bestCosts.get(state):
      continue

    # Comprobar si se alcanzó el objetivo.
    if problem.isGoalState(state):
      return actions

    # Obtener los sucesores del estado actual.
    for successor, action, stepCost in problem.getSuccessors(state):

      # Calcular el nuevo costo real g(n).
      newCost = cost + stepCost

      # Comprobar si este camino mejora el costo conocido.
      if newCost < bestCosts.get(successor, float('inf')):

        bestCosts[successor] = newCost
        newActions = actions + [action]

        # Calcular la prioridad de A*:
        # f(n) = g(n) + h(n)
        priority = newCost + heuristic(successor, problem)

        counter += 1

        frontier.push(
          (counter, successor, newActions, newCost),
          priority
        )

  # Retornar una lista vacía si no existe solución.
  return []
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch