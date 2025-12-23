import pygame
import random
import os
x = pygame.init()

pygame.mixer.init()

# colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

gameWindow = pygame.display.set_mode((700,500))
pygame.display.set_caption("Snakes game - HighScore")
pygame.display.update()

#gamespecific variables
# exit_game = False
# game_over = False
# snake_x = 20
# snake_y = 25
# snake_size = 10
# snake_length = 1
# snake_list = []
# fps = 60
# velocity_x = 0
# velocity_y = 0
# init_velocity = 2
# food_x = random.randint(0, 350) # 700 is screen width
# food_y = random.randint(0, 250) # 500 is screen height
# food_size = 8
# score = 0 putted them in gameloop fn

# to defne FPS
clock = pygame.time.Clock()
# choosing font and its style
font = pygame.font.SysFont("couriernew", 20, bold=True)

# functions
    
def put_snake(gameWindow, colour, snake_list, snake_size):
# pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
    for x, y in snake_list:    
        pygame.draw.rect(gameWindow, colour, [x, y, snake_size, snake_size])

# def put_food(gameWindow, colour, food_x, food_y, food_size):
# # pygame.draw.circle(gameWindow, red, (food_x + food_size//2, food_y + food_size//2), food_size//2)
#     pygame.draw.circle(gameWindow, red, (food_x + food_size//2, food_y + food_size//2), food_size//2)

def show_score(text, colour, x, y):
    screen_text = font.render(text, True, colour)
    gameWindow.blit(screen_text, [x, y])

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def welcome_screen():
    exit_game = False
    pygame.mixer.music.load("Assets/nokia_startup.mp3")
    pygame.mixer.music.play()
    while not exit_game:
        gameWindow.fill(black)
        text_screen("Snakes", white, 315, 220)
        text_screen("Press return to play", white, 230, 250)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

        pygame.display.update()
        clock.tick(60) # in 60 fps
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_RETURN):

                gameloop()

#gameloop
def gameloop():

    exit_game = False
    game_over = False
    snake_x = 20
    snake_y = 25
    snake_size = 10
    snake_length = 1
    snake_list = []
    fps = 65
    velocity_x = 0
    velocity_y = 0
    init_velocity = 2
    food_x = random.randint(0, 350) # 700 is screen width
    food_y = random.randint(0, 250) # 500 is screen height
    food_size = 8
    score = 0
    with open("highscores.txt", "r") as f:
        highscore = f.read() # it reads as a string btw

    while not exit_game:
        if game_over:
            with open("highscores.txt", "w") as f:
                f.write(str(highscore)) # it writes the new highscore
            gameWindow.fill(black)
            # text = font.render(f"Game over!Your score was{score}Press Enter key to continue", True, red)
            # gameWindow.blit(text, text_rect)   the \n doesnt work on font.render🥲
            game_over_text = font.render("Game over!", True, red)
            score_text = font.render(f"Your score was {score}", True, red)
            continue_text = font.render("Press Enter key to continue", True, red)
            # so doing each line
            gameWindow.blit(game_over_text, (200, 200))
            gameWindow.blit(score_text, (200, 250))
            gameWindow.blit(continue_text, (200, 300))         
            text_rect = game_over_text.get_rect(center=(350, 250))
            text_rect = score_text.get_rect(center=(350, 250))
            text_rect = continue_text.get_rect(center=(350, 250))


            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    exit_game = True
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_RETURN):
                        pygame.mixer.music.load("Assets/ringtone-nokia-destiny.mp3")
                        pygame.mixer.music.play()
                        gameloop()
        else:
            for event in pygame.event.get():
                # print(event)
                if(event.type == pygame.QUIT):
                    exit_game = True

                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.K_RIGHT):
                        velocity_x = init_velocity
                        velocity_y = 0
                    if(event.key == pygame.K_LEFT):
                        velocity_x = - init_velocity
                        velocity_y = 0
                    if(event.key == pygame.K_UP):
                        velocity_y = - init_velocity
                        velocity_x = 0
                    if(event.key == pygame.K_DOWN):
                        velocity_y = init_velocity
                        velocity_x = 0
            
            snake_x+=velocity_x
            snake_y+=velocity_y

            if(abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6):
                score+=10
                snake_length+=5
                print(f"Score: {score}")
                # replotting food location once hit
                food_x = random.randint(0, 350) 
                food_y = random.randint(0, 250)
                if(score>int(highscore)):
                    highscore = score

            gameWindow.fill(black)
            show_score("Score: " + str(score) + "   Highscore: " + str(highscore), white, 10, 10) # str() fn to convert to string as that argument only accepts strings
            
            pygame.draw.circle(gameWindow, red, (food_x + food_size//2, food_y + food_size//2), food_size//2)
            if(snake_x < 0 or snake_y < 0 or snake_x > 700 or snake_y > 500):
                game_over = True
                pygame.mixer.music.load("Assets/dead-nokia.mp3")
                pygame.mixer.music.play()
            put_snake(gameWindow, white, snake_list, snake_size)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if(len(snake_list)>snake_length):
                del snake_list[0]

            # if snake bites itself
            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("Assets/dead-nokia.mp3")
                pygame.mixer.music.play()


        pygame.display.update()
        clock.tick(fps)


    pygame.quit()
    quit()

welcome_screen()
# gameloop()