import pygame
from config import *
import math
import random
#matplotlib

class Spritesheet:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)# init player sprite and add it to all_sprites group

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0
        self.facing = "down"

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x  = self.x
        self.rect.y = self.y

    def draw(self):
        # self.game.screen.blit(self.image, self.rect)
        pass
    def update(self):
        self.moverment()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.collide_blocks("x")
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0
    
    def moverment(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_change = -PLAYER_SPEED # thay vi -=
            self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_change = PLAYER_SPEED
            self.facing = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_change = -PLAYER_SPEED
            self.facing = "up"
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_change = PLAYER_SPEED
            self.facing = "down"
        

    def collide_blocks(self, dir):
        if (dir == "x"):
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            
            if hits:
                for block in hits:
                    if self.x_change > 0 and self.rect.right < block.rect.right:
                        self.rect.right = block.rect.left
                    elif self.x_change < 0 and self.rect.left > block.rect.left:
                        self.rect.left = block.rect.right
                
        if (dir == "y"):
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                for block in hits:
                    if self.y_change > 0 and self.rect.bottom < block.rect.bottom:
                        self.rect.bottom = block.rect.top
                    elif self.y_change < 0 and self.rect.top > block.rect.top:
                        self.rect.top = block.rect.bottom

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(384, 576, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

