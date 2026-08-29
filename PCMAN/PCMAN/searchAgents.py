"""
This file contains all of the agents that can be selected to 
control Pacman.  To select an agent, use the '-p' option
when running pacman.py.  Arguments can be passed to your agent
using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run:

> python pacman.py -p SearchAgent -a searchFunction=depthFirstSearch

Commands to invoke other search strategies can be found in the 
project description.

Please only change the parts of the file you are asked to.
Look for the lines that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the
project description for details.

Good luck and happy searching!
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search
import searchAgents


class GoWestAgent(Agent):
  "An agent that goes West until it can't."
  
  def getAction(self, state):
    "The agent receives a GameState (defined in pacman.py)."
    if Directions.WEST in state.getLegalPacmanActions():
      return Directions.WEST
    else:
      return Directions.STOP


#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
  """
  This very general search agent finds a path using a supplied search algorithm for a
  supplied search problem, then returns actions to follow that path.
  
  As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)
  
  Options for fn include:
    depthFirstSearch or dfs
    breadthFirstSearch or bfs
    uniformCostSearch or ucs
    aStarSearch or astar
  
  Note: You should NOT change any code in SearchAgent
  """
    
  def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
    # Get the search function from the name and heuristic
    if fn not in dir(search): 
      raise AttributeError(fn + ' is not a search function in search.py.')
    
    func = getattr(search, fn)
    
    if 'heuristic' not in func.__code__.co_varnames:
      print(('[SearchAgent] using function ' + fn)) 
      self.searchFunction = func
    
    else:
      if heuristic in dir(searchAgents):
        heur = getattr(searchAgents, heuristic)
      elif heuristic in dir(search):
        heur = getattr(search, heuristic)
      else:
        raise AttributeError(
            heuristic +
            ' is not a function in searchAgents.py or search.py.'
        )
      
      print(
          ('[SearchAgent] using function %s and heuristic %s'
           % (fn, heuristic))
      )
      
      self.searchFunction = lambda x: func(x, heuristic=heur)
      
    # Get the search problem type from the name
    if prob not in dir(searchAgents) or not prob.endswith('Problem'): 
      raise AttributeError(
          prob +
          ' is not a search problem type in SearchAgents.py.'
      )
    
    self.searchType = getattr(searchAgents, prob)
    
    print(('[SearchAgent] using problem type ' + prob)) 
    
  def registerInitialState(self, state):
    """
    This is the first time that the agent sees the layout of the game board.
    """
    
    if self.searchFunction is None:
      raise Exception("No search function provided for SearchAgent")
    
    starttime = time.time()
    
    problem = self.searchType(state)
    
    self.actions = self.searchFunction(problem)
    
    totalCost = problem.getCostOfActions(self.actions)
    
    print(
        ('Path found with total cost of %d in %.1f seconds'
         % (totalCost, time.time() - starttime))
    )
    
    if '_expanded' in dir(problem):
      print(('Search nodes expanded: %d' % problem._expanded))
    
  def getAction(self, state):
    """
    Returns the next action in the path chosen earlier.
    """
    
    if 'actionIndex' not in dir(self):
      self.actionIndex = 0
    
    i = self.actionIndex
    
    self.actionIndex += 1
    
    if i < len(self.actions):
      return self.actions[i]
    
    else:
      return Directions.STOP


class PositionSearchProblem(search.SearchProblem):
  """
  A search problem defines the state space, start state, goal test,
  successor function and cost function.
  
  The state space consists of (x,y) positions in a pacman game.
  
  Note: this search problem is fully specified; you should NOT change it.
  """
  
  def __init__(
      self,
      gameState,
      costFn=lambda x: 1,
      goal=(1,1),
      start=None,
      warn=True
  ):
    
    self.walls = gameState.getWalls()
    
    self.startState = gameState.getPacmanPosition()
    
    if start != None:
      self.startState = start
    
    self.goal = goal
    
    self.costFn = costFn
    
    if warn and (
        gameState.getNumFood() != 1 or
        not gameState.hasFood(*goal)
    ):
      print('Warning: this does not look like a regular search maze')

    # For display purposes
    self._visited, self._visitedlist, self._expanded = {}, [], 0

  def getStartState(self):
    return self.startState

  def isGoalState(self, state):
    isGoal = state == self.goal 
    
    # For display purposes only
    if isGoal:
      self._visitedlist.append(state)
      
      import __main__
      
      if '_display' in dir(__main__):
        if 'drawExpandedCells' in dir(__main__._display):
          __main__._display.drawExpandedCells(
              self._visitedlist
          )
       
    return isGoal   
   
  def getSuccessors(self, state):
    """
    Returns successor states, the actions they require, and a cost of 1.
    """
    
    successors = []
    
    for action in [
        Directions.NORTH,
        Directions.SOUTH,
        Directions.EAST,
        Directions.WEST
    ]:
      
      x, y = state
      
      dx, dy = Actions.directionToVector(action)
      
      nextx, nexty = int(x + dx), int(y + dy)
      
      if not self.walls[nextx][nexty]:
        
        nextState = (nextx, nexty)
        
        cost = self.costFn(nextState)
        
        successors.append(
            (nextState, action, cost)
        )
        
    # Bookkeeping for display purposes
    self._expanded += 1 
    
    if state not in self._visited:
      self._visited[state] = True
      self._visitedlist.append(state)
      
    return successors

  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.
    """
    
    if actions is None:
      return 999999
    
    x, y = self.getStartState()
    
    cost = 0
    
    for action in actions:
      
      dx, dy = Actions.directionToVector(action)
      
      x, y = int(x + dx), int(y + dy)
      
      if self.walls[x][y]:
        return 999999
      
      cost += self.costFn((x,y))
    
    return cost


class StayEastSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes
  being in positions on the West side of the board.
  """
  
  def __init__(self):
    
    self.searchFunction = search.uniformCostSearch
    
    costFn = lambda pos: .5 ** pos[0]
    
    self.searchType = lambda state: PositionSearchProblem(
        state,
        costFn
    )


class StayWestSearchAgent(SearchAgent):
  """
  An agent for position search with a cost function that penalizes
  being in positions on the East side of the board.
  """
  
  def __init__(self):
    
    self.searchFunction = search.uniformCostSearch
    
    costFn = lambda pos: 2 ** pos[0]
    
    self.searchType = lambda state: PositionSearchProblem(
        state,
        costFn
    )


#######################################################
# PUNTO 5 - HEURÍSTICA MANHATTAN
#######################################################

def manhattanHeuristic(position, problem, info={}):
  """
  Heurística de distancia Manhattan.

  Calcula la distancia entre la posición actual y el objetivo
  utilizando únicamente movimientos horizontales y verticales.

  h(n) = |x1 - x2| + |y1 - y2|
  """
  
  xy1 = position
  xy2 = problem.goal
  
  return (
      abs(xy1[0] - xy2[0]) +
      abs(xy1[1] - xy2[1])
  )


#######################################################
# PUNTO 6 - HEURÍSTICA EUCLIDIANA
#######################################################

def euclideanHeuristic(position, problem, info={}):
  """
  Heurística de distancia Euclidiana.

  Calcula la distancia directa entre la posición actual
  y el objetivo.

  h(n) = sqrt((x1-x2)^2 + (y1-y2)^2)
  """
  
  xy1 = position
  xy2 = problem.goal
  
  return (
      (xy1[0] - xy2[0]) ** 2 +
      (xy1[1] - xy2[1]) ** 2
  ) ** 0.5


#####################################################
# PUNTO 7 - PROBLEMA DE LAS CUATRO ESQUINAS
#####################################################

class CornersProblem(search.SearchProblem):
  """
  This search problem finds paths through all four corners of a layout.

  El estado se representa como:

      (posición_actual, esquinas_visitadas)

  donde:
      posición_actual = (x, y)
      esquinas_visitadas = tupla con las esquinas ya visitadas
  """
  
  def __init__(self, startingGameState):
    """
    Stores the walls, pacman's starting position and corners.
    """
    
    self.walls = startingGameState.getWalls()
    
    self.startingPosition = (
        startingGameState.getPacmanPosition()
    )
    
    top = self.walls.height - 2
    right = self.walls.width - 2
    
    self.corners = (
        (1,1),
        (1,top),
        (right,1),
        (right,top)
    )
    
    for corner in self.corners:
      if not startingGameState.hasFood(*corner):
        print(
            'Warning: no food in corner ' +
            str(corner)
        )
    
    self._expanded = 0


  def getStartState(self):
    """
    Returns the start state.

    El estado inicial contiene la posición de Pac-Man
    y las esquinas que ya hayan sido visitadas.
    """
    
    visited = ()
    
    if self.startingPosition in self.corners:
      visited = (self.startingPosition,)
    
    return (
        self.startingPosition,
        visited
    )


  def isGoalState(self, state):
    """
    Returns True cuando las cuatro esquinas han sido visitadas.
    """
    
    currentPosition, visited = state
    
    return len(visited) == len(self.corners)


  def getSuccessors(self, state):
    """
    Returns successor states, the actions they require,
    and a cost of 1.
    """
    
    successors = []
    
    currentPosition, visited = state
    
    for action in [
        Directions.NORTH,
        Directions.SOUTH,
        Directions.EAST,
        Directions.WEST
    ]:
      
      x, y = currentPosition
      
      dx, dy = Actions.directionToVector(action)
      
      nextx = int(x + dx)
      nexty = int(y + dy)
      
      # Verificar que no exista una pared
      if not self.walls[nextx][nexty]:
        
        nextPosition = (
            nextx,
            nexty
        )
        
        # Copiar las esquinas ya visitadas
        nextVisited = list(visited)
        
        # Si llegamos a una esquina, la registramos
        if (
            nextPosition in self.corners and
            nextPosition not in nextVisited
        ):
          nextVisited.append(nextPosition)
        
        # Convertimos nuevamente a tupla
        # para que el estado sea hashable
        nextVisited = tuple(nextVisited)
        
        nextState = (
            nextPosition,
            nextVisited
        )
        
        successors.append(
            (
                nextState,
                action,
                1
            )
        )
    
    self._expanded += 1
    
    return successors


  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.
    If the actions contain an illegal move, return 999999.
    """
    
    if actions is None:
      return 999999
    
    x, y = self.startingPosition
    
    for action in actions:
      
      dx, dy = Actions.directionToVector(action)
      
      x, y = int(x + dx), int(y + dy)
      
      if self.walls[x][y]:
        return 999999
    
    return len(actions)


#####################################################
# PUNTO 8 - HEURÍSTICA DE LAS CUATRO ESQUINAS
#####################################################

def cornersHeuristic(state, problem):
  """
  Heurística para el problema de las cuatro esquinas.

  Se calcula la distancia Manhattan desde la posición
  actual hasta cada esquina que todavía no ha sido visitada.

  Se toma como heurística la mayor de esas distancias.

  h(n) = max(distancia Manhattan a esquina pendiente)

  Esta heurística es admisible porque la distancia Manhattan
  ignora las paredes y representa una distancia mínima.
  """
  
  corners = problem.corners
  
  currentPosition, visited = state
  
  visited = set(visited)
  
  # Obtener las esquinas que aún faltan
  remainingCorners = [
      corner
      for corner in corners
      if corner not in visited
  ]
  
  # Si no quedan esquinas, ya estamos en el objetivo
  if not remainingCorners:
    return 0
  
  # Calcular las distancias Manhattan
  distances = [
      util.manhattanDistance(
          currentPosition,
          corner
      )
      for corner in remainingCorners
  ]
  
  # La mayor distancia representa una cota inferior
  return max(distances)


class AStarCornersAgent(SearchAgent):
  """
  A SearchAgent for CornersProblem using A*
  and cornersHeuristic.
  """
  
  def __init__(self):
    
    self.searchFunction = lambda prob: search.aStarSearch(
        prob,
        cornersHeuristic
    )
    
    self.searchType = CornersProblem


#######################################################
# PROBLEMA DE COMIDA
#######################################################

class FoodSearchProblem:
  """
  A search problem associated with finding a path
  that collects all of the food.
  """
  
  def __init__(self, startingGameState):
    
    self.start = (
        startingGameState.getPacmanPosition(),
        startingGameState.getFood()
    )
    
    self.walls = startingGameState.getWalls()
    
    self.startingGameState = startingGameState
    
    self._expanded = 0
    
    self.heuristicInfo = {}
      
  def getStartState(self):
    return self.start
  
  def isGoalState(self, state):
    return state[1].count() == 0

  def getSuccessors(self, state):
    """
    Returns successor states, the actions they require,
    and a cost of 1.
    """
    
    successors = []
    
    self._expanded += 1
    
    for direction in [
        Directions.NORTH,
        Directions.SOUTH,
        Directions.EAST,
        Directions.WEST
    ]:
      
      x, y = state[0]
      
      dx, dy = Actions.directionToVector(direction)
      
      nextx, nexty = int(x + dx), int(y + dy)
      
      if not self.walls[nextx][nexty]:
        
        nextFood = state[1].copy()
        
        nextFood[nextx][nexty] = False
        
        successors.append(
            (
                ((nextx, nexty), nextFood),
                direction,
                1
            )
        )
    
    return successors

  def getCostOfActions(self, actions):
    """
    Returns the cost of a particular sequence of actions.
    """
    
    x, y = self.getStartState()[0]
    
    cost = 0
    
    for action in actions:
      
      dx, dy = Actions.directionToVector(action)
      
      x, y = int(x + dx), int(y + dy)
      
      if self.walls[x][y]:
        return 999999
      
      cost += 1
    
    return cost


class AStarFoodSearchAgent(SearchAgent):
  """
  A SearchAgent for FoodSearchProblem using A*
  and foodHeuristic.
  """
  
  def __init__(self):
    
    self.searchFunction = lambda prob: search.aStarSearch(
        prob,
        foodHeuristic
    )
    
    self.searchType = FoodSearchProblem


def foodHeuristic(state, problem):
  """
  Heurística para FoodSearchProblem.

  Esta función corresponde a una actividad posterior.
  """
  
  position, foodGrid = state
  
  return 0


class ClosestDotSearchAgent(SearchAgent):
  """
  Search for all food using a sequence of searches
  """
  
  def registerInitialState(self, state):
    
    self.actions = []
    
    currentState = state
    
    while currentState.getFood().count() > 0:
      
      nextPathSegment = self.findPathToClosestDot(
          currentState
      )
      
      self.actions += nextPathSegment
      
      for action in nextPathSegment:
        
        legal = currentState.getLegalActions()
        
        if action not in legal:
          
          t = (
              str(action),
              str(currentState)
          )
          
          raise Exception(
              'findPathToClosestDot returned an illegal move: %s!\n%s'
              % t
          )
        
        currentState = currentState.generateSuccessor(
            0,
            action
        )
    
    self.actionIndex = 0
    
    print(
        'Path found with cost %d.' %
        len(self.actions)
    )
    
  def findPathToClosestDot(self, gameState):
    """
    Returns a path to the closest dot.
    """
    
    startPosition = gameState.getPacmanPosition()
    
    food = gameState.getFood()
    
    walls = gameState.getWalls()
    
    problem = AnyFoodSearchProblem(gameState)
    
    return search.bfs(problem)


class AnyFoodSearchProblem(PositionSearchProblem):
  """
  A search problem for finding a path to any food.
  """
  
  def __init__(self, gameState):
    
    self.food = gameState.getFood()
    
    self.walls = gameState.getWalls()
    
    self.startState = gameState.getPacmanPosition()
    
    self.costFn = lambda x: 1
    
    self._visited, self._visitedlist, self._expanded = {}, [], 0
    
  def isGoalState(self, state):
    """
    Returns True if the current position contains food.
    """
    
    x, y = state
    
    return self.food[x][y]


##################
# Mini-contest 1 #
##################

class ApproximateSearchAgent(Agent):
  """
  Implement your contest entry here.
  """
  
  def registerInitialState(self, state):
    self.actions = []
    
  def getAction(self, state):
    return Directions.STOP


def mazeDistance(point1, point2, gameState):
  """
  Returns the maze distance between any two points,
  using BFS.
  """
  
  x1, y1 = point1
  x2, y2 = point2
  
  walls = gameState.getWalls()
  
  assert not walls[x1][y1], (
      'point1 is a wall: ' +
      str(point1)
  )
  
  assert not walls[x2][y2], (
      'point2 is a wall: ' +
      str(point2)
  )
  
  prob = PositionSearchProblem(
      gameState,
      start=point1,
      goal=point2,
      warn=False
  )
  
  return len(search.bfs(prob))
