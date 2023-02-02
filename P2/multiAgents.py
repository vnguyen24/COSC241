# multiAgents.py
# --------------
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
import sys

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # Idea: Pacman should be as far away from the closest ghost as possible, while being as close to the nearest
        # food dot as possible
        new_ghost_positions = successorGameState.getGhostPositions()
        original_food = currentGameState.getFood().asList()
        # If Pacman and a ghost collide while ghost is not scared, return -1
        for ghost_index in range(len(new_ghost_positions)):
            if new_ghost_positions[ghost_index] == newPos and newScaredTimes[ghost_index] == 0:
                return -1
        # If Pacman moves to a location with a food dot, return 1. Note that there is one caveat: Because we are looking
        # into the future, if Pacman moves to a food dot, the food dot will not be in newFood (in this future the dot
        # is eaten). Therefore, we need the original food grid
        for food_pos in original_food:
            if newPos == food_pos:
                return 1
        # Calculate evaluation. Intuition: Want to be close to a food dot, far from a ghost. Here we can use
        # newFood since the case above didn't happen, but it shouldn't make a difference
        min_food = float("inf")
        min_ghost = float("inf")
        for food_pos in original_food:
            distance = util.manhattanDistance(newPos, food_pos)
            if distance < min_food:
                min_food = distance
        for ghost_pos in new_ghost_positions:
            distance = util.manhattanDistance(newPos, ghost_pos)
            if distance < min_ghost:
                min_ghost = distance
        # Intuition: Close to food is food, close to ghost is bad
        return (1 / min_food) - (1 / min_ghost)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # print(f"there are {gameState.getNumAgents()} agents")
        return self.minimax(gameState, 0, 0)[1]

    # THE USE OF AGENT_INDEX IS INSPIRED BY TINA ZHANG - A STUDENT OUTSIDE OF OUR CLASS. SHE GAVE ME THE HINT OF
    # KEEPING TRACK OF AN INDEX INSTEAD OF KEEPING TRACK OF AN ARRAY.
    def minimax(self, gameState, agent_index, depth):
        if agent_index == gameState.getNumAgents():
            # print("All agents have moved. Increasing depth")
            agent_index = 0
            depth += 1
        if agent_index == 0:
            return self.MAX(gameState, agent_index, depth)
        else:
            return self.MIN(gameState, agent_index, depth)

    def MAX(self, gameState, agent_index, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            # print(f"stop condition met. State has utility {self.evaluationFunction(state)}")
            return self.evaluationFunction(gameState), None
        best = (float("-inf"), None)
        for action in gameState.getLegalActions(agent_index):
            action_utility = (
                self.minimax(gameState.generateSuccessor(agent_index, action), agent_index + 1, depth)[0], action)
            best = max(best, action_utility)
        return best

    def MIN(self, gameState, agent_index, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            # print(f"stop condition met. State has utility {self.evaluationFunction(state)}")
            return self.evaluationFunction(gameState), None
        best = (float("inf"), None)
        for action in gameState.getLegalActions(agent_index):
            action_utility = (
                self.minimax(gameState.generateSuccessor(agent_index, action), agent_index + 1, depth)[0], action)
            best = min(best, action_utility)
        return best


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        utility, action = self.alphabeta(gameState)
        # print(f"Pacman will choose action {action} with {utility}")
        return action

    def alphabeta(self, state, agent_index=0, depth=0, alpha=float("-inf"), beta=float("inf")):
        if agent_index == state.getNumAgents():
            # print("All agents have moved. Increasing depth")
            agent_index = 0
            depth += 1
        if agent_index == 0:
            # print("It is Pacman's turn")
            return self.MAX(state, agent_index, depth, alpha, beta)
        else:
            # print("It is a ghost turn")
            return self.MIN(state, agent_index, depth, alpha, beta)

    def MAX(self, state, agent_index, depth, a, b):
        if state.isWin() or state.isLose() or depth == self.depth:
            # print(f"stop condition met. State has utility {self.evaluationFunction(state)}")
            return self.evaluationFunction(state), None
        v = (float("-inf"), None)
        for action in state.getLegalActions(agent_index):
            v = max(v,
                    (self.alphabeta(state.generateSuccessor(agent_index, action), agent_index + 1, depth, a, b)[0],
                     action))
            # print(f"The higher utility is {v[0]}")
            # THE PSEUDOCODE MIGHT BE INCORRECT HERE. IT SHOULD BE >. I FAILED THE TIED ROOT TEST WITH >=
            if v[0] > b:
                # print(f"v[0] {v[0]} is greater than or equal to b {b}, so we prune")
                return v
            a = max(a, v[0])
            # print(f"highest utility seen so far is a {a}")
        # print(f"Pacman will choose utility between {a} and {b}")
        return v

    def MIN(self, state, agent_index, depth, a, b):
        if state.isWin() or state.isLose() or depth == self.depth:
            # print(f"stop condition met. State has utility {self.evaluationFunction(state)}")
            return self.evaluationFunction(state), None
        v = (float("inf"), None)
        for action in state.getLegalActions(agent_index):
            v = min(v,
                    (self.alphabeta(state.generateSuccessor(agent_index, action), agent_index + 1, depth, a, b)[0],
                     action))
            # print(f"The lower utility is {v[0]}")
            # THE PSEUDOCODE MIGHT BE INCORRECT HERE. IT SHOULD BE <. I FAILED THE TIED ROOT TEST WITH <=
            if v[0] < a:
                # print(f"v[0] {v[0]} is smaller than or equal to a {a}, so we prune")
                return v
            b = min(b, v[0])
            # print(f"lowest utility seen so far is b {b}")
        # print(f"Ghost will choose utility between {a} and {b}")
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState)[1]

    def expectimax(self, gameState, agent_index=0, depth=0):
        if agent_index == gameState.getNumAgents():
            # print("All agents have moved. Increasing depth")
            agent_index = 0
            depth += 1
        if agent_index == 0:
            return self.MAX(gameState, agent_index, depth)
        else:
            return self.CHANCE(gameState, agent_index, depth)

    def MAX(self, gameState, agent_index, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            # print(f"stop condition met. State has utility {self.evaluationFunction(state)}")
            return self.evaluationFunction(gameState), None
        best = (float("-inf"), None)
        for action in gameState.getLegalActions(agent_index):
            action_utility = (
                self.expectimax(gameState.generateSuccessor(agent_index, action), agent_index + 1, depth)[0], action)
            best = max(best, action_utility)
        return best

    # Q: WHAT'S THE DIFFERENCE BETWEEN THIS FUNCTION AND EXPECTIMAX_CLOSEST_TO_AVERAGE?
    def CHANCE(self, gameState, agent_index, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            # print(f"stop condition met. State has utility {self.evaluationFunction(state)}")
            return self.evaluationFunction(gameState), None
        actions = gameState.getLegalActions(agent_index)
        # Choose an action at random
        selected_action = actions[random.randrange(0, len(actions), 1)]
        # Calculate average (expected) utility
        total_utility = 0.0
        for action in actions:
            total_utility += self.expectimax(gameState.generateSuccessor(agent_index, action), agent_index + 1, depth)[
                0]
        # Since distribution is uniform, ok to divide at the end
        avg_utility = total_utility / len(actions)
        return avg_utility, selected_action


def betterEvaluationFunction(currentGameState):
    """
    DESCRIPTION: Calculates the distance to the closest ghost, the number
    of remaining pieces of food, and the distance to the closest piece of
    food.


    """
    "*** YOUR CODE HERE ***"
    current_food = currentGameState.getFood().asList()
    current_position = currentGameState.getPacmanPosition()
    current_ghost_states = currentGameState.getGhostStates()
    current_scared_times = [ghost_state.scaredTimer for ghost_state in current_ghost_states]
    current_ghost_positions = currentGameState.getGhostPositions()
    # Things I might also need
    # getNumAgents()
    # getCapsules()
    # isLose()
    # isWin()

    if currentGameState.isWin():
        return 99999999999999
    if currentGameState.isLose():
        return -99999999999999
    min_food = float("inf")
    food_remaining = len(current_food)
    total_scared_time = sum(current_scared_times)
    score = currentGameState.getScore()
    capsules = currentGameState.getCapsules()
    capsule_count = 0
    for capsule in capsules:
        if capsule:
            capsule_count += 1
    for food_pos in current_food:
        distance = util.manhattanDistance(current_position, food_pos)
        min_food = min(min_food, distance)
    return - min_food - food_remaining + score - 100 * capsule_count - total_scared_time


# Abbreviation
better = betterEvaluationFunction
