# tictactoe

Slash command tictactoe

For the server I used local tunnel:

	From localtunnel.github.io

	Quickstart

		Install Localtunnel globally (requires NodeJS) to make it accessible anywhere:

		npm install -g localtunnel
		Start a webserver on some local port (eg http://localhost:8000) and use the command line interface to request a tunnel to your local server:

		lt --port 8000

	This provides with link, that will be used in the slack integration settings:

	For example if the link is https://shzxxenktk.localtunnel.me
	The URL must be https://shzxxenktk.localtunnel.me/ttt

	After that, just run python main.py

	And start the game! 

	PS: For security reason: My token wasnt exposed: 
		In line 8 of main.py:
		slack_token = "PUT YOUR TOKEN HERE"
		change that with the token (I will email it out to the recruiter)

	localtunnel might stop working, so just run lt --port 8000 and change the URL in 
	the slack integration website. 
