class Tictactoe:

	def __init__(self, creator, other_player):
		#other user is the member that got challenged
		#creator gets the x
		#other_user gets the o
		self.x = creator
		self.o = other_player
		self.turn = self.x
		#empyt board
		self.board = [["-", "-", "-"],["-", "-", "-"], ["-", "-", "-"]]
		


	def getBoard(self):
		out = ""
		for r in range(len(self.board)):
			out += "| "
			for c in self.board[r]:
				out += c + " | "
			if r != 2:
				out += "\n" + "|---+---+---|" + "\n"
		if self.turn == self.x: 
			return out + "\nturn: " + self.x
		else: 
			return out + "\nturn: " + self.o
		# for i in self.board
		# 	out += "| " + str(i) + " "
		# 	if i==2 or i==5 :
		# 		out += "| \n" + "|---+---+---|" + "\n"
		# 	if i==8:
		# 		out += "|"
		# return out


	def updateTurn(self):
		if self.turn == self.x:
			self.turn = self.o
		else:
			self.turn = self.x

	def addMark(self, player, move):
		if player == self.x:
			return "x"
		else:
			return "o"

	#move is a tuple (row,column)
	def makeMove(self, player, move):
		#check if it is player's turn
		if player != self.turn:
			return "This isn't your turn"
		#check if move if valid
		if move[0] < 0 or move[0]>2 or move[1] < 0 or move[1]>2:
			return "Invalid move"
		
		#add that move to the board and change turns
		if self.board[move[0]][move[1]] == "-":
			self.board[move[0]][move[1]] = self.addMark(player)
			self.updateTurn()
			return self.getBoard()

		else:
			return "cell isn't empty, try again"


	#self.board = [["-", "-", "-"],["-", "-", "-"], ["-", "-", "-"]]
	def isGameOver(self):
		#check rows:
		for row in self.board:
			x_counter = 0
			o_counter = 0
			for mark in row:
				if mark == 'x':
					x_counter += 1
				elif mark == 'o':
					o_counter +=1
			if x_counter == 3:
				return self.x
			elif o_counter == 3:
				return self.o

		#check colums:

		#check diagonals:







game = Tictactoe("me", "you")
game.makeMove(game.x, (0,0))
print game.makeMove(game.o, (0,1))
# print game.getBoard()



