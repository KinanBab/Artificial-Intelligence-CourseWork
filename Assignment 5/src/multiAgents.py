# multiAgents.py
# --------------

from util import manhattanDistance
from game import Directions
from game import Agent
import random, util

class ReflexAgent(Agent):
	"""
	  A reflex agent chooses an action at each choice point by examining
	  its alternatives via a state evaluation function.

	  The code below is provided as a guide.  You are welcome to change
	  it in any way you see fit, so long as you don't touch our method
	  headers.
	"""

	def getAction(self, gameState):
		"""
		You do not need to change this method, but you're welcome to.

		getAction chooses among the best options according to the evaluation function.

		Just like in the previous project, getAction takes a GameState and returns
		some Directions.X for some X in the set {North, South, West, East, Stop}
		"""
		
		#counts the number of moves
		if hasattr(self, 'moveCount'):
			self.moveCount += 1
		else:
			self.moveCount = 0

		
		# Collect legal moves and successor states
		legalMoves = gameState.getLegalActions()
		
		# Choose one of the best actions
		scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
		bestScore = max(scores)
		bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
		chosenIndex = random.choice(bestIndices) # Pick randomly among the best

		"Add more of your code here if you want to"
		
		return legalMoves[chosenIndex]

	def evaluationFunction(self, currentGameState, action):
		"""
		Design a better evaluation function here.

		The evaluation function takes in the current and proposed successor
		GameStates (pacman.py) and returns a number, where higher numbers are better.

		The code below extracts some useful information from the state, like the
		remaining food (newFood) and Pacman position after moving (newPos).
		newScaredTimes holds the number of moves that each ghost will remain
		scared because of Pacman having eaten a power pellet.

		Print out these variables to see what you're getting, then combine them
		to create a masterful evaluation function.
		"""
		
		"""
			average score is usually around 1200
			10/10 winning ratio 
		"""
		if action == 'Stop': #Never Stop
			return -10000000
		
		# Useful information you can extract from a GameState (pacman.py)
		successorGameState = currentGameState.generatePacmanSuccessor(action) #Get the new state parameters after this action
		newX, newY = successorGameState.getPacmanPosition()
		newFood = successorGameState.getFood()
		newGhostStates = successorGameState.getGhostStates()

		foodEval = 5000*(96 - newFood.count(True) - self.moveCount/10) #food evaluation, based on the number of remaining food dots
		
		foods = newFood.asList(True) #totalDist (total distance to all dots), minDist(distance to the closest food dot)
		totalDist = 0
		minDist = 1000
		foodCount  = 0
		for food in foods:
			foodCount += 1
			dist = manhattanDistance((newX, newY), food)
			totalDist += dist
			if dist < minDist:
				minDist =  dist
		
		ghostEval = 0 #the ghost aspect in evaluating
		for ghostState in newGhostStates:			
			ghostX, ghostY = ghostState.getPosition()
			oldManhattan = manhattanDistance((newX, newY), (ghostX, ghostY))
			
			ghostDir = ghostState.getDirection()
			if ghostDir == 'North':
				ghostY += 1
			elif ghostDir == 'South':
				ghostY -= 1
			elif ghostDir == 'East':
				ghostX += 1
			elif ghostDir == 'West':
				ghostX -= 1
			
			randomAdd = 0
			newManhattan = manhattanDistance((newX, newY), (ghostX, ghostY))
			if oldManhattan < 2: #if action results in having a ghost away by one square, dont take action
				return -1000000
			if newManhattan < oldManhattan: #otherwise, if the ghost is getting closer to the agent include the position of the ghost in the eval
				if oldManhattan < 5: #if ghost was 4 or less square away give greater weight to it then if it was further away
					ghostEval += 500/oldManhattan
				else:
					ghostEval += 3.14/oldManhattan
		return foodEval - totalDist - (foodCount/3.14)*minDist - (2.1725468)*minDist - ghostEval + randomAdd #the total evaluation that contains all previous components, minDist was used more than once with different weights to try and eliminate pacman being stuck in the middle between two groups of dots

def scoreEvaluationFunction(currentGameState):
	"""
	  This default evaluation function just returns the score of the state.
	  The score is the same one displayed in the Pacman GUI.

	  This evaluation function is meant for use with adversarial search agents
	  (not reflex agents).
	"""
	return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
	"""
	  This class provides some common elements to all of your
	  multi-agent searchers.  Any methods defined here will be available
	  to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

	  You *do not* need to make any changes here, but you can if you want to
	  add functionality to all your adversarial search agents.  Please do not
	  remove anything, however.

	  Note: this is an abstract class: one that should not be instantiated.  It's
	  only partially specified, and designed to be extended.  Agent (game.py)
	  is another abstract class.
	"""

	def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
		self.index = 0 # Pacman is always agent index 0
		self.evaluationFunction = util.lookup(evalFn, globals())
		self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent (question 2)
	"""

	def getAction(self, gameState):
		"""
		  Returns the minimax action from the current gameState using self.depth
		  and self.evaluationFunction.

		  Here are some method calls that might be useful when implementing minimax.

		  gameState.getLegalActions(agentIndex):
			Returns a list of legal actions for an agent
			agentIndex=0 means Pacman, ghosts are >= 1

		  gameState.generateSuccessor(agentIndex, action):
			Returns the successor game state after an agent takes an action

		  gameState.getNumAgents():
			Returns the total number of agents in the game
		"""
		return self.maxValue(0, gameState)[1]  #[0] value of the root node, [1] action that max its value

	def maxValue(self, iteration, state):
		"""
			REMARK: Winning ratio for this agent differs between 5/10 to 8/10, 
			but when running for 100 times it is becomes stable around 60%. depth 4
			
			it loses 100% of the times in trappedClassic layout with constant score of -501. depth 3
		"""
		if state.isLose() or state.isWin(): #if this state is an end game state return its evaluation (it doesnt have any successors)
			return self.evaluationFunction(state)
		
		legalActions = state.getLegalActions(0) #0 => pacman
		if Directions.STOP in legalActions: #don't make stop a valid option
			legalActions.remove(Directions.STOP)
		
		successors = [state.generateSuccessor(0, action) for action in legalActions] #generate all possible successors
		values = [self.minValue(iteration, 1, successor) for successor in successors] #get the min values of all possible successors
		v = max(values)
		
		if iteration == 0: #the final return statment must contain the action to take
			return (v, legalActions[values.index(v)])
		else:
			return v

	def minValue(self, iteration, index, state):
		if state.isLose() or state.isWin(): #if this state is an end game state return its evaluation (it doesnt have any successors)
			return self.evaluationFunction(state)
		
		count = state.getNumAgents() #number of agents
		legalActions = state.getLegalActions(index) #index > 1 => ghost
		if Directions.STOP in legalActions: #don't make stop a valid option
			legalActions.remove(Directions.STOP)
		
		successors = [state.generateSuccessor(index, action) for action in legalActions] #generate all possible successors
		if index+1 == count: #if finished one search ply
			if iteration+1 == self.depth: #if depth reached, calculate the values using eval function
				values = [self.evaluationFunction(successor) for successor in successors]
			else: #switch to max
				values = [self.maxValue(iteration+1, successor) for successor in successors] 
		else: #next ghost
			values = [self.minValue(iteration, index+1, successor) for successor in successors]
			
		v = min(values)
		return v

class AlphaBetaAgent(MultiAgentSearchAgent):
	"""
	  Your minimax agent with alpha-beta pruning (question 3)
	"""
	
	def getAction(self, gameState):
		"""
		  Returns the minimax action using self.depth and self.evaluationFunction
		"""
		return self.maxValue(0, gameState, -1000000, +1000000)[1]  #[0] value of the root node, [1] action that max its value

	def maxValue(self, iteration, state, alpha, beta):
		"""
			Behavior is similar to minimax and has the same average score and wining ratios
			also values of the nodes were identical and equal to the description.
		"""
		if state.isLose() or state.isWin(): #if this state is an end game state return its evaluation (it doesnt have any successors)
			return self.evaluationFunction(state)
		
		legalActions = state.getLegalActions(0) #0 => pacman
		if Directions.STOP in legalActions: #don't make stop a valid option
			legalActions.remove(Directions.STOP)
		
		v = -100000000
		actionIndex = -1
		successors = [state.generateSuccessor(0, action) for action in legalActions] #generate all possible successors
		for i in range(len(successors)): #loop over all successors
			tmp = self.minValue(iteration, 1, successors[i], alpha, beta) #use min agent
			if v < tmp: #if v 
				v = tmp
				actionIndex = i
			
			if v > beta: #Beta pruning
				break
			alpha = max(alpha, v)
			
		if iteration == 0:
			return (v, legalActions[actionIndex])
		else:
			return v

	def minValue(self, iteration, index, state, alpha, beta):
		if state.isLose() or state.isWin(): #if this state is an end game state return its evaluation (it doesnt have any successors)
			return self.evaluationFunction(state)
		
		count = state.getNumAgents() #number of agents
		legalActions = state.getLegalActions(index) #index > 1 => ghost
		if Directions.STOP in legalActions: #don't make stop a valid option
			legalActions.remove(Directions.STOP)
		
		v = +100000
		successors = [state.generateSuccessor(index, action) for action in legalActions] #generate all possible successors
		if index+1 == count: #finished one search ply
			if iteration+1 == self.depth: #depth reached, calculate the values using eval function
				for successor in successors: 
					v = min(v, self.evaluationFunction(successor))
					if v < alpha:
						return v
					
					beta = min(beta, v)
				return v
			else: #switch to max
				for successor in successors:
					v = min(v, self.maxValue(iteration+1, successor, alpha, beta))
					if v < alpha:
						return v
					
					beta = min(beta, v)
				return v 
		else: #next ghost
			for successor in successors:
				v = min(v, self.minValue(iteration, index+1, successor, alpha, beta))
				if v < alpha:
					return v
					
				beta = min(beta, v)
			return v

class ExpectimaxAgent(MultiAgentSearchAgent):
	"""
	  Your expectimax agent (question 4)
	"""

	def getAction(self, gameState):
		"""
		  Returns the expectimax action using self.depth and self.evaluationFunction

		  All ghosts should be modeled as choosing uniformly at random from their
		  legal moves.
		"""
		return self.maxValue(0, gameState)[1] #[0] value of the root node, [1] action that max its value
	
	def maxValue(self, iteration, state):
		"""
		For minimaxClassic layout wining percentage is about 80% : depth 4
		for trappedClassic layout wining percentage is about 50% : depth 3
		
		"""
		if state.isLose() or state.isWin(): #if this state is an end game state return its evaluation (it doesnt have any successors)
			return self.evaluationFunction(state)
		
		legalActions = state.getLegalActions(0) #0 => pacman
		if Directions.STOP in legalActions: #don't make stop a valid option
			legalActions.remove(Directions.STOP)
		
		successors = [state.generateSuccessor(0, action) for action in legalActions] #generate all possible successors
		values = [self.ExpectiValue(iteration, 1, successor) for successor in successors] #get the expected values of all possible successors
		v = max(values)
		
		if iteration == 0: #the final return statment must contain the action to take
			return (v, legalActions[values.index(v)])
		else:
			return v

	def ExpectiValue(self, iteration, index, state):
		if state.isLose() or state.isWin(): #if this state is an end game state return its evaluation (it doesnt have any successors)
			return self.evaluationFunction(state)
		
		count = state.getNumAgents() #number of agents
		legalActions = state.getLegalActions(index) #(index >= 1) => ghost
		if Directions.STOP in legalActions: #don't make stop a valid option
			legalActions.remove(Directions.STOP)
		
		successors = [state.generateSuccessor(index, action) for action in legalActions] #generate all possible successors
		if index+1 == count: #finished one search ply
			if iteration+1 == self.depth: #depth reached, calculate the values using eval function
				values = [self.evaluationFunction(successor) for successor in successors]
			else: #switch to max
				values = [self.maxValue(iteration+1, successor) for successor in successors] 
		else: #next ghost
			values = [self.ExpectiValue(iteration, index+1, successor) for successor in successors]
			
		v = sum(values)/(len(values)*1.0) #getting the average (assume that the ghost moves at random so all weights are equal between the actions)
		return v

def betterEvaluationFunction(currentGameState):
	"""
	  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
	  evaluation function (question 5).

	  DESCRIPTION:
	  	- The Factors considered:
	  		* number of food dots left, has a very high weight, pacman must try to decrease them
	  		
	  		* the distance to the closest food dot, has a good weight, pacman must try to get closer to it
	  		
	  		* the distance to the closest 3, 5 ,7 food dots. (3 then 5 then 7, no overlap). has a low weight that keeps getting lower as n grows (3, 5, 7)
	  		
	  		* the score, has a high weight, pacman must always try to increase the score.
	  		
	  		* distance from active ghosts. if the active ghosts are really close, pacman must only consider escaping / eating a mega dot. otherwise it must have a considerable weight. 
	  						must have minimal effect if pacman was very far or moving away.
	  						
	  		* distance from scared ghosts. if the scared ghosts were within reached before the scared effect times out, pacman must go after them. very high weight propotional to the distance.
	  						eating a ghost give a great bonus to the score.
	  						
	  		* distance from the super (mega) food dot. if pacman was relatively close to it and a ghost was within pacman's reach, pacman must go after the mega food and then after the ghost.
	  						Notice that if pacman was away of the super dot or the ghosts were really far this must not have an effect on the value of the state.
	  						
	  		* random tie break component: some times pacman has two states that are nearly equal in value (for example a state where dots on the right equal the dots on the left in distance and number)
	  						in such cases pacman would keep on spinning left and right without making up his mind. this gives a small random extra value to the state (negative or positive). 
	  						the random extra is small, so it will not make the value of a very bad state become better than that of a considerably better state.
	  						
		- I have tried different linear combination of these factors (different weights). evantually I chose these weights
			because I was satisfied with their results.
			
		RESULTS:
			with depth 3 expectimax using this eval function the following results were achieved:
				- out of 10 games, usually 9 games are won.
				- average score is around 1200
	"""
	if currentGameState.isLose(): #lost state is very bad
		return -100000000
	if currentGameState.isWin(): #win state is very good
		return 100000000 + currentGameState.getScore()
	
	X, Y = currentGameState.getPacmanPosition() #Pacman position
	Food = currentGameState.getFood().asList(True) #food distribution as a list
	GhostStates = currentGameState.getGhostStates() #ghosts
	Score = currentGameState.getScore() #current Score
	
	foodCountComponent = -currentGameState.getNumFood() #must reduce the number of food dots on the map
	closestFoodComponent = 0 #distance to the closest food dot
	closest3FoodsComponent = 0 #distance to the other closest 3 dots 
	closest5FoodsComponent = 0 #distance to the other closest 5 dots
	closest7FoodsComponent = 0 #distance to the other closest 7 dots
	scaredGhostComponent = 0 #if the ghost is scared or not, will be explained later
	ghostComponent = 0 #distance from active ghost (i.e. not scared ghosts)
	scoreComponent = Score #score
	distanceFromSuperDotComponent = 0 #super dots that make ghosts scared
	randomTieBreakComponent = random.randint(-1, 1) # a random tie breaker for making pacman attempt random moves to avoid getting stuck on walls or between two adjacent food dots
	
	closestCapsuleDistance = min([manhattanDistance((X, Y), capsulses) for capsulses in (currentGameState.getCapsules()+[(1000, 1000)])]) #the manhattan distance to the closest mega dot or manhattan distance to 1000,1000 in case no mega dot existed
	
	dotsQueue = util.PriorityQueue() #priority queue to store food dots in ordered by their manhattan distance from pacman
	for dot in Food:
		d = manhattanDistance((X,Y), dot)
		dotsQueue.push((-d, dot), -d) #negative priority, because the queue is based on min heap not max heap
		
	for i in range(0, 16): #calculating the distance to the specified (n) food dots
		if dotsQueue.isEmpty():
			break
		d = dotsQueue.pop()[0]
		if i == 0:
			closestFoodComponent = d
		elif i < 4:
			closest3FoodsComponent += d
		elif i < 6:
			closest5FoodsComponent += d
		elif i < 8:
			closest7FoodsComponent += d

	for ghostState in GhostStates: #for each ghost
			ghostX, ghostY = ghostState.getPosition() #get the ghost position
			oldManhattan = manhattanDistance((X, Y), (ghostX, ghostY)) #get the manhattan distance
			ghostDir = ghostState.getDirection() #get the ghosts direction
			if ghostDir == 'North': #get the ghosts new distance after moving in its direction
				ghostY += 1
			elif ghostDir == 'South':
				ghostY -= 1
			elif ghostDir == 'East':
				ghostX += 1
			elif ghostDir == 'West':
				ghostX -= 1
			
			newManhattan = manhattanDistance((X, Y), (ghostX, ghostY))			
			if ghostState.scaredTimer > newManhattan + 3: #if the ghost is scared and pacman has enough time to get him increase the scared ghost component
				scaredGhostComponent += -newManhattan
			else: #otherwise
				if closestCapsuleDistance < 5 and newManhattan < 8: #if the ghost is relatively close and the mega dot is close go eat the mega dot
					distanceFromSuperDotComponent += - (3/ (newManhattan+0.1)) * 350 * closestCapsuleDistance
					
				if oldManhattan < 3: #if the ghost was closer than 3 tiles away, get away from the ghost and don't take random tie breaks
					ghostComponent += oldManhattan*4
					randomTieBreakComponent = 0
				else:
					if oldManhattan < 6: #if the ghost is relatively  close put a regular weight on escaping 
						ghostComponent += newManhattan
					elif newManhattan < oldManhattan: #if the ghost is moving away from give very little weight for escaping
						ghostComponent += newManhattan*0.05
					
	return 100*foodCountComponent + 20*scoreComponent + 0.7 * ghostComponent + 5*closestFoodComponent + 0.3*closest3FoodsComponent + 0.1*closest5FoodsComponent + 0.12*closest7FoodsComponent + randomTieBreakComponent + 25*scaredGhostComponent + distanceFromSuperDotComponent #linear combination of components

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
	"""
	  Your agent for the mini-contest
	"""

	def getAction(self, gameState):
		"""
		  Returns an action.  You can use any method you want and search to any depth you want.
		  Just remember that the mini-contest is timed, so you have to trade off speed and computation.

		  Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
		  just make a beeline straight towards Pacman (or away from him if they're scared!)
		"""
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()

