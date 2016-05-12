import readGame

#######################################################
# These are some Helper functions which you have to use 
# and edit.
# Must try to find out usage of them, they can reduce
# your work by great deal.
#
# Functions to change:
# 1. is_wall(self, pos):
# 2. is_validMove(self, oldPos, direction):
# 3. getNextPosition(self, oldPos, direction):
# 4. getNextState(self, oldPos, direction):
#######################################################
class game:
	def __init__(self, filePath):
        	self.gameState = readGame.readGameState(filePath)
                self.nodesExpanded = 0
		self.trace = []
	
	def is_corner(self, pos):
		########################################
		# You have to make changes from here
		# check for if the new positon is a corner or not
		# return true if the position is a corner

		if self.gameState[pos[0]][pos[1]] == -1:
			return True

		return False	
	
	
	def getNextPosition(self, oldPos, direction):
		#########################################
		# YOU HAVE TO MAKE CHANGES HERE
		# See DIRECTION dictionary in config.py and add
		# this to oldPos to get new position of the peg if moved
		# in given direction , you can remove next line
		
		newPos = []
		newPos.append(oldPos[0]+(2*direction[0]))
		newPos.append(oldPos[1]+(2*direction[1])) 
		

		return newPos 
	
	
	def is_validMove(self, oldPos, direction):
		# or new move is outside peg Board
		newPos = self.getNextPosition(oldPos, direction)
		if (newPos[0] < 0 or newPos[0] > 6) or (newPos < 0 or newPos[1] > 6) :
			return False		

		#########################################
		# DONT change Things in here
		# In this we have got the next peg position and
		# below lines check for if the new move is a corner
		#newPos = self.getNextPosition(oldPos, direction)
		if self.is_corner(newPos):
			return False	
		#########################################
		
		########################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# check for cases like:
		# if new move is already occupied
		if self.gameState[newPos[0]][newPos[1]] == 1:
			return False 
	
		
		#check if next holder is occupied or not for the valid move
		checkPos = []
		checkPos.append(oldPos[0] + direction[0])
                checkPos.append(oldPos[1] + direction[1])

		if self.gameState[checkPos[0]][checkPos[1]] == 0:
			return False



		# Remove next line according to your convenience
		return True
	
	def getNextState(self, oldPos, direction):
		###############################################
		# DONT Change Things in here
		self.nodesExpanded += 1

		if not self.is_validMove(oldPos, direction):
			print "Error, You are not checking for valid move"
			return None
		###############################################
		
		###############################################
		# YOU HAVE TO MAKE CHANGES BELOW THIS
		# Update the gameState after moving peg
		# eg: remove crossed over pegs by replacing it's
		# position in gameState by 0
		# and updating new peg position as 1
		newPos = self.getNextPosition(oldPos,direction)
		
		#updating game state after moving peg
		self.gameState[newPos[0]][newPos[1]] = 1

		adjacentPos = []
		adjacentPos.append(oldPos[0] + direction[0])
		adjacentPos.append(oldPos[1] + direction[1])
	
		self.gameState[adjacentPos[0]][adjacentPos[1]] = 0	
		self.gameState[oldPos[0]][oldPos[1]] = 0
	
		self.trace.append(oldPos)
		self.trace.append(newPos)	

		return self.gameState	
