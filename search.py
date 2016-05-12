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
	
	#getting possible start states for the initial configuration of game
	
	stackGS = []
	
	#for startPos in startStates:
		#pegSolitaireObject = copySolitaireObject
	for depth in range(10000):
			#flag = playGame(pegSolitaireObject, startPos, gameState, depth)
		flag = playGameNew(pegSolitaireObject, depth, stackGS)
		if flag == 1:
			return True
		if flag == 0:
			del stackGS[:]
						
	
	return True


def getStartStates(gameState):
	
	startStates = []
	for i in range(7):
		for j in range(7):
			if gameState[i][j] == 1:
				startStates.append([i,j])

	return startStates


def playGameNew(pegSolitaireObject, depth, stackGS):
	if check_goal_state(pegSolitaireObject.gameState) :
		print "getting goal state...."
		return 1
	elif depth == 0:	
		return 0
	
	result = 0
	for i in range(7):
		for j in range(7):
			if pegSolitaireObject.gameState[i][j] == 1:
				for direction in config.DIRECTION:
					print "checking valid move for depth",i, j, depth
					flag = pegSolitaireObject.is_validMove([i, j], config.DIRECTION[direction])	
					if flag == True:
						pegSolitaireCopy = copy.deepcopy(pegSolitaireObject)
						print "initial state ", pegSolitaireCopy.gameState
						pegSolitaireCopy.getNextState([i, j], config.DIRECTION[direction])
						print "updated state ", pegSolitaireCopy.gameState
						#stackGSi.append(pegSolitaireCopy)
						result = playGameNew(pegSolitaireCopy, depth-1, stackGS)
						pegSolitaireObject.nodesExpanded = pegSolitaireCopy.nodesExpanded 
										
		
						if result == 1:	
							pegSolitaireObject.trace = pegSolitaireCopy.trace						
							return 1
						



	return result

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


def check_goal_state(gameState):

	print "in check goal state", gameState	
	for i in range(7):
		for j in range(7):
			if gameState[i][j] == 1 :
				#if i < 3 or j < 3 or i > 3 or j > 3:
				if i != 3 or j != 3:
					return False				
			
	if gameState[3][3] == 0:
		return False
	
	print "returning true..."
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

	print "initial state", pegSolitaireObject.gameState

	while not pq.empty():
		
		array_pq = pq.get()
		print "popped state ",array_pq[1].gameState
		print "value ", array_pq[0] 
		pegSolitaireTemp = array_pq[1]	

		if check_goal_state(pegSolitaireTemp.gameState):
			print "node expanded in temp ", pegSolitaireTemp.nodesExpanded
			pegSolitaireObject.nodesExpanded = pegSolitaireTemp.nodesExpanded
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
							hn = heuristic(pegSolitaireCopy)
							gn = pegSolitaireCopy.nodesExpanded
							#pq.put((hn+gn, pegSolitaireCopy))
							print "gn hn for state ", i, j, direction
							print hn, gn
							pq.put((-(hn+gn), pegSolitaireCopy))
			


	return False	

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
	return True
