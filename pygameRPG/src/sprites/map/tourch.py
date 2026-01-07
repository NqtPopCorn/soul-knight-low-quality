import pygame
from config import *
from utils import get_asset_path

class Torch(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mapx, mapy):
        self.game = game
        self._layer = TORCH_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = mapx + x * TILE_SIZE
        self.y = mapy + y * TILE_SIZE
        self.width = 32
        self.height = 32

        self.animations = [pygame.image.load(get_asset_path("img/torch_1.png")).convert(),
                           pygame.image.load(get_asset_path("img/torch_2.png")).convert(),
                           pygame.image.load(get_asset_path("img/torch_3.png")).convert(),
                           pygame.image.load(get_asset_path("img/torch_4.png")).convert()
                            ]
        for i in range(4):
            image = pygame.transform.scale(self.animations[i], (64,64))
            image.set_colorkey(BLACK)
            self.animations[i] = image
        self.animation_loop = 0

        self.image = self.animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x - 16
        self.rect.y = self.y - 32
        
        self.timer = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.timer > 100:
            if self.animation_loop > 3:
                self.animation_loop = 0
            self.image = self.animations[self.animation_loop]
            self.animation_loop += 1
            self.timer = pygame.time.get_ticks()
