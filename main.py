import webapp2
import random
from slacker import Slacker
import json
# import model

slack_token = "xoxp-125092052758-124344639443-127119724800-3979fca47818504b3675a09d04669c49"
slack = Slacker(slack_token)

# game = Tictactoe(None, None)
game_instance = None

class Home(webapp2.RequestHandler):
    """A GET Request Handler"""

    def get(self):
        """Receives a GET request"""

        self.response.write('Hello, running!')


class Game(webapp2.RequestHandler):
    """A POST Request Handler"""

    def post(self):
        """Receives a POST request"""

        inp= self.request.get('text')
        channel_name = self.request.get('channel_name')
        channel_id = self.request.get('channel_id')
        current_user_name = self.request.get('user_name')
        current_user_id = self.request.get('user_id')

        ##############
        other_user_id = None
        other_user_name = None

        get_input(inp, channel_id, self)
        ###########
        # other_user_id = get_other_user(inp, channel_id, self)[0]
        # other_user_name = get_other_user(inp, channel_id, self)[1]

        if other_user_id:
        	other_user_name = get_other_user_name(other_user_id, channel_id, self)
        	text = current_user_name +" challenged "+other_user_name
        	get_challenged_text(text, current_user_name, other_user_name, channel_id, self)
        	game_instance = Tictactoe(current_user_id, other_user_id)

        	play_tictactoe(inp, channel_id, current_user_name, self)
        


# def get_other_user(inp, channel_id, self):
# 	inp_array = inp.split()
# 	if "invite" == inp_array[0].lower():
# 		if inp_array[1][0] == "@":
# 			member = inp_array[1][1:]
# 			print member
# 			member_id = ""
# 			for user in slack.users.list().body['members']:
# 				if user['name'] == member:
# 					member_id = user["id"]

# 			if member_id in slack.channels.info(channel_id).body['channel']['members']:
# 				return (member_id, member)
# 	else:
# 		return "wrong command"

def get_input(inp, channel_id, self):
	inp_array = inp.split()
	action = inp_array[0]

	if "invite" == action.lower():
		print "GOT THE INVITE PART"
		other_user_name =  get_other_user_id(inp_array[1], channel_id, self)
		return other_user_name

	# if "display" == action.lower():
	# 	if game_instance == None:

def get_other_user_id(mention, channel_id, self):
	if mention == "@":
		member = mention[1:]
		# print member
		member_id = ""
		for user in slack.users.list().body['members']:
			if user['name'] == member:
				member_id = user["id"]

		if member_id in slack.channels.info(channel_id).body['channel']['members']:
			# other_user_id = member_id
			print "I GOT get other user id"
        	return member_id

def get_other_user_name(other_user_id, channel_id, self):
	for user in slack.users.list().body['members']:
			if user['id'] == other_user_id:
				return user["name"]


def get_challenged_text(text, current_user_name, other_user_name, channel_id, self):
	self.response.headers['Content-type'] = 'application/json'
	my_json = {'text': text, 'response_type': 'in_channel', 'channel': channel_id, 'command': '/ttt'}
	test_json = json.dumps(my_json)
	self.response.write(test_json)

def display_text(game_instance, channel_id, self):
	if game_instance == None:
		self.response.headers['Content-type'] = 'application/json'
		my_json = {'text': "Start inviting someone", 'response_type': 'in_channel', 'channel': channel_id, 'command': '/ttt'}
		test_json = json.dumps(my_json)
		self.response.write(test_json)
	else:
		self.response.headers['Content-type'] = 'application/json'
		text = "board: " + game_instance.getBoard() +"\nturn: " +game_instance.turn
		my_json = {'text': text, 'response_type': 'in_channel', 'channel': channel_id, 'command': '/ttt'}
		test_json = json.dumps(my_json)
		self.response.write(test_json)



# def start_game(current_user_id, other_user_id, channel_id, game_instance, self):
# 	game_instance = Tictactoe(current_user_id, other_user_id)




def play_tictactoe(inp, channel_id, current_user_name, self):
    """this plays rock paper scissors"""

    num = random.randint(0, 3)
    inp = inp.lower()

    # self.response.["response_type"] = "in_channel"

    # User picks rock
    if inp == "rock":

    	# self.response = json.dumps(json.loads(self.response.body).response_type = "in_channel")
    	# self.response.write("doing rocks")

    	self.response.headers['Content-type'] = 'application/json'
    	text = "@"+current_user_name+ " hellllllloooo"
    	my_json = {'text': text, 'response_type': 'in_channel', 'channel': channel_id, 'command': '/ttt'}
    	test_json = json.dumps(my_json)
    	self.response.write(test_json)




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



