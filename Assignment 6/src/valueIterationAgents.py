# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates() <- a list of all states in mdp 
              mdp.getPossibleActions(state) <- all possible actions from s as list
              mdp.getTransitionStatesAndProbs(state, action) <- [s`, T(s, a, s`)] : a list of (s`, probability) 
              mdp.getReward(state, action, nextState) <- R(s, a ,s`)
              mdp.isTerminal(state) <- true if it is terminal
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        for i in range(iterations):
            newValues = self.values.copy() #don't edit in place (Batch version of value iteration)
            for state in mdp.getStates():
                if not self.mdp.isTerminal(state):
                    newValues[state] = max([self.computeQValueFromValues(state, action) for action in mdp.getPossibleActions(state)])   #V(s)(k+1) = max(Q(s,a)(k+1)) over all possible actions
            self.values = newValues #update values

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
        qValue = 0 #Q(s, a)(k+1) = SUM ( T(s, a, s`) * [ R(s, a, s`) + discount* V(s`)(k) ] : over all s` 
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            qValue += prob * ( self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState] )
            
        return qValue 
        
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        result = None #if there are no possible actions must return None, Terminal State
        
        actions = self.mdp.getPossibleActions(state)
        maxQValue = float('-inf') #Dynamic Programming
        for a in actions:
            qValue = self.computeQValueFromValues(state, a) #Represents Q(k+1) while self.values reflects the V(k) 
            if qValue > maxQValue:
                maxQValue = qValue
                result = a
        
        return result

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
