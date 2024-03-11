import pygame, sys, random
def draw_floor():
    screen.blit(floor, (floor_x_pos,650))
    screen.blit(floor, (floor_x_pos + 432, 650))
def create_pipe_rect():
    pipe_height = random.choice([200, 300, 400])
    bot_rect = pipe_surface.get_rect(midtop = (500, pipe_height))
    top_rect = pipe_surface.get_rect(midtop = (500, pipe_height -750)) 
    return top_rect, bot_rect
def move_pipes_rect(pipe_rect_list):
    for pipe in pipe_rect_list:
        pipe.centerx -= BIRD_SPEED
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
        if bird_rect.colliderect(pipe_rect):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 650:
        return False
    return True
def bird_animation(bird_index):
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_status):
    if(game_status == 'main_game'):
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    elif(game_status == 'game_over'):
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High score: {int(highest_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (216, 630))
        screen.blit(high_score_surface, high_score_rect)
    
pygame.init()
pygame.mixer.pre_init()
FPS = 120
BIRD_SPEED = 3
screen = pygame.display.set_mode((432, 768))
clock  = pygame.time.Clock()
gravity = 0.25
bird_movement = 0
game_active = True
game_font = pygame.font.Font('miniproject/04B_19.TTF', 40)
score = 0
highest_score = 0
count_hit_sound = 0
# chen background
bg = pygame.image.load('miniproject/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
#chen floor
floor = pygame.image.load('miniproject/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#tao chim
bird_midflag = pygame.image.load('miniproject/assets/yellowbird-midflap.png').convert_alpha()
bird_upflag = pygame.image.load('miniproject/assets/yellowbird-upflap.png').convert_alpha()
bird_downflag = pygame.image.load('miniproject/assets/yellowbird-downflap.png').convert_alpha()
bird_list = [bird_downflag, bird_midflag, bird_upflag]
bird_index = 0
bird = bird_list[bird_index]
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100, 300))
#tao timer cho bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)
# tao ong
pipe_surface = pygame.image.load('miniproject/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_rect_list = []
pipe_height = [200, 300, 400]
# tao timer ong
spawm_pipe = pygame.USEREVENT
pygame.time.set_timer(spawm_pipe, 1200)
#tao man hinh ket thuc
game_over_surface = pygame.image.load('miniproject/assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (216, 384))

# chen am thanh
flap_sound = pygame.mixer.Sound('miniproject/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('miniproject/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('miniproject/sound/sfx_point.wav')
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
        if event.type == spawm_pipe:
            pipe_rect_list.extend(create_pipe_rect())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect= bird_animation(bird_index)
            bird = pygame.transform.scale2x(bird)
            
    screen.blit(bg, (0,0))
    game_active = check_collision(pipe_rect_list, bird_rect)
    if game_active:
        # chim
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
        screen.blit(rotated_bird, bird_rect)
        # ong
        pipe_rect_list = move_pipes_rect(pipe_rect_list)
        draw_pipe(pipe_rect_list)    
        score += 0.01
        score_countdown -= 1
        if(score_countdown == 0): 
            score_countdown = 100
            score_sound.play()   
        if score > highest_score:
            highest_score = score
        score_display("main_game")
        count_hit_sound = 0
    else: 
        if(count_hit_sound == 0):
            hit_sound.play()
            count_hit_sound = 1
        screen.blit(game_over_surface, game_over_rect)
        score_display("game_over")
    # san
    floor_x_pos -= BIRD_SPEED
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    
    clock.tick(FPS)
