import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint
import socket
import pickle
import sys
import time
import json
import threading

host=sys.argv[1]
port=int(sys.argv[2])

          
class snakemanager():
     
    def __init__(self,add,port):  
          self.client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.gamestart=False
          self.players=[]
          self.fruit=[]
          self.diff=0
          self.counter=True
          self.key=KEY_RIGHT
          #Connecting to server
          try:
                self.client.connect((host, port)) 
                self.client_data()
          except socket.error:
            print("Connection failed")
    
    #Data that client will be using
    def client_data(self):
          data=pickle.loads(self.client.recv(2048))
          num_players=data.pop()
          online_player=data.pop()-1
          self.diff=num_players-online_player
          self.fruit=data.pop()
          if(online_player == num_players):
            self.gamestart=True
          self.players=data

    #Data that is sent to server
    def data_to_server(self,key):
        self.client.sendall(pickle.dumps(key))

    #The display that clients sees
    def printing(self): 
          stdscr = curses.initscr()
          curses.curs_set(0)
          window = curses.newwin(20, 50, 0, 0)
          window.keypad(1)
          window.border(0)
          self.key = KEY_RIGHT      # Default orientation of snake
          window.timeout(400)
          while(True):

                if not self.gamestart:
                    window.clear()
                    window.addstr(10,2,"Remaining players to be connected: {}".format(self.diff))
                    window.refresh()
                    window.border(0)
                    self.data_to_server(0)
                    self.client_data()
                    continue
                
                if  self.players[0].alive!=True:
                    curses.endwin()   
                    print("Game Over!")
                    othersDeadToo = True

                    for snake in self.players:
                        if snake.alive:
                            othersDeadToo = False  

                    if othersDeadToo and self.players[0].headDeath:
                       print("Draw!")
                       time.sleep(5)
                       break;

                    elif othersDeadToo and not self.players[0].headDeath:
                       print("You won!")
                       time.sleep(5)
                       break;
                        
                    elif not othersDeadToo:
                        print("You lost!")
                        time.sleep(5)
                        break;
                    break
                bonus_window=curses.newwin(10, 50, 21, 0)
                bonus_window.clear()
                bonus_window.keypad(1)
                bonus_window.border(0)
                window.clear()
                window.addch(self.fruit[1], self.fruit[0], "F")
                char="O"
                for snake in self.players:
                    if snake.alive:
                        for bodyPart in snake.body:
                            if self.counter:
                                window.addch(bodyPart[1], bodyPart[0], "@")
                                self.counter=False
                            else:
                                window.addch(bodyPart[1], bodyPart[0], char)
                        char="x"
                        self.counter=True
                self.counter=True
                bonus_window.clear()
                bonus_window.addstr(0,0,"Kill counter {}".format(self.players[0].kill_score))
                bonus_window.addstr(1,0,"Fruit counter {}".format(self.players[0].fruit_score))
                bonus_window.refresh()


                  
                window.border(0)
                window.refresh()
                event = window.getch()
                if  event == 27:   
                    curses.endwin()
                    self.key=event
                    self.data_to_server(self.key)
                    self.client.close()
                    print("You closed the Connection")
                    time.sleep(5)
                    return
                elif event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
                   self.key = event
                try:
                    self.data_to_server(self.key)
                    self.client_data()
                except:
                    self.close()

            # except:
            #     curses.endwin()
            #     client.close()
    def close(self):
         self.client.close()
         return

client=snakemanager(host,port)
client.printing()
curses.endwin()
client.close()



                
           
