class Tictactoe:

	def __init__(self, creator, other_player):
		#other user is the member that got challenged
		#creator gets the x
		#other_user gets the o
		self.x = creator
		self.o = other_player
		self.turn = self.x
		#empyt board
		self.board = {1:"-", 2:"-", 3:"-", 4:"-", 5:"-", 6:"-", 7:"-", 8:"-", 9:"-"}
		

	def getBoard(self):
		out = ""
		out += "| " + self.board[1] + " | " + self.board[2] + " | " + self.board[3] + " |"
		out += "\n" + "|---+---+---|" + "\n"
		out += "| " + self.board[4] + " | " + self.board[5] + " | " + self.board[6] + " |"
		out += "\n" + "|---+---+---|" + "\n"
		out += "| " + self.board[7] + " | " + self.board[8] + " | " + self.board[9] + " |"
		return out



	def updateTurn(self):
		if self.turn == self.x:
			self.turn = self.o
		else:
			self.turn = self.x


	def addMark(self, player):
		if player == self.x:
			return "x"
		else:
			return "o"

	#move is a position: 1,2,3,..,9
	#if move is valid, add to the board and update the turn and show board and next turn,
	#if an user win, show board and tell that user won the game
	def makeMove(self, player, move):
		#check if it is player's turn
		if player != self.turn:
			return "This isn't your turn"
		#check if move if valid
		if move not in self.board:
			return "Invalid move"
		
		#add that move to the board and change turns
		if self.board[move] == "-":
			self.board[move] = self.addMark(player)
			if self.isGameOver():
				return self.getBoard() + "\n"+self.isGameOver()
			# self.isGameOver()
			self.updateTurn()
			return self.getBoard() +  "\n player's turn: "+self.turn

		else:
			return "cell isn't empty, try again"



	def isGameOver(self):
		#check rows, columns and diagonals
		if ((self.board[1] == self.board[2] == self.board[3] != "-") or 
			(self.board[4] == self.board[5] == self.board[6] != "-") or 
			(self.board[7] == self.board[8] == self.board[9] != "-") or 
			(self.board[1] == self.board[4] == self.board[7] != "-") or 
			(self.board[2] == self.board[5] == self.board[8] != "-") or 
			(self.board[3] == self.board[6] == self.board[9] != "-") or 
			(self.board[1] == self.board[5] == self.board[9] != "-") or 
			(self.board[3] == self.board[5] == self.board[7] != "-")):
			return "winner is "  + self.turn 
		else: 
			return None







game = Tictactoe("me", "you")
print "me " + game.makeMove(game.x, 1) + "\n"
print "you " + game.makeMove(game.o, 2) +"\n"
print "me " + game.makeMove(game.x, 4)+"\n"
# print game.isGameOver()
print "you " +game.makeMove(game.o, 3) +"\n"
print "me " + game.makeMove(game.x, 7)+"\n"
# print game.isGameOver()
# print game.makeMove(game.o, 5)
# print game.isGameOver()
# print game.getBoard()



