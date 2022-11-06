# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import gridworld

import random, util, math
import copy


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent
      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update
      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)
      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """

    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        # Q, a table of action values indexed by state and action, initially zero
        self.Q = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # If key state and key value not in Q, it will return 0 --> very handy!
        # If we have never seen a state Q[state] returns 0. Hence, cannot call 0[action] --> TypeError
        try:
            QValue = self.Q[state][action]
            # print(f"QValue is {QValue}")
            return QValue
        except TypeError:
            # print(f"QValue is 0")
            return 0

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # self.Q[state] is itself a dictionary (Q is a nested dictionary), so calling argMax should work here
        # Subtlety: Q will only store state/legal action pairs (because I will only add those in), so there's no need
        # to get legal actions and loop here. And if there are no legal actions, argMax() wil return None,
        # so I will catch this
        # argMax() will return a key, not the value

        # THIS DOESN'T WORK
        # Q:I Personally think the two are equivalent, but this doesn't work
        # print(f"Q[state] is {self.Q[state]}")
        # try:
        #     # Again, if Q[state] returns 0, it will give TypeError
        #     max_action = self.Q[state].argMax()
        #     if max_action is None:
        #         # print(f"no legal action, so value is 0")
        #         return 0
        #     else:
        #         value = self.Q[state][max_action]
        #         # print(f"max_action value is {value}")
        #         return value
        # except AttributeError:
        #     # print(f"state key not found, value is 0")
        #     return 0

        # ANOTHER VERSION
        legal_actions = self.getLegalActions(state)
        if not legal_actions:
            return 0.0
        return max(self.getQValue(state, action) for action in legal_actions)


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legal_actions = self.getLegalActions(state)
        # If there are no legal actions
        if not legal_actions:
            # print("no legal actions, return None")
            return None
        else:
            # max_action Q(state,action)
            value = self.computeValueFromQValues(state)
            # find all actions that have the same QValue as the highest Value
            actions = [action for action in legal_actions if self.getQValue(state, action) == value]
            random_action = random.choice(actions)
            # print(f"tie breaking, action is {random_action}")
            return random_action

        # Simpler code, but doesn't break ties randomly
        # max_action = self.Q[state].argMax()
        # return max_action

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.
          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legal_actions = self.getLegalActions(state)
        "*** YOUR CODE HERE ***"
        # We want to know this beforehand, so we can remove it from the list of exploration actions
        # Q: WHEN WE EXPLORE, DO WE STILL PUT THE BEST ACTION INTO CONSIDERATION?
        best_action = self.computeActionFromQValues(state)
        # if there are no legal actions, choose None as the action
        if not legal_actions:
            # print("no legal actions, return None")
            return None
            # r < epsilon, this returns true, meaning we should explore
        if util.flipCoin(self.epsilon):
            # print("exploring")
            # Remove best action from exploration options --> Not doing this for now
            # legalActions.remove(best_action)
            random_action = random.choice(legal_actions)
            # print(f"random action chosen is {random_action}")
            return random_action
        # else, choose best action
        else:
            # print(f"following policy, best action is {best_action}")
            return best_action

    def update(self, state, action, nextState, reward: float):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here
          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # If state key is not in Q, initialize it
        if self.Q[state] == 0:
            # print("First time seeing this state, initializing")
            self.Q[state] = util.Counter()
        # If state key is already in Q, either initialize action or update it
        # print(f"old Q[s][a] is {self.Q[state][action]}")
        self.Q[state][action] = self.Q[state][action] + self.alpha * (
                    reward + self.discount * self.computeValueFromQValues(nextState) - self.Q[state][action])
        # print(f"updated Q[s][a] is {self.Q[state][action]}")

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1
        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent
       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """

    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        weights = self.weights
        features = self.featExtractor.getFeatures(state, action)
        return weights * features

    def update(self, state, action, nextState, reward: float):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        difference = reward + self.discount * self.computeValueFromQValues(nextState) - self.getQValue(state, action)
        weights = self.weights
        features = self.featExtractor.getFeatures(state, action)
        for i in features:
            weights[i] = weights[i] + self.alpha * difference * features[i]



    def final(self, state):
        """Called at the end of each game."""
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
