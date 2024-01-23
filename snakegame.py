import pygame
import time
import random

pygame.init()
screen = (500,400)
display=pygame.display.set_mode(screen)
pygame.display.set_caption('snake game')

blue=(0,0,255)
black=(0,0,0)
red=(255,0,0)
white=(255,255,255)
clock=pygame.time.Clock()
font_style=pygame.font.SysFont(None,20)


def draw_snake(snake_block,snake_list):
    for x in snake_list:
        pygame.draw.rect(display,blue,[x[0],x[1],snake_block, snake_block])
def message(msg,color):
    mesg=font_style.render(msg, True, color)
    display.blit(mesg, [10,300])
def gameLoop():
    game_over=False
    game_close=False
    x1=400
    y1=300
    x1_change=0 
    y1_change=0
    snake_List=[(x1,y1)]
    Length_of_snake=1
    foodx=round(random.randrange(0,int(screen[0]/10.0)))*10.0
    foody=round(random.randrange(0,int(screen[1]/10.0)))*10.0
    while not game_over:
        while game_close==True:
            display.fill(white)
            message("you lost! press q to quit or a to play again", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        game_over=True
                        game_close=False
                    if event.key==pygame.K_a:
                        gameLoop()
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close=False

        #draw
        display.fill(white)
        #draw food
        pygame.draw.rect(display,red,[foodx,foody,10,10])
        #draw snake
        draw_snake(10,snake_List)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x1_change != 10: x1_change = -10
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    if x1_change != -10: x1_change = 10
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    if y1_change != 10: y1_change = -10
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    if y1_change != -10: y1_change = 10
                    x1_change = 0
        
        if x1+x1_change>screen[0] or x1+x1_change<0 or y1+y1_change>screen[1] or y1+y1_change<0:
            game_close=True

        
        if x1_change == 0 and y1_change == 0: continue  #neu ng dung chua bat dau tro choi thi bo qua khoi lenh duoi

        new_head=[x1+x1_change,y1+y1_change]
        if new_head not in snake_List: 
            snake_List.append(new_head)
            x1+=x1_change
            y1+=y1_change
        else: game_close= True

        if len(snake_List)>Length_of_snake:
            del snake_List[0]

        if x1 == foodx and y1 == foody:
            foodx=round(random.randrange(0,int(screen[0]/10.0)))*10.0
            foody=round(random.randrange(0,int(screen[1]/10.0)))*10.0
            Length_of_snake+=1

        clock.tick(20) # thoi gian gioi han cho vong
    pygame.quit()
   
    
gameLoop()