import webapp2
import random
from slacker import Slacker
import json
# import model

slack_token = "xoxp-125092052758-124344639443-128446735155-6c2ccd027d97239625490b3ede029263"
# slack_token = "PUT YOUR TOKEN HERE"
slack = Slacker(slack_token)

# game = Tictactoe(None, None)
# global game_instance
game_instance = None


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
		self.board = {1:"-", 2:"-", 3:"-", 4:"-", 5:"-", 6:"-", 7:"-", 8:"-", 9:"-"}
		

	def getBoard(self):
		out = ""
		out += "| " + self.board[1] + " | " + self.board[2] + " | " + self.board[3] + " |"
		out += "\n" + "|---|---|---|" + "\n"
		out += "| " + self.board[4] + " | " + self.board[5] + " | " + self.board[6] + " |"
		out += "\n" + "|---|---|---|" + "\n"
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

			return self.getBoard() +  "\n player's turn: "+ self.getTurnName(self.turn)

		else:
			return "cell is occupied, try again \nplayer's turn: "+ self.getTurnName(self.turn)



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
			return "winner is "  + self.getTurnName(self.turn)
		else: 
			return None


	def getTurnName (self, turn_id):
		if turn_id == self.x:
			return self.x_name
		elif turn_id == self.o:
			return self.o_name




class Home(webapp2.RequestHandler):
    """A GET Request Handler"""

    def get(self):
        """Receives a GET request"""

        self.response.write('Hello, running!')

    #     # game_instance = None
    #     # game_instance = handlers(inp_array, game_instance, channel_id, self)


class Game(webapp2.RequestHandler):
    """A POST Request Handler"""

    def get(self):
        """Receives a GET request"""
        global game_instance
        # self.response.write('Hello, running!')

        # game_instance = None
        handlers(inp_array, channel_id, self)



    def post(self):
        """Receives a POST request"""

        global game_instance

        inp= self.request.get('text')
        # channel_name = self.request.get('channel_name')
        channel_id = self.request.get('channel_id')

        inp_array = inp.split()

        handlers(inp_array, channel_id, self)

        # return game_instance


def handlers (inp_array, channel_id, self):

	global game_instance

	if inp_array[0].lower() == "invite":
		if game_instance == None:
			mention = inp_array[1]
			channel_id = self.request.get('channel_id')
			current_user_name = self.request.get('user_name')
			current_user_id = self.request.get('user_id')
			other_user_id = get_user_id(mention, channel_id, self)
			other_user_name = get_user_name(other_user_id, channel_id, self)
			
			game_instance = Tictactoe(current_user_id, current_user_name, other_user_id, other_user_name, channel_id)
	       
	        text = current_user_name + " challenged " + "@"+other_user_name+ "\n turn: " + current_user_name
	        self.response.headers['Content-type'] = 'application/json'
	        my_json = {'text': text, 'response_type': 'in_channel', 'channel': channel_id, 'command': '/ttt'}
	        test_json = json.dumps(my_json)
	        self.response.write(test_json)
        # if game_instance != None:
        # 	text = "game is currently being played in this channel. Wait until game is over or visit other channel"
        # 	print_slack (text, channel_id, self)


	if inp_array[0].lower() == "move":
		user_id = self.request.get('user_id')
		print "this user is: "+ user_id
		move = inp_array[1]

		if game_instance != None:

			if self.request.get('channel_id') == game_instance.channel and  user_id != game_instance.turn:
				text = text = "This isn't your turn, wait until other player makes a move. \n player's turn: "+ game_instance.getTurnName(game_instance.turn) + "\n board: "+ game_instance.getBoard()
				print_slack(text, channel_id, self)

			if self.request.get('channel_id') == game_instance.channel and user_id == game_instance.turn:
				if move in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
					text = game_instance.makeMove(user_id, int(move))
					print_slack (text, channel_id, self)
					print "changed turn: " + game_instance.turn
    			if move not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
    				text = "move is a integer from 1 to 9.\nplayer's turn: "+ game_instance.getTurnName(game_instance.turn)
    				print_slack (text, channel_id, self)

			if self.request.get('channel_id') == game_instance.channel and user_id != game_instance.x and user_id != game_instance.o:
				text = "You aren't playing the game. Wait until the game ends" 
				print_slack (text, channel_id, self)

		else:
			text = "There isnt a game being played.\nTo start a game TYPE invite @mention"
			print_slack (text, channel_id, self)



	if inp_array[0].lower() == "board":
		if game_instance != None:
			if self.request.get('channel_id') == game_instance.channel:
				text = game_instance.getBoard()+"\nturn: " + game_instance.getTurnName (game_instance.turn)
				print_slack (text, channel_id, self)
		if game_instance == None:
			if self.request.get('channel_id') == game_instance.channel:
				text = "There isn't any game being played.\nTo start a game TYPE: invite @memtion"
				print_slack(text, channel_id, self)


	if inp_array[0].lower() == "end":

		if game_instance == None:
			if self.request.get('channel_id') == game_instance.channel:
				text = "There isn't any game being played.\nTo start a game TYPE: invite @memtion"
				print_slack (text, channel_id, self)

		if game_instance != None:
			if self.request.get('channel_id') == game_instance.channel and (self.request.get('user_id') == game_instance.x or self.request.get('user_id') == game_instance.o):
				game_instance = None
				text = self.request.get('user_name') + " ended the game"
				print_slack (text, channel_id, self)
			else:
				text = "you aren't playing the game, only current players can end the game"
				print_slack (text, channel_id, self)


	return game_instance


def get_user_id(mention, channel_id, self):
	if mention[0] == "@":
		member = mention[1:]
		member_id = ""
		for user in slack.users.list().body['members']:
			if user['name'] == member:
				member_id = user["id"]

		if member_id in slack.channels.info(channel_id).body['channel']['members']:
			return member_id

def get_user_name(user_id, channel_id, self):
	for user in slack.users.list().body['members']:
			if user['id'] == user_id:
				return user["name"]

def print_slack (text, channel_id, self):
	self.response.headers['Content-type'] = 'application/json'
	my_json =  {'text': text, 'response_type': 'in_channel', 'channel': channel_id, 'command': '/ttt'}
	my_json_dump = json.dumps(my_json)
	self.response.write(my_json_dump)




app = webapp2.WSGIApplication([
                        (r'/', Home),
                        (r'/ttt', Game)
                        ],
                        debug=True)


# def __unicode__(self):
#    return unicode(self.some_field) or u''

def main():
    """Runs webservice"""

    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')


if __name__ == '__main__':
    main()



