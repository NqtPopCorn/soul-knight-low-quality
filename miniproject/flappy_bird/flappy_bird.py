import pygame, sys, random

def draw_floor():
    global floor_x_pos
    screen.blit(floor, (floor_x_pos, FLOOR_Y))
    screen.blit(floor, (floor_x_pos + 432,  FLOOR_Y))
    floor_x_pos -= BIRD_SPEED
    if floor_x_pos <= -432:
        floor_x_pos = 0
def create_pipe_rect(pipe_heights, pipe_surface):
    pipe_height = random.choice(pipe_heights)
    STARTX = 500 
    FREE_SPACE = 200
    top_rect = pipe_surface.get_rect(midbottom = (STARTX, pipe_height)) 
    bot_rect = pipe_surface.get_rect(midtop = (STARTX, pipe_height + FREE_SPACE))
    return top_rect, bot_rect
def move_pipes_rect(pipe_rect_list):
    for pipe_rect in pipe_rect_list:
        pipe_rect.centerx -= BIRD_SPEED
    return pipe_rect_list
def draw_pipe(pipe_rect_list):
    for pipe_rect in pipe_rect_list:
        if pipe_rect.top > 0:
            screen.blit(pipe_surface, pipe_rect)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) 
            screen.blit(flip_pipe, pipe_rect)
def check_collision(pipe_rect_list, bird_rect):
    for pipe_rect in pipe_rect_list:
        if pipe_rect.colliderect(bird_rect):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >=  FLOOR_Y:
        return False
    return True
def bird_animation():
    global bird_index, bird_rect
    if bird_index < 2:
        bird_index += 1
    else:
        bird_index = 0
    new_bird = bird_list[bird_index]
    new_bird = pygame.transform.scale2x(new_bird)
    new_bird_rect = new_bird.get_rect(center = bird_rect.center)
    return new_bird, new_bird_rect
def score_display(game_status):
    if(game_status == 'main_game'):
        score_surface = GAME_FONT.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    elif(game_status == 'game_over'):
        score_surface = GAME_FONT.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
        high_score_surface = GAME_FONT.render(f'High score: {int(highest_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (216, 630))
        screen.blit(high_score_surface, high_score_rect)
def draw_bg():
    global bg_x_pos
    screen.blit(bg, (bg_x_pos,0))
    screen.blit(bg, (bg_x_pos + 432, 0))
    bg_x_pos -= 0.2
    if bg_x_pos <= -432:
        bg_x_pos = 0
def update_score():
    global score, pipe_rect_list, highest_score, upcoming_pipe
    if len(pipe_rect_list) > upcoming_pipe and pipe_rect_list[upcoming_pipe].right <= bird_rect.left:
        score += 1
        score_sound.play()
        upcoming_pipe += 2
    if score > highest_score:
        highest_score = score 

pygame.init()
pygame.mixer.pre_init()
FPS = 120
BIRD_SPEED = 3
GRAVITY = 0.25
GAME_FONT = pygame.font.Font('C:/Học/python/doan/miniproject/flappy_bird/04B_19.TTF', 40)
FLOOR_Y = 650
BG_WIDTH = 432
BG_HEIGHT = 768

screen = pygame.display.set_mode((BG_WIDTH, BG_HEIGHT))
clock  = pygame.time.Clock()
bird_movement = 0
game_active = True
score = 0
highest_score = 0
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(pygame.image.load('miniproject/flappy_bird/assets/yellowbird-upflap.png'))
# background
bg = pygame.image.load('miniproject/flappy_bird/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
bg_rect = bg.get_rect(topleft=(0,0))
bg_x_pos = 0

# chen floor
floor = pygame.image.load('miniproject/flappy_bird/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# chim
bird_midflag = pygame.image.load('miniproject/flappy_bird/assets/yellowbird-midflap.png').convert_alpha()
bird_upflag = pygame.image.load('miniproject/flappy_bird/assets/yellowbird-upflap.png').convert_alpha()
bird_downflag = pygame.image.load('miniproject/flappy_bird/assets/yellowbird-downflap.png').convert_alpha()
bird_list = [bird_downflag, bird_midflag, bird_upflag]
bird_index = 0
bird = bird_list[bird_index]
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 300))
#tao timer cho bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200) 

# ong
pipe_surface = pygame.image.load('miniproject/flappy_bird/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_rect_list = []
pipe_heights = [100, 150, 200, 250, 300]
upcoming_pipe = 0
# tao timer ong
spawm_pipe = pygame.USEREVENT
pygame.time.set_timer(spawm_pipe, 1200)

# tao man hinh ket thuc
game_over_surface = pygame.image.load('miniproject/flappy_bird/assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (BG_WIDTH/2, BG_HEIGHT/2))

# chen am thanh
flap_sound = pygame.mixer.Sound('miniproject/flappy_bird/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('miniproject/flappy_bird/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('miniproject/flappy_bird/sound/sfx_point.wav')
hit_sound.set_volume(0.1)
score_sound.set_volume(0.1)
score_countdown = 100

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == True:
                bird_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_rect_list.clear()
                bird_rect.center = (100, 300)
                bird_movement = 0
                score = 0
                upcoming_pipe = 0
        if event.type == spawm_pipe:
            pipe_rect_list.extend(create_pipe_rect(pipe_heights, pipe_surface))
        if event.type == bird_flap:
            bird, bird_rect = bird_animation()

    draw_bg()     
    if game_active:
        game_active = check_collision(pipe_rect_list, bird_rect)
        if game_active == False: hit_sound.play()
        else:# chim
            bird_movement += GRAVITY
            bird_rect.centery += bird_movement
            rotated_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
            screen.blit(rotated_bird, bird_rect)
            # ong
            pipe_rect_list = move_pipes_rect(pipe_rect_list)
            draw_pipe(pipe_rect_list)    
            update_score()
            score_display("main_game")
    else: 
        screen.blit(game_over_surface, game_over_rect)
        score_display("game_over")
    # san
    draw_floor()

    # clean up
    if len(pipe_rect_list) > 0 and pipe_rect_list[0].right <= 0:
        pipe_rect_list.pop(0)
        pipe_rect_list.pop(0)
        upcoming_pipe -= 2
    pygame.display.update()
    clock.tick(FPS)   
       