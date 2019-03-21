# Add your Python code here. E.g.
from microbit import *
import radio
import random

#Position class, used to keep track of 2 dimensional positions0
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y



while True:
    sleep(random.randint(500, 4000))
    radio.on()
    server = False
    radio.send('server')
    
    display.scroll("Looking for opponents...", wait=False, loop=True)
    
    #wait for messages
    while True:
        incoming = radio.receive()

        if incoming is not None:
            if incoming == 'server':    #Join another players game
                server = False
                radio.send('client')
                break
            if incoming == 'client':    #Let other players join
                server = True
                break
    
    #present the server 
    if server == True :
        display.set_pixel(0, 0, 9)
    if server == False :
        display.set_pixel(0, 0, 3)
    
    #"Load" game
    sleep(100)
    
    display.scroll("3", wait=True, loop=False)
    display.scroll("2", wait=True, loop=False)
    display.scroll("1", wait=True, loop=False)
    
    
    #players properties
    local_player_position = 1
    foreign_player_position = 1
    
    #ball properties
    ball_position = Position(2, 2)
    ball_velocity = Position(1, 0)
    ball_timer = 0
    
    #Invert ball properties if we are a client
    if server != True :
        ball_position.x = 2 - (ball_position.x - 2)
        ball_position.y = 2 - (ball_position.y - 2)
        
        ball_velocity.x = -ball_velocity.x 
        ball_velocity.y = -ball_velocity.y
    
    while True :
        
        #Input
        last_local_player_position = local_player_position
        
        if local_player_position < 3 :
            local_player_position += button_b.is_pressed()
        if local_player_position > 0 :
            local_player_position -= button_a.is_pressed()
        
        #Share our new position with our opponent
        if last_local_player_position != local_player_position :
            radio.send('player=' + str(local_player_position))
        
        
        #network Syncing
        incoming = radio.receive()

        if incoming is not None:
            if incoming.find("player") != -1:
                foreign_player_position = 4 - int(incoming.split('=')[1])
              
        #Ball movement
        ball_timer += 1
        if ball_timer % 10 == 0 :
            #Colliding with player
            if ball_position.y == 3:
                if local_player_position.x == ball_position.x  :
                    ball_velocity.y = 1
                    ball_velocity.x = -1
                if local_player_position.x + 1 == ball_position.x :
                    ball_velocity.y = 1
                    ball_velocity.x = 1
            #colliding with enemy
            if ball_position.y == 1:
                if foreign_player_position.x == ball_position.x :
                    ball_velocity.y = -1
                    ball_velocity.x = 1
                if foreign_player_position.x - 1 == ball_position.x :
                    ball_velocity.y = -1
                    ball_velocity.x = -1
            #Colliding with walls 
            if ball_position.x + ball_velocity.x > 4 or ball_position.x + ball_velocity.x < 0:
                ball_velocity.x = -ball_velocity.x
            #Dying
            if ball_position.y == 4 or ball_position.y == 0 :
                sleep(100)#lost
            
            #Apply velocity
            ball_position.x += ball_velocity.x
            ball_position.y += ball_velocity.y
            
            
        
        
        #rendering
        #clear screen
        display.clear()
        
        #Render ball
        display.set_pixel(ball_position.x, ball_position.x, 9)
        
        #Render both players
        display.set_pixel(local_player_position, 4, 5)
        display.set_pixel(local_player_position + 1, 4, 5)
        display.set_pixel(foreign_player_position, 0, 5)
        display.set_pixel(foreign_player_position - 1, 0, 5)
        
        sleep(100)
