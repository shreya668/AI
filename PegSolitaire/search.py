import pegSolitaireUtils
import config
import sys
import copy
import Queue

def ItrDeepSearch(pegSolitaireObject):
	#################################################
	# Must use functions:
	# getNextState(self,oldPos, direction)
	# 
	# we are using this function to count,
	# number of nodes expanded, If you'll not
	# use this grading will automatically turned to 0
	#################################################
	#
	# using other utility functions from pegSolitaireUtility.py
	# is not necessary but they can reduce your work if you 
	# use them.
	# In this function you'll start from initial gameState
	# and will keep searching and expanding tree until you 
	# reach goal using Iterative Deepning Search.
	# you must save the trace of the execution in pegSolitaireObject.trace
	# SEE example in the PDF to see what to save
	#
	#################################################
	depth = 1
	copySolitaireObject = copy.deepcopy(pegSolitaireObject)
	gameState = pegSolitaireObject.gameState
	
	#iterative call to recursiveIDS() which calls getNextState() recursively for updating game state
	##################################################
	flag = 0
	for depth in range(20):
		flag = recursiveIDS(pegSolitaireObject, depth)
		if flag == 1:
			return True
	
	
	#after checking for maximum depth, if still goal stae not found 
	#return goal state not found
	###################################################
	if flag == 0:
		pegSolitaireObject.trace = ['NO GOAL STATE FOUND']
		return False			
	
	return True


###########################################
#Recursive Iterative Deepening Search function
#picks valid move from the board and calls recursiveIDS
#with new GameState and depth-1
############################################
def recursiveIDS(pegSolitaireObject, depth):
	if check_goal_state(pegSolitaireObject.gameState) :
		return 1
	elif depth == 0:	
		return 0
	
	result = 0
	for i in range(7):
		for j in range(7):
			if pegSolitaireObject.gameState[i][j] == 1:
				for direction in config.DIRECTION:
					flag = pegSolitaireObject.is_validMove([i, j], config.DIRECTION[direction])	
					if flag == True:
						pegSolitaireCopy = copy.deepcopy(pegSolitaireObject)
						pegSolitaireCopy.getNextState([i, j], config.DIRECTION[direction])
						result = recursiveIDS(pegSolitaireCopy, depth-1)
						pegSolitaireObject.nodesExpanded = pegSolitaireCopy.nodesExpanded 
										
						flag_move = True			
						if result == 1:	
							pegSolitaireObject.trace = pegSolitaireCopy.trace
							return result


	return result


#function to check if current gameState is goal state
def check_goal_state(gameState):

	for i in range(7):
		for j in range(7):
			if gameState[i][j] == 1 :
				#if i < 3 or j < 3 or i > 3 or j > 3:
				if i != 3 or j != 3:
					return False				
			
	if gameState[3][3] == 0:
		return False
	
	return True


def aStarOne(pegSolitaireObject):
	#################################################
        # Must use functions:
        # getNextState(self,oldPos, direction)
        # 
        # we are using this function to count,
        # number of nodes expanded, If you'll not
        # use this grading will automatically turned to 0
        #################################################
        #
        # using other utility functions from pegSolitaireUtility.py
        # is not necessary but they can reduce your work if you 
        # use them.
        # In this function you'll start from initial gameState
        # and will keep searching and expanding tree until you 
	# reach goal using A-Star searching with first Heuristic
	# you used.
        # you must save the trace of the execution in pegSolitaireObject.trace
        # SEE example in the PDF to see what to return
        #
        #################################################
	

	pq = Queue.PriorityQueue()
	pq.put((0, pegSolitaireObject))

	count_nodes=0

	while not pq.empty():
		
		array_pq = pq.get()
		pegSolitaireTemp = array_pq[1]

		if check_goal_state(pegSolitaireTemp.gameState):
			pegSolitaireObject.trace = pegSolitaireTemp.trace
			pegSolitaireObject.nodesExpanded = count_nodes
			return True

		for i in range(7):
			for j in range(7):
				if pegSolitaireTemp.gameState[i][j] == 1:
					for direction in config.DIRECTION:
						pegSolitaireCopy = copy.deepcopy(pegSolitaireTemp)
						flag = pegSolitaireCopy.is_validMove([i, j], config.DIRECTION[direction])
                                        	if flag == True:				
							pegSolitaireCopy.getNextState([i, j], config.DIRECTION[direction])
							hn = heuristic(pegSolitaireCopy)
							gn = pegSolitaireCopy.nodesExpanded
							count_nodes = count_nodes+1
							pq.put((-(hn+gn), pegSolitaireCopy))
			

	pegSolitaireObject.trace = ['NO GOAL STATE FOUND']
	return False	

#################################
#heuristic1
#heuristic based on number of valid moves left on the board after
#a move is played
#################################
def heuristic(pegSolitaireObject):
	count = 0
	for i in range(7):
		for j in range(7):
			if pegSolitaireObject.gameState[i][j] == 1:
				for direction in config.DIRECTION:
					flag = pegSolitaireObject.is_validMove([i, j], config.DIRECTION[direction])
					if flag == True:
						count = count + 1												
	return count


def aStarTwo(pegSolitaireObject):
	#################################################
        # Must use functions:
        # getNextState(self,oldPos, direction)
        # 
        # we are using this function to count,
        # number of nodes expanded, If you'll not
        # use this grading will automatically turned to 0
        #################################################
        #
        # using other utility functions from pegSolitaireUtility.py
        # is not necessary but they can reduce your work if you 
        # use them.
        # In this function you'll start from initial gameState
        # and will keep searching and expanding tree until you 
        # reach goal using A-Star searching with second Heuristic
        # you used.
        # you must save the trace of the execution in pegSolitaireObject.trace
        # SEE example in the PDF to see what to return
        #
        #################################################

	pq = Queue.PriorityQueue()
	pq.put((0, pegSolitaireObject))
	count_nodes = 0


	while not pq.empty():
		
		array_pq = pq.get()
		pegSolitaireTemp = array_pq[1]	

		if check_goal_state(pegSolitaireTemp.gameState):
			pegSolitaireObject.nodesExpanded = count_nodes
			pegSolitaireObject.trace = pegSolitaireTemp.trace
			return True

		for i in range(7):
			for j in range(7):
				if pegSolitaireTemp.gameState[i][j] == 1:
					for direction in config.DIRECTION:
						pegSolitaireCopy = copy.deepcopy(pegSolitaireTemp)
						flag = pegSolitaireCopy.is_validMove([i, j], config.DIRECTION[direction])
                                        	if flag == True:				
							pegSolitaireCopy.getNextState([i, j], config.DIRECTION[direction])
							hn = heuristic_2(pegSolitaireCopy)
							gn = pegSolitaireCopy.nodesExpanded
							count_nodes = count_nodes+1
							pq.put((-(hn+gn), pegSolitaireCopy))
			

	pegSolitaireObject.trace = ['NO GOAL STATE FOUND']
	return False


###################################
#heuristic2
#heuristic based on number of empty holes on the game board
####################################
def heuristic_2(pegSolitaireObject):
	count = 0
	for i in range(7):
		for j in range(7):
			if pegSolitaireObject.gameState[i][j] == 0:
				count = count + 1
	return count
