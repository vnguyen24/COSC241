# SHORT VERSION: ALL CODE IN ONE FUNCTION

def minimax(self, gameState, agent_index, depth):
    # If agent_index is not an actual agent, reset turn to Pacman and increment depth
    if agent_index == gameState.getNumAgents():
        # print("All agents have moved this turn. Next agent to move should be Pacman")
        agent_index = 0
        depth += 1
    # Subtlety: Need to increment depth before checking terminal and cutoff test. If reversed, will explore 1
    # more depth than expected. Intuition: If there are 2 agents (0 and 1), agent_index = 2 (which doesn't exist)
    # is actually Pacman will have 2 turns in the same depth.
    # Check terminal state and cut off test. If met, calculate utility with evaluation function
    if gameState.isWin() or gameState.isLose() or depth == self.depth:
        # print("Stop condition met")
        # print(f"Utility at this stop state is {self.evaluationFunction(game_state)}")
        return self.evaluationFunction(gameState), None
    # Pacman case
    if agent_index == 0:
        best = (float("-inf"), None)
        for action in gameState.getLegalActions(agent_index):
            # print(f"agent {agent_index} doing {action}")
            action_utility = (
                self.minimax(gameState.generateSuccessor(agent_index, action), agent_index + 1, depth)[0], action)
            # print(f"First action is {best[1]} with utility {best[0]}")
            # print(f"Second action is {action_utility[1]} with utility {action_utility[0]}")
            best = max(best, action_utility)
            # print(f"the better action is {best[1]} with utility {best[0]}")
        # print(f"best action is {best[1]} with utility {best[0]}")
        return best
    # A ghost case
    else:
        best = (float("inf"), None)
        for action in gameState.getLegalActions(agent_index):
            # print(f"agent {agent_index} doing {action}")
            action_utility = (
                self.minimax(gameState.generateSuccessor(agent_index, action), agent_index + 1, depth)[0], action)
            # print(f"First action is {best[1]} with utility {best[0]}")
            # print(f"Second action is {action_utility[1]} with utility {action_utility[0]}")
            best = min(best, action_utility)
            # print(f"the better action is {best[1]} with utility {best[0]}")
        # print(f"best action is {best[1]} with utility {best[0]}")
        return best