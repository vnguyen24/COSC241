# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""
import game
import searchAgents
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, step_cost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'step_cost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


"""function Depth-First-Search(problem) returns a solution, or failure"""

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    node = Node(state=problem.getStartState(), past_action=None, path_cost=0, past_node=None)

    if problem.isGoalState(node.state):
        return []

    frontier = util.Stack()  # A stack of nodes
    frontier.push(node)
    explored = set()

    while True:
        if frontier.isEmpty():
            return False
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return past_actions(node)
        if node.state not in explored:
            explored.add(node.state)
            for successor_state, action, step_cost in problem.getSuccessors(node.state):
                child_node = Node(state=successor_state, past_action=action, path_cost=node.path_cost + step_cost,
                                  past_node=node)
                frontier.push(child_node)


"""function BREADTH-FIRST-SEARCH(problem) returns a solution, or failure"""

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    node = Node(state=problem.getStartState(), past_action=None, path_cost=0, past_node=None)
    if problem.isGoalState(node.state):
        return []
    frontier = util.Queue()
    frontier.push(node)
    explored = set()

    while True:
        if frontier.isEmpty():
            return False
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return past_actions(node)
        if node.state not in explored:
            explored.add(node.state)
            for successor_state, action, step_cost in problem.getSuccessors(node.state):
                child_node = Node(state=successor_state, past_action=action, path_cost=node.path_cost + step_cost,
                                  past_node=node)
                frontier.push(child_node)


"""function UNIFORM-COST-SEARCH(problem) returns a solution, or failure"""

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    node = Node(state=problem.getStartState(), past_action=None, path_cost=0, past_node=None)
    frontier = util.PriorityQueue()
    frontier.push(node, node.path_cost)
    explored = set()

    while True:
        if frontier.isEmpty():
            return False
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return past_actions(node)
        if node.state not in explored:
            explored.add(node.state)
            for successor_state, action, step_cost in problem.getSuccessors(node.state):
                child_node = Node(state=successor_state, past_action=action, path_cost=node.path_cost + step_cost,
                                  past_node=node)
                frontier.push(child_node, child_node.path_cost)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    node = Node(state=problem.getStartState(), past_action=None, path_cost=0, past_node=None)
    frontier = util.PriorityQueue()
    frontier.push(node, node.path_cost + heuristic(node.state, problem))
    explored = set()

    while True:
        if frontier.isEmpty():
            return False
        node = frontier.pop()
        if problem.isGoalState(node.state):
            return past_actions(node)
        if node.state not in explored:
            explored.add(node.state)
            for successor_state, action, step_cost in problem.getSuccessors(node.state):
                child_node = Node(state=successor_state, past_action=action, path_cost=node.path_cost + step_cost,
                                  past_node=node)
                frontier.push(child_node, child_node.path_cost + heuristic(child_node.state, problem))


"""
Returns a path to the goal state as a list of actions.

Travels up from the node whose state is the goal state through all the previous nodes, adding each past_action attribute
to the list, in reverse.
"""

def past_actions(node):
    list_of_actions = []
    while (node.past_action != None):
        list_of_actions.insert(0, node.past_action)
        node = node.past_node
    return list_of_actions


"""The Node object stores the state, path cost, and the previous node and action for each node."""

class Node:

    def __init__(self, state, past_action, path_cost, past_node):
        self.state = state
        self.past_action = past_action
        self.path_cost = path_cost
        self.past_node = past_node


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch