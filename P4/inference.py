# inference.py
# ------------
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


import itertools
import random
import busters
import game

from util import manhattanDistance, raiseNotDefined


class DiscreteDistribution(dict):
    """
    A DiscreteDistribution models belief distributions and weight distributions
    over a finite set of discrete keys.
    """

    def __getitem__(self, key):
        self.setdefault(key, 0)
        return dict.__getitem__(self, key)

    def copy(self):
        """
        Return a copy of the distribution.
        """
        return DiscreteDistribution(dict.copy(self))

    def argMax(self):
        """
        Return the key with the highest value.
        """
        if len(self.keys()) == 0:
            return None
        all = list(self.items())
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def total(self):
        """
        Return the sum of values for all keys.
        """
        return float(sum(self.values()))

    def normalize(self):
        """
        Normalize the distribution such that the total value of all keys sums
        to 1. The ratio of values for all keys will remain the same. In the case
        where the total value of the distribution is 0, do nothing.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> dist.normalize()
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0)]
        >>> dist['e'] = 4
        >>> list(sorted(dist.items()))
        [('a', 0.2), ('b', 0.4), ('c', 0.4), ('d', 0.0), ('e', 4)]
        >>> empty = DiscreteDistribution()
        >>> empty.normalize()
        >>> empty
        {}
        """
        "*** YOUR CODE HERE ***"
        sum_ = self.total()
        # For an empty distribution or a distribution where all of the values are zero, do nothing
        if sum_ == 0:
            return
        for key in self:  # Keys are discrete elements
            # Update values, which are weights
            self[key] = self[key] / sum_

    def sample(self):
        """
        Draw a random sample from the distribution and return the key, weighted
        by the values associated with each key.

        >>> dist = DiscreteDistribution()
        >>> dist['a'] = 1
        >>> dist['b'] = 2
        >>> dist['c'] = 2
        >>> dist['d'] = 0
        >>> N = 100000.0
        >>> samples = [dist.sample() for _ in range(int(N))]
        >>> round(samples.count('a') * 1.0/N, 1)  # proportion of 'a'
        0.2
        >>> round(samples.count('b') * 1.0/N, 1)
        0.4
        >>> round(samples.count('c') * 1.0/N, 1)
        0.4
        >>> round(samples.count('d') * 1.0/N, 1)
        0.0
        """
        "*** YOUR CODE HERE ***"
        elements = list(self.keys())
        weights = list(self.values())
        # random.random() is fine, but random.choices() is neater here since we have list of weights
        sample = random.choices(elements, weights=weights, k=1)[0]  # Need [0] or else it will return a list of size 1
        return sample


class InferenceModule:
    """
    An inference module tracks a belief distribution over a ghost's location.
    """

    ############################################
    # Useful methods for all inference modules #
    ############################################

    def __init__(self, ghostAgent):
        """
        Set the ghost agent for later access.
        """
        self.ghostAgent = ghostAgent
        self.index = ghostAgent.index
        self.obs = []  # most recent observation position

    def getJailPosition(self):
        return (2 * self.ghostAgent.index - 1, 1)

    def getPositionDistributionHelper(self, gameState, pos, index, agent):
        try:
            jail = self.getJailPosition()
            gameState = self.setGhostPosition(gameState, pos, index + 1)
        except TypeError:
            jail = self.getJailPosition(index)
            gameState = self.setGhostPositions(gameState, pos)
        pacmanPosition = gameState.getPacmanPosition()
        ghostPosition = gameState.getGhostPosition(index + 1)  # The position you set
        dist = DiscreteDistribution()
        if pacmanPosition == ghostPosition:  # The ghost has been caught!
            dist[jail] = 1.0
            return dist
        pacmanSuccessorStates = game.Actions.getLegalNeighbors(pacmanPosition, \
                                                               gameState.getWalls())  # Positions Pacman can move to
        if ghostPosition in pacmanSuccessorStates:  # Ghost could get caught
            mult = 1.0 / float(len(pacmanSuccessorStates))
            dist[jail] = mult
        else:
            mult = 0.0
        actionDist = agent.getDistribution(gameState)
        for action, prob in actionDist.items():
            successorPosition = game.Actions.getSuccessor(ghostPosition, action)
            if successorPosition in pacmanSuccessorStates:  # Ghost could get caught
                denom = float(len(actionDist))
                dist[jail] += prob * (1.0 / denom) * (1.0 - mult)
                dist[successorPosition] = prob * ((denom - 1.0) / denom) * (1.0 - mult)
            else:
                dist[successorPosition] = prob * (1.0 - mult)
        return dist

    def getPositionDistribution(self, gameState, pos, index=None, agent=None):
        """
        Return a distribution over successor positions of the ghost from the
        given gameState. You must first place the ghost in the gameState, using
        setGhostPosition below.
        """
        if index == None:
            index = self.index - 1
        if agent == None:
            agent = self.ghostAgent
        return self.getPositionDistributionHelper(gameState, pos, index, agent)

    def getObservationProb(self, noisyDistance, pacmanPosition, ghostPosition, jailPosition):
        """
        Return the probability P(noisyDistance | pacmanPosition, ghostPosition).
        """
        "*** YOUR CODE HERE ***"
        # Q: What is the probability here? Is it the probability that pacman captures the ghost?

        # Things that are noisy: noisyDistance
        # Things that are absolute: pacmanPosition, ghostPosition, jailPosition
        # Apply Bayes' rule with extra conditioning:
        # P(noisyDistance | pacmanPosition, ghostPosition) = P(noisyDistance | trueDistance) --> Is this a correct
        # assumption?

        # COMMENT: The description is extremely confusing!
        # Handling the edge case:
        # if the ghost’s position is the jail position, then the observation is None with probability 1,
        # and everything else with probability 0
        if ghostPosition == jailPosition:
            # After debugging, it is clear that even if the ghost is in jail, noisyDistance can be not None. This
            # contradicts what is written in Q1 description. Therefore, always returning 1 is incorrect
            # print("ghost is in jail because of coordinate check")
            # print(f"ghost position: {ghostPosition}")
            # print(f"jail position: {jailPosition}")
            # print(float(noisyDistance is None))
            return float(noisyDistance is None)
        # If the distance reading is None then the ghost is in jail with probability 1
        if noisyDistance is None:
            # After debugging, it is clear that even if the noisyDistance is None, the ghost can be out of jail. This
            # contradicts what is written in Q1 description. Therefore, always returning 1 is incorrect
            # print("noisy distance is None")
            # print(f"ghost position: {ghostPosition}")
            # print(f"jail position: {jailPosition}")
            # print(float(ghostPosition == jailPosition))
            return float(ghostPosition == jailPosition)
        trueDistance = manhattanDistance(pacmanPosition, ghostPosition)
        # print(busters.getObservationProbability(noisyDistance, trueDistance))
        return busters.getObservationProbability(noisyDistance, trueDistance)

    def setGhostPosition(self, gameState, ghostPosition, index):
        """
        Set the position of the ghost for this inference module to the specified
        position in the supplied gameState.

        Note that calling setGhostPosition does not change the position of the
        ghost in the GameState object used for tracking the true progression of
        the game.  The code in inference.py only ever receives a deep copy of
        the GameState object which is responsible for maintaining game state,
        not a reference to the original object.  Note also that the ghost
        distance observations are stored at the time the GameState object is
        created, so changing the position of the ghost will not affect the
        functioning of observe.
        """
        conf = game.Configuration(ghostPosition, game.Directions.STOP)
        gameState.data.agentStates[index] = game.AgentState(conf, False)
        return gameState

    def setGhostPositions(self, gameState, ghostPositions):
        """
        Sets the position of all ghosts to the values in ghostPositions.
        """
        for index, pos in enumerate(ghostPositions):
            conf = game.Configuration(pos, game.Directions.STOP)
            gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
        return gameState

    def observe(self, gameState):
        """
        Collect the relevant noisy distance observation and pass it along.
        """
        distances = gameState.getNoisyGhostDistances()
        if len(distances) >= self.index:  # Check for missing observations
            obs = distances[self.index - 1]
            self.obs = obs
            self.observeUpdate(obs, gameState)

    def initialize(self, gameState):
        """
        Initialize beliefs to a uniform distribution over all legal positions.
        """
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        self.allPositions = self.legalPositions + [self.getJailPosition()]
        self.initializeUniformly(gameState)

    ######################################
    # Methods that need to be overridden #
    ######################################

    def initializeUniformly(self, gameState):
        """
        Set the belief state to a uniform prior belief over all positions.
        """
        raise NotImplementedError

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the given distance observation and gameState.
        """
        raise NotImplementedError

    def elapseTime(self, gameState):
        """
        Predict beliefs for the next time step from a gameState.
        """
        raise NotImplementedError

    def getBeliefDistribution(self):
        """
        Return the agent's current belief state, a distribution over ghost
        locations conditioned on all evidence so far.
        """
        raise NotImplementedError


class ExactInference(InferenceModule):
    """
    The exact dynamic inference module should use forward algorithm updates to
    compute the exact belief function at each time step.
    """

    def initializeUniformly(self, gameState):
        """
        Begin with a uniform distribution over legal ghost positions (i.e., not
        including the jail position).
        """
        self.beliefs = DiscreteDistribution()
        for p in self.legalPositions:
            self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distance to the ghost you are
        tracking.

        self.allPositions is a list of the possible ghost positions, including
        the jail position. You should only consider positions that are in
        self.allPositions.

        The update model is not entirely stationary: it may depend on Pacman's
        current position. However, this is not a problem, as Pacman's current
        position is known.
        """
        "*** YOUR CODE HERE ***"
        pacman_position = gameState.getPacmanPosition()
        jail_position = self.getJailPosition()
        # Beliefs represent the probability that the ghost is at a particular location
        beliefs = self.beliefs
        # The ghost could be anywhere, so we loop through all positions
        all_positions = self.allPositions

        for position in all_positions:
            conditional_probability = self.getObservationProb(observation, pacman_position, position, jail_position)
            # Adjusting the weights of each position. We do this at each step so that we don't have to deal with a long
            # "given" query in the end (referring to slide 15 in lecture 12)
            beliefs[position] = beliefs[position] * conditional_probability

        self.beliefs.normalize()

    def elapseTime(self, gameState):
        """
        Predict beliefs in response to a time step passing from the current
        state.

        The transition model is not entirely stationary: it may depend on
        Pacman's current position. However, this is not a problem, as Pacman's
        current position is known.
        """
        "*** YOUR CODE HERE ***"
        # Current beliefs
        beliefs = self.beliefs
        # Get the new position distribution for every position
        conditional_probability = DiscreteDistribution()

        # After looping, this should give us a nested dictionary. It's the distribution probability of (1,1), (2,2), and
        # so on
        for position in self.allPositions:
            # This variable by itself is a dictionary, so we will get a nested dictionary in the end. Example of ONE
            # dictionary. Given that we start at (1, 1), there is 0 probability to move to (10,10) in the next step,
            # but there is 0.25 probability to move to (1,2), and we get a probability for each position on the board
            conditional_probability[position] = self.getPositionDistribution(gameState, position)

        # Update our beliefs
        new_beliefs = DiscreteDistribution()
        # For each position, update how likely it is for ghost to be there
        for next_position in self.allPositions:
            new_beliefs[next_position] = 0
            for previous_position in beliefs:
                # There any multiple ways to get to 1 position (from left, right, down, up). We simply add all those
                # probabilities together
                new_beliefs[next_position] += conditional_probability[previous_position][next_position] * beliefs[
                    previous_position]
                #                                    ^
                #                                    |
                #       Probability of being at {next_position} in t+1, given that we were at {previous_position} in t
        self.beliefs = new_beliefs

    def getBeliefDistribution(self):
        return self.beliefs


class ParticleFilter(InferenceModule):
    """
    A particle filter for approximately tracking a single ghost.
    """

    def __init__(self, ghostAgent, numParticles=300):
        InferenceModule.__init__(self, ghostAgent)
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def initializeUniformly(self, gameState):
        """
        Initialize a list of particles. Use self.numParticles for the number of
        particles. Use self.legalPositions for the legal board positions where
        a particle could be located. Particles should be evenly (not randomly)
        distributed across positions in order to ensure a uniform prior. Use
        self.particles for the list of particles.
        """
        self.particles = []
        "*** YOUR CODE HERE ***"
        num_particles = self.numParticles
        legal_positions = self.legalPositions
        # We want the prior to be uniform, so we put a fixed number of particles into each board position first
        fixed_particles = num_particles // len(legal_positions)
        # We will have some remaining particles, so we simple randomly put them into board positions
        remaining_particles = num_particles % len(legal_positions)

        # Adding the fixed particles
        self.particles = fixed_particles * legal_positions  # int * list gives us a list. We are rewriting
        # the legal_positions list fixed_particles times. This becomes a list that lets us know the position of each
        # particle

        # Adding the remaining particles
        self.particles += random.sample(legal_positions, remaining_particles)  # We want to put k particles into n
        # positions

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distance to the ghost you are
        tracking.

        There is one special case that a correct implementation must handle.
        When all particles receive zero weight, the list of particles should
        be reinitialized by calling initializeUniformly. The total method of
        the DiscreteDistribution may be useful.
        """
        "*** YOUR CODE HERE ***"
        # Things recommended by the project description
        pacman_position = gameState.getPacmanPosition()
        jail_position = self.getJailPosition()

        # Get the current belief distribution
        beliefs = self.getBeliefDistribution()

        # Update beliefs
        for location in beliefs:
            conditional_probability = self.getObservationProb(observation, pacman_position, location, jail_position)
            beliefs[location] = beliefs[location] * conditional_probability

        # Handling the edge case: When all particles receive zero weight, reinitialize uniformly
        if beliefs.total() == 0:
            self.initializeUniformly(gameState)
        else:
            # Else, resample using the new weights random.choices is extra neat here since we have the number of
            # samples (self.numParticles) and weights (beliefs.values()). Technically, beliefs is a
            # DiscreteDistribution object, which doesn't have a specified values() function. However,
            # DiscreteDistribution is a dict, so there is a values() function inherently
            self.particles = random.choices(list(beliefs), weights=list(beliefs.values()), k=self.numParticles)

    def elapseTime(self, gameState):
        """
        Sample each particle's next state based on its current state and the
        gameState.
        """
        "*** YOUR CODE HERE ***"
        new_particles = []
        for particle in self.particles:
            # Get the next position distribution of this particle. Recall that a particle is a location of a ghost
            next_position_distribution = self.getPositionDistribution(gameState, particle)
            # Sample this particle's next state using this new position distribution
            next_state = next_position_distribution.sample()  # next_pos_dist is a DiscreteDistribution object
            new_particles.append(next_state)

        self.particles = new_particles

    def getBeliefDistribution(self):
        """
        Return the agent's current belief state, a distribution over ghost
        locations conditioned on all evidence and time passage. This method
        essentially converts a list of particles into a belief distribution.
        
        This function should return a normalized distribution.
        """
        "*** YOUR CODE HERE ***"
        distribution = DiscreteDistribution()
        # A particle is 1 sample of a ghost location on the board
        for particle in self.particles:
            distribution[particle] += 1
        distribution.normalize()
        return distribution


class JointParticleFilter(ParticleFilter):
    """
    JointParticleFilter tracks a joint distribution over tuples of all ghost
    positions.
    """

    def __init__(self, numParticles=600):
        self.setNumParticles(numParticles)

    def initialize(self, gameState, legalPositions):
        """
        Store information about the game, then initialize particles.
        """
        self.numGhosts = gameState.getNumAgents() - 1
        self.ghostAgents = []
        self.legalPositions = legalPositions
        self.initializeUniformly(gameState)

    def initializeUniformly(self, gameState):
        """
        Initialize particles to be consistent with a uniform prior. Particles
        should be evenly distributed across positions in order to ensure a
        uniform prior.
        """
        self.particles = []
        "*** YOUR CODE HERE ***"
        # Each particle will represent a tuple of ghost positions that is a sample of where all the ghosts are at the
        # present time
        num_particles = self.numParticles
        num_ghosts = self.numGhosts
        legal_positions = self.legalPositions
        fixed_particles = num_particles // len(legal_positions)
        remaining_particles = num_particles % len(legal_positions)
        ghost_positions = []
        # Initialize position distribution for each ghost
        for ghost in range(num_ghosts):
            this_ghost_particles = []
            # Adding the fixed particles
            this_ghost_particles = fixed_particles * legal_positions
            # Adding the remaining particles
            this_ghost_particles += random.sample(legal_positions, remaining_particles)
            ghost_positions.append(this_ghost_particles)
        # Now, ghost_positions is a list of list, with each list being the position distribution of a ghost

        # Shuffle the position of each ghost, not the position of each ghost in the list
        for positions in ghost_positions:
            random.shuffle(positions)

        # Each particle is a tuple of ghost positions. Here we craft each particle at a time by indexing the correct
        # position for each ghost
        for position in range(len(ghost_positions[0])):
            particle = []
            for ghost in range(len(ghost_positions)):
                particle.append(ghost_positions[ghost][position])
            particle = tuple(particle)
            self.particles.append(particle)

        # Q: Why use itertools.product()?

    def addGhostAgent(self, agent):
        """
        Each ghost agent is registered separately and stored (in case they are
        different).
        """
        self.ghostAgents.append(agent)

    def getJailPosition(self, i):
        return (2 * i + 1, 1)

    def observe(self, gameState):
        """
        Resample the set of particles using the likelihood of the noisy
        observations.
        """
        observation = gameState.getNoisyGhostDistances()
        self.observeUpdate(observation, gameState)

    def observeUpdate(self, observation, gameState):
        """
        Update beliefs based on the distance observation and Pacman's position.

        The observation is the noisy Manhattan distances to all ghosts you
        are tracking.

        There is one special case that a correct implementation must handle.
        When all particles receive zero weight, the list of particles should
        be reinitialized by calling initializeUniformly. The total method of
        the DiscreteDistribution may be useful.
        """
        "*** YOUR CODE HERE ***"
        # Things that might be handy
        pacman_position = gameState.getPacmanPosition()
        beliefs = self.getBeliefDistribution()
        # print(beliefs)
        # Different from 1 ghost game:
        jail_positions = [self.getJailPosition(i) for i in range(self.numGhosts)]

        # Update beliefs - Copied straight from ParticleFilter, with appropriate modifications
        for location in beliefs:
            # Update for every ghost:
            for i in range(self.numGhosts):
                # Q: I don't quite understand this chunk. Why is beliefs[location] just a number while we have multiple
                # ghosts? If we update like this, what would this number tell us?
                conditional_probability = self.getObservationProb(observation[i],
                                                                  pacman_position,
                                                                  location[i],
                                                                  jail_positions[i])
                beliefs[location] = beliefs[location] * conditional_probability

        # Handling the edge case: When all particles receive zero weight, reinitialize uniformly
        if beliefs.total() == 0:
            self.initializeUniformly(gameState)
        else:
            # Else, resample using the new weights. random.choices is extra neat here since we have the number of
            # samples (self.numParticles) and weights (beliefs.values()). Technically, beliefs is a
            # DiscreteDistribution object, which doesn't have a specified values() function. However,
            # DiscreteDistribution is a dict, so there is a values() function inherently
            self.particles = random.choices(list(beliefs), weights=list(beliefs.values()), k=self.numParticles)

        # Q: The code is only failing 1 case. When I tweak the tolerance level I got max points. An idea I could try
        # is the fact that one ghost chooses to stay as far away from the other as possible.

    def elapseTime(self, gameState):
        """
        Sample each particle's next state based on its current state and the
        gameState.
        """
        newParticles = []
        ghosts = self.ghostAgents
        for oldParticle in self.particles:
            newParticle = list(oldParticle)  # A list of ghost positions

            # now loop through and update each entry in newParticle...
            "*** YOUR CODE HERE ***"
            # We have a list of ghost positions, so now loop through each ghost
            for i in range(self.numGhosts):
                next_position_distribution = self.getPositionDistribution(gameState, oldParticle, i, ghosts[i])
                newParticle[i] = next_position_distribution.sample()
            """*** END YOUR CODE HERE ***"""
            newParticles.append(tuple(newParticle))
        self.particles = newParticles


# One JointInference module is shared globally across instances of MarginalInference
jointInference = JointParticleFilter()


class MarginalInference(InferenceModule):
    """
    A wrapper around the JointInference module that returns marginal beliefs
    about ghosts.
    """

    def initializeUniformly(self, gameState):
        """
        Set the belief state to an initial, prior value.
        """
        if self.index == 1:
            jointInference.initialize(gameState, self.legalPositions)
        jointInference.addGhostAgent(self.ghostAgent)

    def observe(self, gameState):
        """
        Update beliefs based on the given distance observation and gameState.
        """
        if self.index == 1:
            jointInference.observe(gameState)

    def elapseTime(self, gameState):
        """
        Predict beliefs for a time step elapsing from a gameState.
        """
        if self.index == 1:
            jointInference.elapseTime(gameState)

    def getBeliefDistribution(self):
        """
        Return the marginal belief over a particular ghost by summing out the
        others.
        """
        jointDistribution = jointInference.getBeliefDistribution()
        dist = DiscreteDistribution()
        for t, prob in jointDistribution.items():
            dist[t[self.index - 1]] += prob
        return dist
