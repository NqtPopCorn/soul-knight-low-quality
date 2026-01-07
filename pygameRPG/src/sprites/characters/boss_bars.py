import pygame
from config import *

class BossHPBar(pygame.sprite.Sprite):
    def __init__(self, game, owner):
        self._layer = BAR_LAYER
        self.groups = game.bars
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.bar_size = (240, 20)
        self.border = 2
        self.owner = owner

        self.image = pygame.Surface((self.bar_size[0]+self.border*2, self.bar_size[1]+self.border*2))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIN_WIDTH//2 
        self.rect.y = 60
        
        self.health_bg = pygame.Surface(self.bar_size)
        self.health_bg.fill((71, 62, 62))
        self.health_bar = pygame.Surface(self.bar_size)
        self.health_bar.fill(RED)
        self.health_bar_rect = self.health_bar.get_rect()
        self.health_bar_rect.topleft = (0,0)
        self.health_bg_rect = self.health_bg.get_rect()
        self.health_bg_rect.topleft = (self.border, self.border)

        self.health_bg.blit(self.health_bar, self.health_bar_rect)

        self.image.fill(BLACK)
        self.image.blit(self.health_bg, self.health_bg_rect)
        
    def update(self):
        self.draw_HP()
        pass

    def draw_HP(self):
        self.health_bar_rect.right = self.bar_size[0] * self.owner.HP / self.owner.max_hp

        self.health_bg.fill((43, 40, 40))
        self.health_bg.blit(self.health_bar, self.health_bar_rect)
        self.image.blit(self.health_bg, self.health_bg_rect)
        if self.owner.HP <= 0:
            self.kill()
