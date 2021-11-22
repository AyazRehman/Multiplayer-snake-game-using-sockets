# Multiplayer-snake-game-using-sockets

This is a multiplayer snake game which you can play with your friends which are on the same network.

Step 1:
Run server on one machine by giving the following command: python3 server.py *IP address* *port* *number of players*.
E.g python3 server.py 127.0.0.1 8000 2

Step 2:
Each player runs the client file on its own system by giving the following command:python3 client.py *IP address* *port*
E.g python3 client.py 127.0.0.1 8000

I have used "curses" library to make the UI of the game. Hope you like the game.
