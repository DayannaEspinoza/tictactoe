import webapp2
import random
from slacker import Slacker
import json
import model


slack_token = "PUT YOUR TOKEN HERE"
slack = Slacker(slack_token)

game_instance = None



class Home(webapp2.RequestHandler):
    """A GET Request Handler"""

    def get(self):
        """Receives a GET request"""

        self.response.write('Hello, running!')


class Game(webapp2.RequestHandler):
    """A POST Request Handler"""

    def get(self):
        """Receives a GET request"""
        global game_instance
        handlers(inp_array, channel_id, self)



    def post(self):
        """Receives a POST request"""

        global game_instance

        inp= self.request.get('text')
        channel_id = self.request.get('channel_id')
        inp_array = inp.split()
        handlers(inp_array, channel_id, self)


def handlers (inp_array, channel_id, self):

	global game_instance

	valid_commands = ["invite", "move", "board", "end", "help"]
	valid_moves = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

	if inp_array[0].lower() == "invite":
		if game_instance != None:
			text = "Game is currently being played in this channel. Wait until game is over or visit other channel"
			print_slack(text, channel_id, self)

		if game_instance == None:
			mention = inp_array[1]
			channel_id = self.request.get('channel_id')
			current_user_name = self.request.get('user_name')
			current_user_id = self.request.get('user_id')
			other_user_id = get_user_id(mention, channel_id, self)

			if other_user_id == "invalid":
				text = "Mention was invalid. Invite a member in this channel by typing invite @VALIDMEMBER"
				print_slack (text, channel_id, self)
				return

			else:
				other_user_name = get_user_name(other_user_id, channel_id, self)
				game_instance = model.Tictactoe(current_user_id, current_user_name, other_user_id, other_user_name, channel_id)
		        text = current_user_name + " challenged " + "@"+other_user_name+ "\n turn: " + current_user_name
		        print_slack (text, channel_id, self)


	if inp_array[0].lower() == "move":
		user_id = self.request.get('user_id')
		move = inp_array[1]

		if game_instance != None:

			if self.request.get('channel_id') == game_instance.channel and user_id != game_instance.x and user_id != game_instance.o:
				text = "You aren't playing the game. Wait until the game ends" 
				print_slack (text, channel_id, self)

			if self.request.get('channel_id') == game_instance.channel and  user_id != game_instance.turn:
				text = text = "This isn't your turn, wait until other player makes a move. \n player's turn: "+ game_instance.getTurnName(game_instance.turn) + "\n board: \n"+ game_instance.getBoard()
				print_slack(text, channel_id, self)

			if self.request.get('channel_id') == game_instance.channel and user_id == game_instance.turn:
				if move in valid_moves:
					text = game_instance.makeMove(user_id, int(move))
					if game_instance.isGameOver()[0]:
						game_instance = None
					print_slack (text, channel_id, self)
    			if move not in valid_moves:
    				text = "Invalid move. \nValid move is a integer from 1 to 9.\nplayer's turn: "+ game_instance.getTurnName(game_instance.turn) + "\n board: \n"+ game_instance.getBoard()
    				print_slack (text, channel_id, self)		

		else:
			text = "There isn't a game being played.\nTo start a game TYPE invite @mention"
			print_slack (text, channel_id, self)



	if inp_array[0].lower() == "board":
		if game_instance != None:
			if self.request.get('channel_id') == game_instance.channel:
				text = game_instance.getBoard()+"\nturn: " + game_instance.getTurnName (game_instance.turn)
				print_slack (text, channel_id, self)
		# if game_instance == None:
		else:
			text = "There isn't any game being played.\nTo start a game TYPE: invite @memtion"
			print_slack(text, channel_id, self)


	if inp_array[0].lower() == "end":

		if game_instance == None:
			text = "There isn't any game being played.\nTo start a game TYPE: invite @memtion"
			print_slack (text, channel_id, self)

		# if game_instance != None:
		else:
			if self.request.get('channel_id') == game_instance.channel and (self.request.get('user_id') == game_instance.x or self.request.get('user_id') == game_instance.o):
				game_instance = None
				text = self.request.get('user_name') + " ended the game"
				print_slack (text, channel_id, self)
				return game_instance
			else:
				text = "You aren't playing the game, only current players can end the game"
				print_slack (text, channel_id, self)
				return

	if inp_array[0].lower() == "help":
		text = "Invite a player by typing: INVITE @mention \n"
		text += "Only current players can make moves or end the game\n"
		text += "To make a valid MOVE choose numbers from 1-9 \n| 1 | 2 | 3 |\n| 4 | 5 | 6 |\n| 7 | 8 | 9 |\n For example: MOVE 2 \n"
		text += "To end the game type in END\n"
		text += "Any member in the channel can see the board and whose turn is it by typing BOARD\n"
		text += "There could be only one game being played at the time in a channel\n"
		print_slack(text, channel_id, self)


	if inp_array[0].lower() not in valid_commands:
		text = inp_array[0].lower() +" is not a valid command. Try typing "
		for command in valid_commands:
			text += command + ", "
		print_slack(text, channel_id, self)


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
		else: 
			return "invalid"
	else:
		return "invalid"

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



def main():
    """Runs webservice"""

    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')


if __name__ == '__main__':
    main()



