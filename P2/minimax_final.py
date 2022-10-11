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