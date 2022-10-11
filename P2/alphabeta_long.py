# LONG VERSION: HAVE SEPARATE MAX AND MIN FUNCTIONS FOR PACMAN AND THE GHOSTS

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