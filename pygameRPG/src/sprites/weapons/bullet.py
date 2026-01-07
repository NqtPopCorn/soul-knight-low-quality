import pygame
import math
import random
from config import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, heading, rad, dmg, rad_offset, speed, owner):
        # Local import to avoid circular dependency
        from sprites.characters import Enemy
        
        self._layer = BULLET_LAYER
        self.game = game
        self.dmg = dmg
        self.x = heading[0]
        self.y = heading[1]
        self.width = 10
        self.height = 10
        if isinstance(owner, Enemy):
            self.groups = self.game.all_sprites, self.game.enemies_bullets
        else:
            self.groups = self.game.all_sprites, self.game.bullets
            
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, YELLOW, (self.width//2, self.height//2), self.width//2)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.x_change = 0
        self.y_change = 0
        self.rad = rad + random.randint(-abs(rad_offset), abs(rad_offset)) * math.pi/180
        self.max_travel = WIN_WIDTH
        self.speed = speed
        
    def movement(self):
        self.rect.x += self.speed * math.cos(self.rad)
        self.rect.y += self.speed * math.sin(self.rad)
        self.max_travel -= self.speed
        if self.max_travel <= 0:
            self.kill()

    def update(self):
        self.movement()
        self.collide_blocks()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

    def collide_blocks(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits += pygame.sprite.spritecollide(self, self.game.entrances, False)
        if hits:
            self.kill()
