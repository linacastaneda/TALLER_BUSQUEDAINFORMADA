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
 
     This method returns the total cost of a particular sequence of actions. 
     The sequence must be composed of legal moves
     """
     util.raiseNotDefined()


def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first.

  Uses a Stack, which follows a LIFO policy.
  """

  frontier = util.Stack()
  start = problem.getStartState()

  frontier.push((start, []))
  visited = set()

  while not frontier.isEmpty():

    state, actions = frontier.pop()

    if state in visited:
      continue

    visited.add(state)

    if problem.isGoalState(state):
      return actions

    for successor, action, stepCost in problem.getSuccessors(state):
      if successor not in visited:
        frontier.push((successor, actions + [action]))

  return []


def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.

  Uses a Queue, which follows a FIFO policy.
  """

  frontier = util.Queue()
  start = problem.getStartState()

  frontier.push((start, []))
  visited = set()

  while not frontier.isEmpty():

    state, actions = frontier.pop()

    if state in visited:
      continue

    visited.add(state)

    if problem.isGoalState(state):
      return actions

    for successor, action, stepCost in problem.getSuccessors(state):
      if successor not in visited:
        frontier.push((successor, actions + [action]))

  return []


def uniformCostSearch(problem):
  """
  Search the node of least total cost first.

  Uses a PriorityQueue where the priority is the accumulated
  path cost g(n).
  """

  frontier = util.PriorityQueue()
  start = problem.getStartState()

  # (state, actions, cost)
  counter = 0
  frontier.push((start, [], 0), (0, counter))

  visited = set()

  while not frontier.isEmpty():

    state, actions, cost = frontier.pop()

    if state in visited:
      continue

    visited.add(state)

    if problem.isGoalState(state):
      return actions

    for successor, action, stepCost in problem.getSuccessors(state):

      if successor not in visited:

        newCost = cost + stepCost
        counter += 1

        frontier.push(
            (successor, actions + [action], newCost),
            (newCost, counter)
        )

  return []


def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0


def aStarSearch(problem, heuristic=nullHeuristic):
  """
  Search the node that has the lowest combined cost and heuristic first.

  f(n) = g(n) + h(n)

  where:
    g(n) = cost accumulated from the start state
    h(n) = estimated cost from the current state to the goal
  """

  frontier = util.PriorityQueue()
  start = problem.getStartState()

  initialHeuristic = heuristic(start, problem)

  # (state, actions, cost)
  counter = 0
  frontier.push(
      (start, [], 0),
      (initialHeuristic, counter)
  )

  visited = set()

  while not frontier.isEmpty():

    state, actions, cost = frontier.pop()

    if state in visited:
      continue

    visited.add(state)

    if problem.isGoalState(state):
      return actions

    for successor, action, stepCost in problem.getSuccessors(state):

      if successor not in visited:

        newCost = cost + stepCost

        h = heuristic(successor, problem)

        priority = newCost + h

        counter += 1
        frontier.push(
            (successor, actions + [action], newCost),
            (priority, counter)
        )

  return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
