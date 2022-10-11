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


def CHANCE(self, gameState, agent_index, depth):
    if gameState.isWin() or gameState.isLose() or depth == self.depth:
        # print(f"stop condition met. State has utility {self.evaluationFunction(state)}")
        return self.evaluationFunction(gameState), None
    utility_list = []
    action_list = []
    for action in gameState.getLegalActions(agent_index):
        utility = self.expectimax(gameState.generateSuccessor(agent_index, action), agent_index + 1, depth)[0]
        utility_list.append(utility),
        action_list.append(action)
    # Calculate average utility
    utility_sum = 0
    for u in utility_list:
        utility_sum += u
    avg_utility = utility_sum / len(utility_list)
    # Calculate the difference between an action's utility and the average sum
    utility_difference_list = []
    for u in utility_list:
        utility_difference_list.append(u - avg_utility)
    # Finding the index of the smallest difference
    smallest_difference = float("inf")
    idx = 0
    for index in range(len(utility_difference_list)):
        if utility_difference_list[index] < smallest_difference:
            smallest_difference = utility_difference_list[index]
            idx = index
    return (utility_list[idx], action_list[idx])