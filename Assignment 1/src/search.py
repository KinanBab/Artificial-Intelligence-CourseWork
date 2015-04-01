# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

""" end of SearchProblem class """

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    REQUIRES:    problem is not null, problem is well defined (getStartState(), isGoalState(), getSuccessors() yield good results).
    EFFECTS:     returns a list that contains the direction to reach the goal state from the start state, uses depth first search 
                 algorithm to search for the goal node (and find the path).
    CLAUSES:     for the medium Maze, The maximum number of explored nodes is 146, result path should have a length of 130.                
    DESCRIPTION: Search the deepest nodes in the search tree first 
    
	"""
    
    """
    IMPLEMENTATION IDEA:
        the result path is a list of length 130 , the elements of the list represents the direction to move from one state to the other,
        in other words, each element represents an edge of the path from the root to the goal node in the search tree. thus, only one 
        direction per level of tree is included in the path. 
        
            path[i-1] = directionTo(nodeAtLevel(i)) : 
                    0 < i < 130
                    direction To represents the required direction to reach the node from its parent (obtained from the successor list)
    
    IMPLEMENTATION SKETCH:  
        current <- start state with level 0.
        WHILE current is not the goal state DO
            mark current as explored.
            
            get successors of current.
            FOR each successor of current
                IF the successor was not explored THEN
                    add successor to frontier (stack) with level (current level + 1) .
            
            current <- next element in frontier.
            
            IF path contains a direction for a node with the same level as current THEN 
                replace direction at this level with the direction to current.
            ELSE
                append direction to current to the path.
                
        RETURN path.
    """
    
    frontier = util.Stack() #LIFO Stack to store nodes to be explored
    explored = []   #List that stores the already explored nodes (To avoid Exploring already explored nodes)
    path = ['Stop'] #List that contains the moves to the goal, initially set to Stop
     
    current = (problem.getStartState(), 0, 'Stop')    #set the current state to (Start state position, level=0, direction to get to this state='Stop')
    while not problem.isGoalState(current[0]): #loop as long as we didn't reach the goal
        explored.append(current[0]) #mark current as explored
                
        sucs = problem.getSuccessors(current[0]) #get the successors of the current state
        for f in sucs:  
            if not (f[0] in explored):  #if the node was not explored add it to the frontier as the tuple (position[x,y], level = parent node level + 1, direction to get to this node)
                frontier.push((f[0], (current[1] + 1) , f[1]))
                
        current = frontier.pop()  #set the next state to the next state (last added state to the stack)
        
        if(len(path) <= current[1]-1):  #putting the direction for this node in it is right place in direction list (level-1)
            path.append(current[2])
        else:
            path[current[1]-1] = current[2]
        
    return path

def breadthFirstSearch(problem):
    """
    REQUIRES:    problem is not null, problem is well defined (getStartState(), isGoalState(), getSuccessors() yield good results).
    EFFECTS:     returns a list that contains the direction to reach the goal state from the start state, uses breadth first search
                 algorithm.
    CLAUSES:     for the medium Maze, The maximum number of explored nodes is 269, result path should have a length of 68.  
    DESCRIPTION: Search the most shallow nodes in the search tree first. 
    
    """
    
    """
    IMPLEMENTATION IDEA:
        the path to reach Node (n) is kept with n in the frontier, when n is explored that path is passed by to its children
        node with one extra direction (from n to each child). once the algorithm reaches the goal, it will have the direction associated
        with it in the frontier. all there is to do is to return it.

    IMPLEMENTATION SKETCH:  
        current <- start state with an empty list as the path to reach it.
        WHILE current is not the goal state DO
            mark current as explored.
            
            get successors of current.
            FOR each successor of current
                add successor to frontier (queue) with the path of current + direction from current to successor.
            
            current <- next element in frontier.
            WHILE current is explored DO        [1] 
                current <- next element in frontier.
                
        RETURN the path associated with current.
        
        
        *[1]:       Checking if the node was explored before adding the node won't work, in BFS the node can be
                added to the queue many times before it is actually expanded (unlike DFS). because BFS skims
                through the tree row by row. so if Node X was a child of Nodes A, B (which are of the same height)
                then X would be added to the queue for a second time before the first occurrence of X is explored and
                marked within the explored list.
                
                    an alternative is to configure our queue to not allow duplicates. (by keeping 
                old nodes instead of replacing) and checking before adding each node, but this will cost more in time,
                instead of having to check if explored contains the node (for every node), we will have to check that
                as well as to loop over the queue every time we add a new element to prevent duplicate (whether explicitly
                in the BFS method or implicitly within the queue class). 
    """
        
    frontier = util.Queue() #FIFO Queue to store nodes to be explored
    explored = []   #List that stores the already explored nodes (To avoid Exploring already explored nodes)
    
    current = (problem.getStartState(), [])    #set the current state to (Start state position, empty list that represents the path to Start state)
    while not problem.isGoalState(current[0]): #loop as long as we didn't reach the goal            
        explored.append(current[0]) #mark current as explored
                
        sucs = problem.getSuccessors(current[0]) #get the successors of the current state
        for f in sucs:  
            frontier.push((f[0], current[1] + [f[1]]))  #adding the node to the frontier as the tuple (position[x,y], path current(parent) node + direction from current to this node)
                
        current = frontier.pop()  #set the next state to the next state (last added state to the stack)
        while current[0] in explored:  #pick the current state to be not explored
            current = frontier.pop()
        
    return current[1]   #return the path to current (which is equal to the goal state after loop finishes)

def uniformCostSearch(problem):
    """
    REQUIRES:    problem is not null, problem is well defined (getStartState(), isGoalState(), getSuccessors() yield good results).
    EFFECTS:     returns a list that contains the direction to reach the goal state from the start state using the best path (each step has a different cost), uses
                 uniform cost search algorithm.
    CLAUSES:     for the big Maze, the number of nodes explored is 620.
    DESCRIPTION: searches the node that has the lowest total cost from start state first
    """
    
    """
    IMPLEMENTATION IDEA:
        Similar To BFS, Instead of using a queue we will use a priority queue with the total cost to reach a node from the start
        state as that node's priority. pop method would return the node with least priority, i.e. least cost. Ensures Optimality.
        
    IMPLEMENTATION SKETCH:  
        current <- (start state position[x,y], empty list representing the path to reach the start state, initial cost of zero).
        WHILE current is not the goal state DO
            mark current as explored.
            
            get successors of current.
            FOR each successor of current
                add successor to frontier (priority queue) as tuple 
                (position[x,y], path to current + direction from current to node, cost of current + step cost)
                with priority cost of current + step cost. 
            
            current <- next element in frontier.
            WHILE current is explored DO        [1]          
                current <- next element in frontier.
                
        RETURN the path associated with current.
        
        *[1]:       We allow duplicates in the priority queue. if the node was already explored then the if statement will return false
                and the duplicated elements will be discarded (if visited). if the node was not already explored then the pop method 
                will return the occurrence with the least priority (cost) first, then it would be marked as explored and other duplicates
                would be discarded.
    """
    
    frontier = util.PriorityQueue() #FIFO Queue to store nodes to be explored
    explored = []   #List that stores the already explored nodes (To avoid Exploring already explored nodes)

    current = (problem.getStartState(), [], 0)    #set the current state to (Start state position, empty list that represents the path to Start state, initial cost of 0)
    while not problem.isGoalState(current[0]): #loop as long as we didn't reach the goal            
        explored.append(current[0]) #mark current as explored
                
        sucs = problem.getSuccessors(current[0]) #get the successors of the current state
        for f in sucs:  
            frontier.push((f[0], current[1] + [f[1]], current[2] + f[2]), current[2] + f[2])  #adding the node to the frontier as the tuple (position[x,y], path current(parent) node + direction from current to this node, total cost from start state) with that cost being the priority
                
        current = frontier.pop()  #set the next state to the next state (last added state to the stack)
        while current[0] in explored:  #pick the current state to be not explored
            current = frontier.pop()
        
    return current[1]   #return the path to current (which is equal to the goal state after loop finishes)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    REQUIRES:    problem is not null, problem is well defined (getStartState(), isGoalState(), getSuccessors() yield good results).
    EFFECTS:     returns a list that contains the direction to reach the goal state from the start state using the best path (each step has a different cost), uses
                 uniform cost search algorithm.
    CLAUSES:     for the big Maze, the number of nodes explored is about 549 (ties in priority may make the number differ slightly).
    DESCRIPTION: Search the node that has the lowest combined cost and heuristic first.
    """
    
    """
    IMPLEMENTATION IDEA:
        Same as ucs, But we use the following function as priority for each node n in the priority queue
        Evaluation function f(n) = g(n) + h(n):
            g(n) = cost so far to reach n
            h(n) = estimated cost to goal from n (obtained via the heuristic method)
            f(n) = estimated total cost of path through n to goal
        
    IMPLEMENTATION SKETCH:  
        current <- (start state position[x,y], empty list representing the path to reach the start state, initial cost of zero).
        WHILE current is not the goal state DO
            mark current as explored.
            
            get successors of current.
            FOR each successor of current
                add successor to frontier (priority queue) as tuple 
                (position[x,y], path to current + direction from current to node, cost of current + step cost)
                with priority cost of current + step cost + heuristic function of the node. 
            
            current <- next element in frontier.
            WHILE current is explored DO        [1]          
                current <- next element in frontier.
                
        RETURN the path associated with current.
        
        *[1]:       We allow duplicates in the priority queue. if the node was already explored then the if statement will return false
                and the duplicated elements will be discarded (if visited). if the node was not already explored then the pop method 
                will return the occurrence with the least priority (cost) first, then it would be marked as explored and other duplicates
                would be discarded.
    """
    frontier = util.PriorityQueue() #FIFO Queue to store nodes to be explored
    explored = []   #List that stores the already explored nodes (To avoid Exploring already explored nodes)

    current = (problem.getStartState(), [], 0)    #set the current state to (Start state position, empty list that represents the path to Start state, initial cost of 0)
    while not problem.isGoalState(current[0]): #loop as long as we didn't reach the goal            
        explored.append(current[0]) #mark current as explored
                
        sucs = problem.getSuccessors(current[0]) #get the successors of the current state
        for f in sucs:
            priority = current[2] + f[2] + heuristic(f[0], problem)  #calculating the Evaluation function for the node: f(n) = g(n) + h(n) = current cost + step cost + heuristic(node)
            frontier.push((f[0], current[1] + [f[1]], current[2] + f[2]), priority)  #adding the node to the frontier as the tuple (position[x,y], path current(parent) node + direction from current to this node, total cost from start state) with the Evalution Function as the priority
                
        current = frontier.pop()  #set the next state to the next state (last added state to the stack)
        while current[0] in explored:  #pick the current state to be not explored
            current = frontier.pop()
        
    return current[1]   #return the path to current (which is equal to the goal state after loop finishes)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
