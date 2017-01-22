

class Tictactoe:

	""" Tictactoe model for the game

    Attributes:
        x 			tictactoe creator's id
        x_name 		tictactoe creator's username
        o 			tictactoe other player's id
        o_name 		tictactoe other player's username
        turn 		player's whose turn is. It could only be either x or o
        channel		channel id where the game happens
        board 		game board that stores marks and positions of the game
    """

	def __init__(self, creator_id, creator_name, other_player_id, other_player_name, channel):
		self.x = creator_id
		self.x_name = creator_name
		self.o = other_player_id
		self.o_name = other_player_name
		self.turn = self.x
		self.channel = channel
		#empyt board
		self.board = {1:"--", 2:"--", 3:"--", 4:"--", 5:"--", 6:"--", 7:"--", 8:"--", 9:"--"}
		

	def getBoard(self):
		"""
	    Creates the visual represention of self.board
	    It contains either "--" when a cell is empty or a number from 1-9 if the cell is occupied
	    Parameters: None
	    Return type: String
    	"""
		out = ""
		out += "| " + self.board[1] + " | " + self.board[2] + " | " + self.board[3] + " |\n"
		out += "| " + self.board[4] + " | " + self.board[5] + " | " + self.board[6] + " |\n"
		out += "| " + self.board[7] + " | " + self.board[8] + " | " + self.board[9] + " |"
		return out


	def updateTurn(self):
		"""
	    Update the player's turn every time a valid move happens
	    Parameters: None
    	"""
		if self.turn == self.x:
			self.turn = self.o
		else:
			self.turn = self.x


	def addMark(self, player):
		"""
	    Add "X" or "O" to the board to update the state its state.
	    Parameters: player either x or o
	    Return type: String represenation of the player ("X" for the creator and "O" for the other player)
    	"""
		if player == self.x:
			return "X"
		else:
			return "O"

	
	def makeMove(self, player, move):
		"""
	    Given a specific player and a move, it checks if the player and move are valid.
	    	If player and move arent valid, it outputs a string with feedback information
	    	If they are valid, it updates the board information, checks if the game is over, 
	    		update turns and outputs a string contains the board and whose turn is next
	    	If the game is over and there is a winner, it outputs a string with the board and the winner username
	    	If the game is over and there is a tie, it outputs a string with the board and "tie"

	    Parameters:
	    	player 	player id
	    	move    move input from the player
	    Return type: String

    	"""
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
		"""
	    Checks if the game is over. If the game is over 2 conditions coudld happen:
	    	win = If there is a winner
	    	tie = None of the players winner
	    If the game is over it outputs a tuple, where the first value is the boolean True 
	    	and the second value contains condition ("win", "tie")

	    If the game isnt over, it outputs a tuple, where the first value is the boolean False
	    	and the second value is None

	    Parameters: None
	    Return type: tuple (Boolean, String/None)
    	"""
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
		"""
	    Gets the username of the player whose turn is it
	    Parameters: turn_id  (x or o)
	    Return type: String (x_name or o_name)
    	"""
		if turn_id == self.x:
			return self.x_name
		elif turn_id == self.o:
			return self.o_name




game_instance = None
"""
Creates the game instance, to be initialized when the game starts
"""





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
# print game.makeMove("me", 9) TIE
