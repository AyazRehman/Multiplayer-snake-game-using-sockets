import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint

height = 20
width = 50
max_width = width-2
max_height = height-2
snake_length = 3
TIMEOUT=100


class Snake():

    def __init__(self,snake_x,snake_y):
        self.snake_body=[]
        self.alive=True
        self.headDeath=False
        self.body=[]
        self.fruit_score=0
        self.kill_score=0 
        self.length=snake_length
        self.direction=KEY_RIGHT
        self.REV_MAP = {
        KEY_UP: KEY_DOWN, KEY_DOWN: KEY_UP,
        KEY_LEFT: KEY_RIGHT, KEY_RIGHT: KEY_LEFT,
        }
        for x in range(snake_length):
         self.body.append([snake_x-x,snake_y])

    #make sure that sure does not move when opposite keys are pressed
    def change_direction(self,key):
        if(key==0):
           return
        if key != self.REV_MAP[self.direction]:
            self.direction = key
        self.update(self.direction)
    #snake grows when fruit is eaten
    def grow(self):
        new_part = [self.body[-1][0] - 1, self.body[-1][1]]
        self.body.append(new_part)
        self.fruit_score+=1
    #Snake moves by placing the tail in place of head
    def update(self, key):
        head = self.body[0]
        tail = self.body.pop()
        if key == KEY_RIGHT:         
            tail[0]= head[0] + 1
            tail[1] = head[1]      
        elif key == KEY_LEFT:
            tail[0]= head[0] - 1
            tail[1] = head[1]      
        elif key == KEY_UP:
            tail[0]= head[0]
            tail[1] = head[1]-1      
        elif key == KEY_DOWN:
            tail[0] = head[0]
            tail[1] = head[1] +1      

        self.body.insert(0, tail)
