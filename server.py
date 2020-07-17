import socket
import threading
import pickle
import pickle
import sys
import random
from sannp import Snake

host=sys.argv[1]
port=int(sys.argv[2])
player=int(sys.argv[3])
height = 20
width = 50

class server:
    #Setup the server
    def __init__(self):
        self.players_number=player      #Number of players that can join this network
        self.snakes_players=[]          #This list will contain the snake objects
        self.fruit=[]
        self.render()                   #Where the snakes are born hehhehe :)))
        try:
            self.Soc_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Soc_con.bind((host, port))
            self.Soc_con.listen(0)
            print("Server listening")
        except socket.error:
            print("Error in code3")
        
    #Snakes initialise
    def render(self):
        x_cords=random.sample(range(5,30),self.players_number)
        y_cords=random.sample(range(5,19),self.players_number)
        self.fruit=[random.randint(4,45),random.randint(5,15)]
        for i in range(self.players_number):
             self.snakes_players.append(Snake(x_cords[i],y_cords[i]))
    def remover(self,list,snake):
        ret_list=[]
        for mem in list:
            if mem==snake:
                continue
            else:
                ret_list.append(mem)
        return ret_list
    #In order to close the connection when the client dies i have made sure that when the data is sent then the first member is the client's snake so that client could easily distinguish itself from others
    def serverData(self,player_connection,snake):
        opplist=self.remover((self.snakes_players),snake)
        # print(self.snakes_players[0].body)
        data = [snake] + opplist + [self.fruit]+ [threading.active_count()] + [self.players_number]
        player_connection.sendall(pickle.dumps(data))
      
    

    #Thread for each player allow to just build a single code for each snake and hence all other players will follow the same code
    def parallel_thread(self,player_connection,player_IP,player_snake):
        #Sending data to respective threaded player before the start of game so that it could spawn every snake
        self.serverData(player_connection,player_snake)

        #The game cycle which will continue unless the snake dies
        while True:
            #key Dir in pickled form from client
            try:
              Player_dir=player_connection.recv(2048)
            except:
                player_connection.close()
                sys.exit()
            try:
                direction=pickle.loads(Player_dir)
            except:
                player_connection.close()               
                break;
            if direction==27:
                player_connection.close()
                break;

            if direction ==0:
                 self.serverData(player_connection,player_snake)
                 continue
                
            player_snake.change_direction(direction)
            
            head = player_snake.body[0]
            # If Snake touches wall or its own body
            if head[0]<2 or head[0]>48 or head[1]<2 or head[1]>18 or head in player_snake.body[1:]:
                player_snake.alive = False
           

            if head == self.fruit:
                player_snake.grow()
                self.fruit=[random.randint(4,45),random.randint(5,15)]
          

            # Cases: Player hits the opponent
            opponent = self.remover((self.snakes_players), player_snake )
            for enemy in opponent:
                # Case: If Player has head collision with opponent
                if player_snake.body[0] == enemy.body[0]:
                    player_snake.alive = False
                    enemy.alive = False
                    player_snake.headDeath = True
                    enemy.headDeath = True
                elif player_snake.body[0] in enemy.body:
                    player_snake.alive = False
                    enemy.kill_score=enemy.kill_score+1
            # sending coor after the update
            self.serverData(player_connection,player_snake)
        
        player_connection.close()
        return

    def server_connection(self):
        try:
            for player in range(len(self.snakes_players)):
                c,ip_port=self.Soc_con.accept()
                c.settimeout(10)
                print("New connection formed")
                print("Ip address:",ip_port[0])
                print("connection on port no:",ip_port[1])
                try:
                     threading.Thread(target=self.parallel_thread, args=(c, ip_port, self.snakes_players[player])).start()
                except:
                    c.close()
        except:
            print("Error in connection")



#Starting connection
game_server=server()
#conneccting players
game_server.server_connection()





