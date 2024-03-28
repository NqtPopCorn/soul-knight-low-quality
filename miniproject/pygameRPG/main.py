import pygame
from sprites import *
from config import *
import sys

#                            _
#                         _ooOoo_
#                        o8888888o
#                        88" . "88
#                        (| -_- |)
#                        O\  =  /O
#                     ____/`---'\____
#                   .'  \\|     |//  `.
#                  /  \\|||  :  |||//  \
#                 /  _||||| -:- |||||_  \
#                 |   | \\\  -  /'| |   |
#                 | \_|  `\`---'//  |_/ |
#                 \  .-\__ `-. -'__/-.  /
#               ___`. .'  /--.--\  `. .'___
#            ."" '<  `.___\_<|>_/___.' _> \"".
#           | | :  `- \`. ;`. _/; .'/ /  .' ; |
#           \  \ `-.   \_\_`. _.'_/_/  -' _.' /
# ===========`-.`___`-.__\ \___  /__.-'_.'_.-'================
#                         `=--=-'


class Game: 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('miniproject/pygameRPG/Arial.ttf', 32)
        self.running = True

        self.character_spritesheet = Spritesheet('miniproject/pygameRPG/img/character.png')
        self.terrain_spritesheet = Spritesheet('miniproject/pygameRPG/img/terrain.png')
        self.enemy_spritesheet = Spritesheet('miniproject/pygameRPG/img/enemy.png')
        self.attack_spritesheet = Spritesheet('miniproject/pygameRPG/img/attack.png')
        self.glock_spritesheet = Spritesheet('miniproject/pygameRPG/img/Glock-SpriteSheet.png')
        self.intro_background = pygame.image.load('miniproject/pygameRPG/img/introbackground.png')
        self.gameover_background = pygame.image.load('miniproject/pygameRPG/img/gameover.png')

        self.t1 = pygame.time.get_ticks()

    def create_tilemap(self):
        self.maps = MapList(tilemaps, self)
        self.maps.draw()

    # new game start
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.bullets = pygame.sprite.LayeredUpdates()
        self.guns = pygame.sprite.LayeredUpdates()
        self.entrances = pygame.sprite.LayeredUpdates()
        self.create_tilemap()

    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + 32, self.player.rect.y)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - 32, self.player.rect.y)
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - 32)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + 32)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.player_weapon.can_shoot():
                    self.player.attacking = True
                    self.player_weapon.shoot()
                pass

    def update(self):
        self.all_sprites.update()
        
    def draw(self):
        #game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while(self.playing):
            self.events()
            self.update()
            self.draw()

    def gameover(self):
        text = self.font.render('Game Over', True, RED)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        restart_button = Button(10, 50, 120, 50, WHITE, BLACK,'Restart', 32)

        for sprite in self.all_sprites:
            sprite.kill()

        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if restart_button.isPressed(mouse_pos, mouse_pressed):
                self.new()
                self.main()

            self.screen.blit(self.gameover_background, (0,0))
            self.screen.blit(text, text_rect)
            self.screen.blit(restart_button.image, restart_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
        pass

    def intro_screen(self):
        intro = True
        title = self.font.render('Pygame RPG', True, BLACK)
        title_rect = title.get_rect(x=10,y=10)
        text = self.font.render('Let\'s Play', True, RED)
        text_rect = text.get_rect(center=(WIN_WIDTH/2, WIN_HEIGHT/2))

        play_button = Button(10, 50, 120, 50, WHITE, BLACK,'Play', 32)
        while(intro):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    intro = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            if play_button.isPressed(mouse_pos, mouse_pressed):
                intro = False

            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(text, text_rect)
            self.clock.tick(FPS)
            pygame.display.update()
        pass
def main():
    g = Game()
    g.intro_screen()
    g.new()
    while(g.running):
        g.main()
        g.gameover()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()