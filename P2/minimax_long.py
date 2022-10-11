# LONG VERSION: HAVE SEPARATE MAX AND MIN FUNCTIONS FOR PACMAN AND THE GHOSTS

def minimax(self, gameState, agent_index, depth):
    # print(f"agent is now {agent_index}")
    # If agent_index is not an actual agent, reset turn to Pacman and increment depth
    if agent_index == gameState.getNumAgents():
        # print("All agents have moved this turn. Next agent to move should be Pacman")
        agent_index = 0
        depth += 1
    # Pacman case
    if agent_index == 0:
        return self.MAX(gameState, agent_index, depth)
    # A ghost case
    else:
        return self.MIN(gameState, agent_index, depth)


def MAX(self, game_state, agent_index, depth):
    # Check terminal state and cut off test. If met, calculate utility with evaluation function
    if game_state.isWin() or game_state.isLose() or depth == self.depth:
        # print("Stop condition met")
        # print(f"Utility at this stop state is {self.evaluationFunction(game_state)}")
        return self.evaluationFunction(game_state), None

    best = (float("-inf"), None)
    for action in game_state.getLegalActions(agent_index):
        # print(f"agent {agent_index} doing {action}")
        action_utility = (
            self.minimax(game_state.generateSuccessor(agent_index, action), agent_index + 1, depth)[0], action)
        # print(f"First action is {best[1]} with utility {best[0]}")
        # print(f"Second action is {action_utility[1]} with utility {action_utility[0]}")
        best = max(best, action_utility)
        # print(f"the better action is {best[1]} with utility {best[0]}")
    # print(f"best action is {best[1]} with utility {best[0]}")
    return best


def MIN(self, game_state, agent_index, depth):
    # Check terminal state and cut off test. If met, calculate utility with evaluation function
    if game_state.isWin() or game_state.isLose() or depth == self.depth:
        # print("Stop condition met")
        # print(f"Utility at this state is {self.evaluationFunction(game_state)}")
        return self.evaluationFunction(game_state), None

    best = (float("inf"), None)
    for action in game_state.getLegalActions(agent_index):
        # print(f"agent {agent_index} doing {action}")
        action_utility = (
            self.minimax(game_state.generateSuccessor(agent_index, action), agent_index + 1, depth)[0], action)
        # print(f"First action is {best[1]} with utility {best[0]}")
        # print(f"Second action is {action_utility[1]} with utility {action_utility[0]}")
        best = min(best, action_utility)
        # print(f"the better action is {best[1]} with utility {best[0]}")
    # print(f"best action is {best[1]} with utility {best[0]}")
    return best
