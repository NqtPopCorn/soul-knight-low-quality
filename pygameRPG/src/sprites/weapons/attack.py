import pygame
import math
from config import *

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.game = game
        self.x = x
        self.y = y
        self.width = WEAPON_SIZE
        self.height = WEAPON_SIZE
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.damage = PLAYER_NORMAL_ATTACK_DMG

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        # kill enemy if hit -> 1 hit kill
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True) 

        # hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        # for hit in hits:
        #     hit.take_dmg(self.damage)

    def animate(self):
        direction = self.game.player.facing

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]
        
        if direction == "up":
            self.image = up_animations[math.floor(self.animation_loop)]
        if direction == "down":
            self.image = down_animations[math.floor(self.animation_loop)]
        if direction == "left":
            self.image = left_animations[math.floor(self.animation_loop)]
        if direction == "right":
            self.image = right_animations[math.floor(self.animation_loop)]

        self.animation_loop += 0.5
        # Remove the attack sprite after the animation is done
        if self.animation_loop >= 5:
            self.kill()
    #end
 