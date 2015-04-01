# searchAgents.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
This file contains all of the agents that can be selected to
control Pacman.  To select an agent, use the '-p' option
when running pacman.py.  Arguments can be passed to your agent
using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the
project description.

Please only change the parts of the file you are asked to.
Look for the lines that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the
project description for details.

Good luck and happy searching!
"""
from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search algorithm for a
    supplied search problem, then returns actions to follow that path.

    As a default, this agent runs DFS on a PositionSearchProblem to find location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError, fn + ' is not a search function in search.py.'
        func = getattr(search, fn)
        if 'heuristic' not in func.func_code.co_varnames:
            print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError, heuristic + ' is not a function in searchAgents.py or search.py.'
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError, prob + ' is not a search problem type in SearchAgents.py.'
        self.searchType = globals()[prob]
        print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game board. Here, we
        choose a path to the goal.  In this phase, the agent should compute the path to the
        goal and store it in a local variable.  All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception, "No search function provided for SearchAgent"
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in registerInitialState).  Return
        Directions.STOP if there is no further action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test,
    successor function and cost function.  This search problem can be
    used to find paths to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print 'Warning: this does not look like a regular search maze'

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5


#####################################################
# This portion has been completed for Assignment 1  #
#####################################################

class CornersProblem(search.SearchProblem):
    """
    OVERVIEW:    this class represents the CornersProblem
                 it implements all the method in search.SearchProblem class.
                 it uses the class CornersProblem.MyState to represent the states.
                 this state class contains only relevant information(pacman's position and corners statuses) and not all the information about pacman.
    """
    class MyState:
        """ 
        OVERVIEW:     a class that represents a state
                      contains only relevant information:
                      the position of the pacman, a flag for each corner to determine whether it was reached or not
        """
        
        def __init__(self, position, corners):
            """ Constructor """
            """
            REQUIRES:    position is a pair(x,y)
                         corners is a list of length 4, contains 0 and 1 where 0 represents a corner not reached and 1 represents a corner reached
            EFFECTS:     creates a state that encapsulates position and corners information
            """
            self.position = position
            self.corners = corners
            
        def isGoalState(self):
            """
            EFFECTS: return True if self is a goal state(all the corners where reached), False otherwise.
            """
            return self.corners[0]+self.corners[1]+self.corners[2]+self.corners[3] == 4
        
        def __eq__(self, other):
            """
            EQUALS OPERATION FOR MyState
            EFFECTS:    returns True if other and self were MyState instances and they contained the same position and corners information
            """
            if isinstance(other, self.__class__):
                return (self.position == other.position) and (self.corners == other.corners)
            else:
                return False
        
    def __init__(self, startingGameState):
        """ Constructor """
        """
        REQUIRES:    startingGameState is a pair(x,y) that represents the orignial position of the pacman in the maze.
        EFFECTS:     creates a new instance of CornersProblem.
                     this instance stores the walls layout, the pacman's starting position, and the positions of corners as a list.
                     also it stores the startState as an instance of MyState containg the pacman's starting position, and a list [0,0,0,0] that represents that no corner was reached.
        """
        self.walls = startingGameState.getWalls()   #storing walls layout
        self.startingPosition = startingGameState.getPacmanPosition()   #storing the starting position
        
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = [(1,1), (1,top), (right, 1), (right, top)]   #storing the corners position in a list
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print 'Warning: no food in corner ' + str(corner)
                
        self._expanded = 0 #Initializing the numbers of nodes expanded to 0
        
        crns = [0, 0, 0, 0]
        if self.startingPosition in self.corners:
            i = self.corners.index(self.startingPosition)
            crns[i] = 1
        self.startState = CornersProblem.MyState(self.startingPosition, crns)   #saving the start state as an instance of MyState

    def getStartState(self):
        """
        EFFECTS: returns the starting state as an instance of MyState.
        """
        return self.startState

    def isGoalState(self, state):
        """
        EFFECTS: returns True if state was a goal state, False otherwise.
        """
        return state.isGoalState()

    def getSuccessors(self, state):
        """
        REQUIRES:    state is not null, state represents a legal state.
        EFFECTS:     returns a list containing all the successor states of state, i.e. states that results from one legal move of pacman
                     starting from the previous state
        
        """

        """
        IMPLEMENTATION SKETCH:
            FOR EACH direction (north, south, east, west)
                calculate the new pacman position.
                IF the new position is valid(not a wall) THEN
                    IF the new position is a corner THEN
                        mark the corner as reached.
                    
                    add the tuple (new state[new pacman position, new corners information], action required to get to the new state, cost of 1) to the result.
            RETURN result.
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]: #loop over all directions
            # Add a successor state to the successor list if the action is legal
            x,y = state.position    #get the original position
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy) #calculate the new position
            if not self.walls[nextx][nexty]:    #check if the new position is not a wall
                cornerValues = state.corners[:]    #get the original corner information (copy list by value not refrence)
                if (nextx, nexty) in self.corners:  #if the new position is a corner mark it as reached
                    index = self.corners.index((nextx,nexty))
                    cornerValues[index] = 1
                    
                newState = CornersProblem.MyState((nextx,nexty), cornerValues)
                successors.append((newState,action,1))  #add the new state to the successors list
                
        self._expanded += 1 #increasing the number of expanded nodes by one
        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)

def cornersHeuristic(state, problem):
    """
    REQUIRES:    state is not null and is an instance of CornersProblem.MyState.
                 problem is not null and is an instance of CornersProblem.
                 
    EFFECTS:     Should Return a number that represent the Heuristic of the state, This Heuristic must be
                 admissible and consistent, i.e. the Heuristic must never overestimates the cost and taking an
                 action with cost c can only cause the Heuristic to drop at most c.
    """
    """
    IMPLEMENTATION IDEA:
                 - The Heuristic Must take into consideration only the corners not reached.
                 - The Heuristic should encourage the paceman to go for the closet corner (in number of moves not direct distance), then
                   the next corner, then the next, etc..
                 - The manhattan distance was a good Heuristic for one dot of food.
                 - Let the Heuristic be the sum of the manhattan distances between:
                         - the current position and the closest not reached corner c1 [in manhattan distance not euclidean distance].
                         - c1 and the next closest not reached corner c2
                         - c2 and the next not reached corner c3 ... etc ...
                         
                 The described manhattan distance is consistent, the cost of one movement is one. and after any move the distance to 
                 the corners that were not reached is reduced either by one, or is increased by one. 
                 
                 also the described manhattan distance is admissible, the shortest possible way(if there was no walls) for the pacman to 
                 reach a corner cost the same number of moves as the manhattan distance between it and that corner. and the pacman needs
                 to go to all the corners. so at any state, the Heuristic is less than the actual cost (or equal to it if there is no walls).

    IMPLEMENTATION SKETCH:
        store the position of each corner that was not reached.
        pos <- current pacman position.
        WHILE there is more corners to check DO
            get the closest corner to pos.
            add the manhattan distance between the corner and pos to the Heuristic.
            pos <- corner.
            remove the corner from the list of corners to be checked.
            
        RETURN the Heuristic.
    """
    
    corners = problem.corners # These are the corner coordinates

    Heuristic = 0   #declare Heuristic
    
    cornersReachedPosition = []
    for i in range(4):  #loop over all corners
        if state.corners[i] == 0:   #if corner is not reached add it to the list
            cornersReachedPosition.append(corners[i])
    
    pos = state.position    #set the pos to the pacman position
    while len(cornersReachedPosition) > 0:
        crn = getClosestManhatanCorner(pos, cornersReachedPosition) #get the closest corner to pos
        Heuristic += abs(pos[0] - crn[0]) + abs(pos[1] - crn[1])    #add the manhattan distance to the Heuristic
        
        cornersReachedPosition.remove(crn)
        pos = crn   
            
    return Heuristic # Default to trivial solution

def getClosestManhatanCorner(position, corners):
    """
    REQUIRES:    position is a pair(x,y) of numbers.
                 corners is a list of pairs containing at least one element.
    RETURNS:     returns the pair(x,y) in corners that has the least manhattan distance to position.
    """
    mindst = -1
    pos = (0,0)
    for i in corners:
        dist = abs(position[0] - i[0]) + abs(position[1] - i[1])
        if(mindst == -1 or dist < mindst):
            mindst = dist
            pos = i
    
    return pos 

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a
    Grid (see game.py) of either True or False. You can call foodGrid.asList()
    to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, problem.walls gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use. For example,
    if you only want to count the walls once and store that value, try:
      problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount']
    """
    position, foodGrid = state
    "*** YOUR CODE HERE ***"
    return 0

class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception, 'findPathToClosestDot returned an illegal move: %s!\n%s' % t
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print 'Path found with cost %d.' % len(self.actions)

    def findPathToClosestDot(self, gameState):
        "Returns a path (a list of actions) to the closest dot, starting from gameState"
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AnyFoodSearchProblem(PositionSearchProblem):
    """
      A search problem for finding a path to any food.

      This search problem is just like the PositionSearchProblem, but
      has a different goal test, which you need to fill in below.  The
      state space and successor function do not need to be changed.

      The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
      inherits the methods of the PositionSearchProblem.

      You can use this search problem to help you fill in
      the findPathToClosestDot method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test
        that will complete the problem definition.
        """
        x,y = state

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

##################
# Mini-contest 1 #
##################

class ApproximateSearchAgent(Agent):
    "Implement your contest entry here.  Change anything but the class name."

    def registerInitialState(self, state):
        "This method is called before any moves are made."
        "*** YOUR CODE HERE ***"

    def getAction(self, state):
        """
        From game.py:
        The Agent will receive a GameState and must return an action from
        Directions.{North, South, East, West, Stop}
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def mazeDistance(point1, point2, gameState):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built.  The gameState can be any game state -- Pacman's position
    in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = gameState.getWalls()
    assert not walls[x1][y1], 'point1 is a wall: ' + point1
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = PositionSearchProblem(gameState, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))
