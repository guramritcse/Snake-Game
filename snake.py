from multiprocessing.connection import wait
import pygame 
import random  
import argparse

######################## Program Starts ########################
pygame.init()  

######################## Color Used ########################
white = (255, 255, 255) 
yellow = (255, 255, 102) 
black = (0, 0, 0)  
red = (213, 50, 80)
green = (0, 200, 0)
blue = (55, 155, 215)
orange= (255, 69, 0)  
magenta=(255, 0, 255)


######################## Screen Dimensions ########################
screen_width = 500 
screen_height = 500

######################## Game Constants and Fonts ########################
block = 10
snake_speed = 7
food_radius = 5
message1_font = pygame.font.SysFont('Copperplate', 20)
message2_font = pygame.font.SysFont('Marker Felt', 20)
message3_font = pygame.font.SysFont('Marker Felt', 30)
message4_font = pygame.font.SysFont('Bradley Hand', 25)
message5_font = pygame.font.SysFont('Lucida Calligraphy', 24, italic=True) 
message6_font = pygame.font.SysFont('Lucida Calligraphy', 40, italic=True)  

  
######################## Score Displayer ########################
def score_display(score): 
    todisplay = message6_font.render(f"Score: {score}", True, magenta) 
    screen.blit(todisplay, [0, 0])
    pygame.draw.line(screen,green, (0, 30), (screen_width, 30))
    pygame.display.update()    

######################## Snake Displayer ########################
def snake_display(block, snake_pos): 
    pygame.draw.rect(screen, red, [snake_pos[len(snake_pos)-1][0], snake_pos[len(snake_pos)-1][1], block, block])   
    for i in range(0,len(snake_pos)-1):
        pygame.draw.rect(screen, orange, [snake_pos[i][0], snake_pos[i][1], block, block])   

######################## Food Displayer ########################
def food_display(block, food_pos):     
    pygame.draw.rect(screen, yellow, [food_pos[0], food_pos[1], block, block])   

######################## Start Screen Displayer ########################
def start_display():
    screen.fill(green) 
    todisplay = message3_font.render("Welcome to Snake Game", True, orange)
    screen.blit(todisplay, [screen_width/4-10, 30])
    todisplay = message3_font.render("Enter Your Name", True, magenta)
    screen.blit(todisplay, [screen_width/4+25, screen_height/4+20])
    todisplay = message5_font.render("(Maximum 12 characters)", True, red) 
    screen.blit(todisplay, [screen_width/4+28, screen_height/4+60])
    todisplay = message1_font.render("Designed by Guramrit Singh", True, yellow)
    screen.blit(todisplay, [screen_width/4-15, 460])
    pygame.display.update() 
    notentered = True
    user_name=''
    input_text = pygame.Rect(screen_width/4-10, screen_height/4+90, 210, 32)
    while notentered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(user_name)>0:
                        notentered = False
                else:
                    if len(user_name)<12:
                        user_name += event.unicode
            if not notentered:
                break

            pygame.draw.rect(screen, blue, input_text)
            text_surface = message4_font.render(user_name, True, white)
            screen.blit(text_surface, [input_text.x+5, input_text.y])
            input_text.w = 290
            pygame.display.flip()

    return user_name

######################## End Screen Displayer ########################
def end_display(user_name, score): 
    message = message2_font.render("          Game Over                  Press A-Play Again or Q-Quit", True, red) 
    screen.blit(message, [0, 60])   
    message = message2_font.render(f"You scored: {score}", True, orange) 
    screen.blit(message, [screen_width/3+30, 100]) 
    message = message6_font.render(f"Highest Score(s)", True, magenta) 
    screen.blit(message, [screen_width/3-20, 150])  
    file=open("highscores.txt", 'r')
    scores=[]
    users=[]
    total=-1
    for line in file.readlines():
        if not total ==-1:
            score_here = line.split(",")
            scores.append(score_here[0])
            users.append(score_here[1][:-1])
        total=total+1
    if total>5:
        total=5
    file.close()
    if total<5:
        file=open("highscores.txt", 'w')
        index_add=0
        for i in range(total):
            if score<=int(scores[i]):
                index_add=index_add+1
                continue
            break
        file.write('This file stores 5 highest scores\n')
        for i in range(index_add):
            file.write(f'{scores[i]},{users[i]}\n')
        file.write(f'{score},{user_name}\n')
        for i in range(index_add,total):
            file.write(f'{scores[i]},{users[i]}\n')
        file.close()
    else:
        index_add=0
        for i in range(total):
            if score<=int(scores[i]):
                index_add=index_add+1
                continue
            break
        if(index_add<5):
            file=open("highscores.txt", 'w')
            file.write('This file stores 5 highest scores\n')
            for i in range(index_add):
                file.write(f'{scores[i]},{users[i]}\n')
            file.write(f'{score},{user_name}\n')
            for i in range(index_add,total-1):
                file.write(f'{scores[i]},{users[i]}\n')
            file.close()

    file=open("highscores.txt", 'r')
    scores=[]
    users=[]
    total=-1
    for line in file.readlines():
        if not total ==-1:
            score_here = line.split(",")
            scores.append(score_here[0])
            users.append(score_here[1][:-1])
        total=total+1
    if total>5:
        total=5
    for i in range(total):
        message = message2_font.render(f"Position {i+1}: {users[i]}", True, blue) 
        screen.blit(message, [screen_width/5-50, 210+30*i])
        message = message2_font.render(f"Score: {scores[i]}", True, blue) 
        screen.blit(message, [2*screen_width/3+50, 210+30*i]) 
        
    
    
    
######################## Game Loop ########################
def gameLoop(user_name):

    ###################### First entry ######################
    game_over = False 
    game_close = False  
    headX = screen_width/2 
    headY = screen_height/2  
    headX_change = 0 
    headY_change = 0  
    snake_pos = [[headX, headY]] 
    snake_length = 1  
    foodx = round(random.randrange(0, screen_width - block) / 10.0) * 10.0 
    foody = round(random.randrange(30, screen_height - block) / 10.0) * 10.0
    food_display(block, [foodx, foody])
    score_display(snake_length - 1)
    pygame.display.update()


    ###################### Update Screen ######################
    while not game_over: 
        if game_close:
            screen.fill(yellow) 
            end_display(user_name, snake_length-1)
            pygame.display.update() 
            while game_close:  
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    elif event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_q: 
                            game_over = True 
                            pygame.quit() 
                            quit()  
                        game_close = False 
                        if event.key == pygame.K_a: 
                            gameLoop(user_name)
                            pygame.quit() 
                            quit()    
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                game_over = True
                pygame.quit() 
                quit()
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    if headX_change == block and snake_length>1:
                        break
                    headX_change = -block 
                    headY_change = 0 
                elif event.key == pygame.K_RIGHT:
                    if headX_change == -block and snake_length>1:
                        break 
                    headX_change = block 
                    headY_change = 0 
                elif event.key == pygame.K_UP: 
                    if headY_change == block and snake_length>1:
                        break 
                    headY_change = -block 
                    headX_change = 0 
                elif event.key == pygame.K_DOWN:
                    if headY_change == -block and snake_length>1:
                        break  
                    headY_change = block 
                    headX_change = 0   
        headX += headX_change 
        headY += headY_change 
        if headX >= screen_width or headX < 0 or headY >= screen_height or headY < 30: 
            game_close = True
            continue
        screen.fill(black) 
        snake_curr_head = [] 
        snake_curr_head.append(headX) 
        snake_curr_head.append(headY) 
        snake_pos.append(snake_curr_head) 
        if len(snake_pos) > snake_length: 
            snake_pos.pop(0)  
            for pos in snake_pos[:-1]: 
                if pos == snake_curr_head: 
                    game_close = True
                    break    
            if headX == foodx and headY == foody:
                foodx = round(random.randrange(0, screen_width - block) / 10.0) * 10.0 
                foody = round(random.randrange(30, screen_height - block) / 10.0) * 10.0
                snake_length += 1
            snake_display(block, snake_pos)
            food_display(block, [foodx, foody])
            score_display(snake_length - 1)
            pygame.display.update()
            clock.tick(snake_speed)
                            

######################## Game Initializer ########################
parser = argparse.ArgumentParser()
parser.add_argument("--theme",type=str,required=True)
args = parser.parse_args()

screen = pygame.display.set_mode((screen_width, screen_height)) 
pygame.display.set_caption('Snake Game by Guramrit Singh')
pygame.mixer.init()
pygame.mixer.music.load(args.theme)
pygame.mixer.music.play(-1)
clock = pygame.time.Clock() 
user_name=start_display() 
snake_display(block, [[screen_width/2, screen_height/2]])
pygame.display.update()

######################## Game Begins ########################
gameLoop(user_name)

######################## Game Ends ########################
pygame.quit() 
quit()   

