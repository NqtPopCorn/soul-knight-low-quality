import pygame
from config import *

class Entrance(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mapx, mapy):
        self.enable = True
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.entrances, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = mapx + x * TILE_SIZE
        self.y = mapy + y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(384, 576, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if(self.enable): 
            self.image = self.game.terrain_spritesheet.get_sprite(704, 160, self.width, self.height)
            self.game.blocks.add(self)
            self.game.entrances.remove(self)
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(95, 576, self.width, self.height)
            self.game.blocks.remove(self)
            self.game.entrances.add(self)
