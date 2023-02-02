# Don't get killed on enemy side
# Don't run away from scared ghosts
# if scared, both agents should do defense OR both agents do offense

# OldTeam.py
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game, capture
from util import nearestPoint


#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='HybridAgent', second='HybridAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.  isRed is True if the red team is being created, and
    will be False if the blue team is being created.

    As a potentially helpful development aid, this function can take
    additional string-valued keyword arguments ("first" and "second" are
    such arguments in the case of this function), which will come from
    the --redOpts and --blueOpts command-line arguments to capture.py.
    For the contest, however, your team will be created without
    any extra arguments, so you should make sure that the default
    behavior is what you want for the nightly contest.
    """

    # The following line is an example only; feel free to change it.
    return [eval(first)(firstIndex), eval(second)(secondIndex)]


##########
# Agents #
##########

class HybridAgent(CaptureAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState: capture.GameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).

        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)

        IMPORTANT: This method may run for at most 15 seconds.
        """

        '''
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        '''
        CaptureAgent.registerInitialState(self, gameState)

        '''
        Your initialization code goes here, if you need any.
        '''
        self.start = gameState.getAgentPosition(self.index)

    def chooseAction(self, gameState: capture.GameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        actions = gameState.getLegalActions(self.index)  # All possible actions of this agent
        remaining_actions = actions.copy()  # Categorically bad decisions will be removed from remaining_actions
        boundary_line = (gameState.data.layout.width - 2) // 2
        current_pos = gameState.getAgentPosition(self.index)
        my_scared_timer = gameState.data.agentStates[self.index].scaredTimer

        # Used for an earlier strategy. The idea is that our PacMan agent should not eat food if there are ghosts
        # nearby, since most food pellets lie in corners where the ghost can trap PacMan.
        # ghost_distance = 10000

        # Below are hard-coded cases agents always have to perform
        # This for-loop tells the agent what to do if an opponent is nearby
        for opponent in self.getOpponents(gameState):
            opponent_pos = gameState.getAgentPosition(opponent)
            distance = self.getMazeDistance(current_pos, opponent_pos)
            enemy_scared_timer = gameState.data.agentStates[opponent].scaredTimer

            if distance <= 4:  # Currently set to 4 or less, though what counts as "nearby" can be changed
                # Covers instances where our agent is running from a ghost or (itself scared) is running from PacMan
                # print("near ghost")
                if (self.onEnemySide(opponent_pos, boundary_line) and enemy_scared_timer == 0) or (
                        self.onOurSide(opponent_pos, boundary_line) and my_scared_timer > 0):
                    for action in remaining_actions:
                        # If only one action remains, go ahead and return it
                        if len(remaining_actions) == 1:
                            return remaining_actions[0]

                        successor = self.getSuccessor(gameState, action)
                        new_pos = successor.getAgentState(self.index).getPosition()
                        new_distance = self.getMazeDistance(new_pos, opponent_pos)

                        # If being chased by a ghost and carrying food, always return to our side if the option exists
                        if self.onOurSide(new_pos, boundary_line) and gameState.getAgentState(self.index).numCarrying>0:
                            return action

                        if new_distance > distance:
                            return action

                        # While being chased, never take an action that moves our agent closer to the enemy
                        if new_distance < distance:
                            remaining_actions.remove(action)
                            continue

                        # # Checks for nearby walls to prevent being cornered
                        # x = int(new_pos[0])
                        # y = int(new_pos[1])
                        # walls_nearby = 0
                        # if (gameState.hasWall(x + 1, y)):
                        #     walls_nearby += 1
                        # if (gameState.hasWall(x, y + 1)):
                        #     walls_nearby += 1
                        # if (gameState.hasWall(x - 1, y)):
                        #     walls_nearby += 1
                        # if (gameState.hasWall(x, y - 1)):
                        #     walls_nearby += 1
                        #
                        # # If being chased, never take an action that corners our agent
                        # if walls_nearby == 3:
                        #     remaining_actions.remove(action)

                # Commands agent to chase enemy PacMan if not scared
                # Against baselineTeam, this code works exceptionally well (baselineTeam has not been able to win)
                elif self.onOurSide(opponent_pos, boundary_line):
                    for action in remaining_actions:
                        successor = self.getSuccessor(gameState, action)
                        new_pos = successor.getAgentState(self.index).getPosition()
                        new_distance = self.getMazeDistance(new_pos, opponent_pos)

                        # Take whatever action decreases the distance to PacMan
                        if new_distance < distance:
                            return action
                elif self.onEnemySide(opponent_pos, boundary_line):
                    for action in remaining_actions:
                        successor = self.getSuccessor(gameState, action)
                        new_pos = successor.getAgentState(self.index).getPosition()
                        if new_pos == opponent_pos:
                            return action
            # Remnant of earlier strategy, kept here for reference
            # if self.onEnemySide(opponent_pos, boundary_line) and enemy_scared_timer == 0:
            #     ghost_distance = min(ghost_distance, distance)

        # Generally, nothing is gained by stopping, so we remove this action if possible
        if len(remaining_actions) > 1:
            remaining_actions.remove("Stop")

        # A matrix of whether food exists at a given location (opponent's side only)
        food_matrix = self.getFood(gameState)

        # This for-loop ensures if there is food one step away, our PacMan agent must eat it
        for action in remaining_actions:
            x, y = self.getSuccessor(gameState, action).getAgentState(self.index).getPosition()
            # If the action would cause food to be consumed, eliminate all actions that do not
            if food_matrix[int(x)][int(y)]:
                return action
                # Remnant of earlier strategy, kept here for reference
                # if ghost_distance <= 3 and len(remaining_actions) > 1:
                #     remaining_actions.remove(action)
                #     continue

                # Eliminates all other actions that do not involve consuming food
                # for other_action in remaining_actions:
                #     if other_action != action:
                #         other_x, other_y = self.getSuccessor(gameState, other_action).getAgentState(
                #             self.index).getPosition()
                #         if not food_matrix[int(other_x)][int(other_y)]:
                #             remaining_actions.remove(other_action)

        # If only one action remains, go ahead and return it
        if len(remaining_actions) == 1:
            return remaining_actions[0]

        # You can profile your evaluation time by uncommenting these lines
        # start = time.time()
        values = [self.evaluate(gameState, a) for a in remaining_actions]  # All Q values of remaining_actions
        # print('eval time for agent %d: %.4f' % (self.index, time.time() - start))

        maxValue = max(values)  # Highest Q value
        bestActions = [a for a, v in zip(actions, values) if
                       v == maxValue]  # Best actions that correspond to max Q value

        return random.choice(bestActions)

    def getSuccessor(self, gameState: capture.GameState, action):  # When a ghost takes 1 step, Pacman takes 0.5 steps
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState: capture.GameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights

    def getFeatures(self, gameState: capture.GameState, action):
        """
        Returns a counter of features for the state
        """
        """
        Features that we want to have at each state:

        * OFFENSE SPECIFIC *
        1. Successor score
        2. Distance to closest boundary: Intuitively, the more dots we have, the more important it is to go back. In
        other words, we want to be closer to the boundary (weight should be negative to penalize being far away). This
        feature multiplies distance to the boundary by the food carried by our agent
        3. Distance to nearest food: If the food is close, we should grab it (weight should be negative to penalize the
        food for being far away)
        4. Distance to nearest capsule: If the capsule is close, we should grab it (negative weight)
        5. Distance to closest ghost: We want to stay as far away as possible
        6. Number of food left: If there's a small number of food dots left, it's less lucrative to attack.
        If there are only 2 food dots left, call Pacman back immediately

        * DEFENSE SPECIFIC *
        7. Distance to enemy Pacman: We should chase and kill the Pacman on our side. If our agent is scared, it should
        keep a healthy distance from PacMan so it can kill him when the timer hits 0.
        8. Distance to our side's capsule: If there is no enemy PacMan, defend the capsule. Intuitively, PacMan is far
        weaker if he cannot reach the capsule. If the enemy agent is programmed to prioritize the capsule or the capsule
        is near many food dots, this feature has the added benefit of making it easy to get close to PacMan.
        """

        features = util.Counter()
        # Shared variables
        successor = self.getSuccessor(gameState, action)  # After taking an action, this is the state we end up in
        my_pos = successor.getAgentState(self.index).getPosition()
        food_list = self.getFood(successor).asList()
        capsule_list = self.getCapsules(successor)
        my_scared_timer = successor.getAgentState(self.index).scaredTimer
        # Successor score
        features['successor_score'] = -len(food_list)

        # Number of food this agent is carrying
        features["food_carrying"] = successor.getAgentState(self.index).numCarrying

        # Distance to the closest boundary
        # Create the boundary
        if self.red:
            boundary_line = (gameState.data.layout.width - 2) // 2
        else:
            boundary_line = ((gameState.data.layout.width - 2) // 2) + 1
        boundary = []
        for i in range(1, gameState.data.layout.height - 1):
            if not gameState.hasWall(boundary_line, i):
                boundary.append((boundary_line, i))

        # Compute distance to closest boundary location
        min_dist_to_boundary = min([self.getMazeDistance(my_pos, boundary_pos) for boundary_pos in boundary])
        features["dist_to_boundary"] = min_dist_to_boundary

        # After this point, boundary_line is only useful for passing to the onOurSide() and onEnemySide() functions,
        # which account for whether we are red or blue
        boundary_line = (gameState.data.layout.width - 2) // 2

        # Distance to nearest food
        if len(food_list) > 2:
            min_dist_to_food = min([self.getMazeDistance(my_pos, food) for food in food_list])
            features["dist_to_food"] = min_dist_to_food
        else:
            features["dist_to_food"] = 0  # If carrying enough food to win, we should prioritize returning to our side

        # Distance to nearest capsule
        if len(capsule_list) > 0 and len(food_list) > 2:
            min_dist_to_capsule = min([self.getMazeDistance(my_pos, capsule) for capsule in capsule_list])
            features["dist_to_capsule"] = min_dist_to_capsule

        # Distance to closest ghost - Assuming that they don't move for simplicity
        ghostDistances = []  # Collection of all distances to ghosts that are not scared

        # Fills ghostDistances with the distance to each ghost that is not scared
        for opponent in self.getOpponents(successor):
            opponent_pos = gameState.getAgentPosition(opponent)
            if self.onEnemySide(opponent_pos, boundary_line):
                distance = self.getMazeDistance(my_pos, opponent_pos)
                # Only includes distance in ghostDistances if the ghost is not scared or
                # might not remain scared by the time our agent could eat it
                if gameState.data.agentStates[opponent].scaredTimer > 6:  # 6 and not 0 to make time to get away
                    ghostDistances.append(distance)

        if len(ghostDistances) != 0:
            min_dist_to_ghost = min(ghostDistances)
            features["dist_to_ghost"] = min_dist_to_ghost
            # if min_dist_to_ghost < 12:  # Exact value can be changed; should also be changed below
            #     # Ensures min_dist_to_ghost punishes our PacMan agent for getting closer
            #     features["dist_to_ghost"] = 12 - min_dist_to_ghost
            # else:
            #     features["dist_to_ghost"] = 0  # If far away from all ghosts, this feature's value is set to 0

        # Number of food left
        features["food_left"] = max(len(food_list) - 2, 0)

        # Distance to enemy Pacman

        min_distance = -1

        # This for-loop gets the distance to the closest enemy PacMan and how much food he's carrying
        for opponent in self.getOpponents(successor):
            opponent_pos = gameState.getAgentPosition(opponent)
            if self.onOurSide(opponent_pos, boundary_line):
                distance = self.getMazeDistance(my_pos, opponent_pos)
                if min_distance == -1 or min_distance < distance:
                    min_distance = distance

        if min_distance != -1:
            # If this agent is not scared, defense should kill PacMan, especially if he's carrying a lot of food
            if my_scared_timer == 0:
                features["dist_to_enemy_pacman"] = min_distance
            # If scared, defense should keep a healthy distance from the enemy
            else:
                features["dist_to_enemy_pacman"] = abs(2 - min_distance)
            features["dist_to_our_capsule"] = 0
        else:
            # If there are no enemy PacMan's, defense goes to our team's capsule
            features["dist_to_enemy_pacman"] = 0
            for capsule in successor.getCapsules():
                if self.onOurSide(capsule, boundary_line):
                    features["dist_to_our_capsule"] = max(self.getMazeDistance(my_pos, capsule) - 2, 0)
                    break

        return features

    def getWeights(self, gameState, action):
        """
        Normally, weights do not depend on the gamestate.  They can be either
        a counter or a dictionary.
        """

        successor = self.getSuccessor(gameState, action)
        my_pos = successor.getAgentPosition(self.index)
        num_carrying = successor.getAgentState(self.index).numCarrying
        is_offensive = True  # Determines which agent is Offense and which is Defense
        #defensive_agent_created = False
        boundary_line = (gameState.data.layout.width - 2) // 2

        if successor.getAgentState(self.index).scaredTimer == 0:
            for opponent in self.getOpponents(gameState):
                opponent_pos = gameState.getAgentState(opponent).getPosition()
                if self.nearOrOnOurSide(opponent_pos, boundary_line):
                    for teammate in self.getTeam(gameState):
                        if teammate != self.index:
                            team_pos = gameState.getAgentState(teammate).getPosition()
                            my_dist = self.getMazeDistance(my_pos, opponent_pos)
                            team_dist = self.getMazeDistance(team_pos, opponent_pos)
                            if my_dist < team_dist:
                                is_offensive = False
                                #defensive_agent_created = True

        # if not defensive_agent_created:
        #     if self.red:
        #         for team_mate in successor.getRedTeamIndices():
        #             if team_mate != self.index:
        #                 if successor.getAgentPosition(self.index)[0] < successor.getAgentPosition(team_mate)[0]:
        #                     is_offensive = False
        #     else:
        #         for team_mate in successor.getBlueTeamIndices():
        #             if team_mate != self.index:
        #                 if successor.getAgentPosition(self.index)[0] > successor.getAgentPosition(team_mate)[0]:
        #                     is_offensive = False

        if is_offensive:
            dist_to_food_weight = -1
            food_left_weight = -100
            dist_to_ghost_weight = 30
            dist_to_boundary_weight = - 2 * num_carrying

            # When (all) enemies are scared
            enemy_scared_timer = 40  # Will be set equal to the smallest scared_timer, even if one enemy is not scared
            for opponent in self.getOpponents(gameState):
                enemy_scared_timer = min(gameState.data.agentStates[opponent].scaredTimer, enemy_scared_timer)

            # When enemy ghosts are scared, our goal is to race to get food then race back
            if enemy_scared_timer > 12:
                scaler = -1 + (6 - enemy_scared_timer) / 20
                dist_to_food_weight = scaler
                food_left_weight = scaler
                dist_to_ghost_weight = 0
                dist_to_boundary_weight = 0

            # Weights for the offensive agent
            return {"successor_score": 0, "food_carrying": 0, "dist_to_boundary": dist_to_boundary_weight,
                    "dist_to_food": dist_to_food_weight, "dist_to_capsule": -10, "dist_to_ghost": dist_to_ghost_weight,
                    "food_left": food_left_weight, "dist_to_enemy_pacman": 0, "dist_to_our_capsule": 0}

        # Weights for the defensive agent
        return {"successor_score": 0, "food_carrying": 0, "dist_to_boundary": 0, "dist_to_food": 0,
                "dist_to_capsule": 0, "dist_to_ghost": 0, "food_left": 0, "dist_to_enemy_pacman": -15,
                "dist_to_our_capsule": -1}

    def nearOrOnOurSide(self, position, boundary_line):
        if self.red:
            return position[0] <= boundary_line + 2
        return position[0] > boundary_line - 2

    def onOurSide(self, position, boundary_line):
        if self.red:
            return position[0] <= boundary_line
        return position[0] > boundary_line

    def onEnemySide(self, position, boundary_line):
        if self.red:
            return position[0] > boundary_line
        return position[0] <= boundary_line