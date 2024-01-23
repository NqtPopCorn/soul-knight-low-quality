import pygame
import time
import random
pygame.init()
display=pygame.display.set_mode((800,600))
pygame.display.set_caption('snake game')
blue=(0,0,255)
black=(0,0,0)
red=(255,0,0)
white=(255,255,255)
clock=pygame.time.Clock()
font_style=pygame.font.SysFont(None,20)
def our_snake(snake_block,snake_list):
    for x in snake_list:
        pygame.draw.rect(display,blue,[x[0],x[1],10,10])
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
    snake_List=[]
    Length_of_snake=1
    foodx=round(random.randrange(0,790/10.0))*10.0
    foody=round(random.randrange(0,590/10.0))*10.0
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -10
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = 10
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -10
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = 10
                    x1_change = 0
        if x1>=800 or x1<0 or y1>600 or y1<0:
             game_close=True
        x1+=x1_change
        y1+=y1_change
        display.fill(white)        
         #rectValue bộ 4 (x,y,width,height) ở đây thì có 1 hình chữ nhật kích thước 10x10 pixel đặt ở vị trí (200,150)
        pygame.draw.rect(display,red,[foodx,foody,10,10])
        snake_head=[]
        snake_head.append(x1)
        snake_head.append(y1)
        snake_List.append(snake_head)
        if len(snake_List)>Length_of_snake:
            del snake_List[0]
        for x in snake_List[:-1]:
            if x==snake_head:
                game_close=True
        our_snake(10,snake_List)
        pygame.display.update()
        if x1 == foodx and y1 == foody:
           foodx=round(random.randrange(0,790/10.0))*10.0
           foody=round(random.randrange(0,590/10.0))*10.0
           Length_of_snake+=1
        clock.tick(30)  #----vòng lặp chạy k quá 30 lần trong 1s
    pygame.quit()
   
    
gameLoop()
