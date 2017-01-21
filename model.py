

class Tictactoe:

	def __init__(self, creator_id, creator_name, other_player_id, other_player_name, channel):
		#other user is the member that got challenged
		#creator gets the x
		#other_user gets the o
		self.x = creator_id
		self.x_name = creator_name
		self.o = other_player_id
		self.o_name = other_player_name
		self.turn = self.x
		self.channel = channel
		#empyt board
		self.board = {1:"--", 2:"--", 3:"--", 4:"--", 5:"--", 6:"--", 7:"--", 8:"--", 9:"--"}
		

	def getBoard(self):
		out = ""
		out += "| " + self.board[1] + " | " + self.board[2] + " | " + self.board[3] + " |\n"
		out += "| " + self.board[4] + " | " + self.board[5] + " | " + self.board[6] + " |\n"
		out += "| " + self.board[7] + " | " + self.board[8] + " | " + self.board[9] + " |"
		return out



	def updateTurn(self):
		if self.turn == self.x:
			self.turn = self.o
		else:
			self.turn = self.x


	def addMark(self, player):
		if player == self.x:
			return "X"
		else:
			return "O"

	#move is a position: 1,2,3,..,9
	#if move is valid, add to the board and update the turn and show board and next turn,
	#if an user win, show board and tell that user won the game
	# def makeMove(self, player, move):
	# 	#check if it is player's turn
	# 	if player != self.turn:
	# 		return "This isn't your turn"
	# 	#check if move if valid
	# 	if move not in self.board:
	# 		return "Invalid move"
		
	

	#returns the self object
	def makeMove(self, player, move):
		if player != self.turn:
			return "This isn't your turn"
		#if move is not 1-9
		if move not in self.board:
			return "Not a valid move"

		if self.board[move] == "--":
			self.board[move] = self.addMark(player)

			if self.isGameOver()[0]:
				board = self.getBoard()
				if self.isGameOver()[1] == "win":
					winner = self.getTurnName( self.turn)
					return board +"\nwinner is:" + winner
				if self.isGameOver()[1] == "tie":
					return board +"\nIt is a tie"
			else:
				self.updateTurn()
				return self.getBoard()+"\n turn: "+self.getTurnName(self.turn)
		else:
			#cell is occupied
			return "cell is occupied, try again \nplayer's turn: "+ self.getTurnName(self.turn)+ "\n board: \n"+ self.getBoard()


	def isGameOver(self):
		if ((self.board[1] == self.board[2] == self.board[3] != "--") or 
			(self.board[4] == self.board[5] == self.board[6] != "--") or 
			(self.board[7] == self.board[8] == self.board[9] != "--") or 
			(self.board[1] == self.board[4] == self.board[7] != "--") or 
			(self.board[2] == self.board[5] == self.board[8] != "--") or 
			(self.board[3] == self.board[6] == self.board[9] != "--") or 
			(self.board[1] == self.board[5] == self.board[9] != "--") or
			(self.board[3] == self.board[5] == self.board[7] != "--")):

			return (True, "win")

		is_a_tie = True
		for cell in range(1, 10):
			if self.board[cell] == "--":
				is_a_tie = False	

		if is_a_tie:

			return (True, "tie")

		else:
			return (False, None)





	def getTurnName (self, turn_id):
		if turn_id == self.x:
			return self.x_name
		elif turn_id == self.o:
			return self.o_name


game_instance = None





# game  = Tictactoe("me", "me_name", "you", "you_name", "chan")
# print game.getBoard()

# game.makeMove("me", 2)
# game.makeMove("you", 1)
# game.makeMove("me", 5)
# game.makeMove("you", 3)
# game.makeMove("me", 6)
# game.makeMove("you", 4)
# game.makeMove("me", 7)
# game.makeMove("you", 8)
# print game.makeMove("me", 9)
