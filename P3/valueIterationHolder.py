# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        # discount = self.discount
        # U is already given, which is self.values
        # U_prime = util.Counter()
        print(f"We are iterating {self.iterations} times \n")
        for i in range(self.iterations):
            U_prime = self.values.copy()
            # self.values = U_prime.copy()
            print(f"iteration {i}")
            print(f"U initially is {self.values}")
            print(f"U_prime initially is {U_prime}")
            for state in mdp.getStates():
                if mdp.isTerminal(state):
                    # print(f"state {state} is a terminal state")
                    continue
                actions = mdp.getPossibleActions(state)
                print(f"There are {len(actions)} possible actions for state {state}")

                """Note: A policy synthesized from values of depth k (which reflect the next k rewards) will actually 
                reflect the next k+1 rewards (i.e. you return πk+1πk+1). Similarly, the Q-values will also reflect 
                one more reward than the values (i.e. you return Qk+1). You should return the synthesized policy 
                πk+1πk+1. Therefore, instead of calculating R(s) + discount * ..., we calculate R(s, a, s') * P(s'|s,
                a) + discount * ... """
                action_utilities = util.Counter()
                for action in actions:
                    action_utilities[action] = self.computeQValueFromValues(state, action)
                    print(f"action {action} has utility {action_utilities[action]}")
                best_action = action_utilities.argMax()
                print(f"best action is {best_action}")
                best_utility = action_utilities[best_action]
                print(f"best utility is {best_utility}")
                # Update U'[s]
                U_prime[state] = best_utility
                print(f"U_prime is now {U_prime}")
                # print(
                #    f"making sure U and U_prime are not connected, U is now {U}")  # DA FUQ, U AND U_PRIME ARE LINKED
                # IF WE DON'T USE COPY()???
                # print(f"U is now {self.values}") # TERMINAL_STATE somehow got inside self.values
            self.values = U_prime.copy()
        print(f"After loop, U is {self.values} \n")
        return self.values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        discount = self.discount
        if mdp.isTerminal(state):
            return 0
        next_states_and_probs = mdp.getTransitionStatesAndProbs(state, action)
        running_sum = 0
        for next_state, prob in next_states_and_probs:
            running_sum += mdp.getReward(state, action, next_state) * prob + discount * self.getValue(next_state)
        # print(f"QValue of state {state} and action {action} is {running_sum}")
        return running_sum

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        mdp = self.mdp
        if mdp.isTerminal(state):
            return None
        actions = mdp.getPossibleActions(state)
        action_utilities = util.Counter()
        for action in actions:
            action_utilities[action] = self.computeQValueFromValues(state, action)
        best_action = action_utilities.argMax()
        # print(f"best_action is {best_action}")
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
