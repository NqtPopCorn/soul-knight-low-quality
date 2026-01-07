import pygame
from config import *
from .enemy import Enemy

class Boss(Enemy):
    def __init__(self, game, x, y, mapx, mapy, map):
        self.game = game
        Enemy.__init__(self, self.game, x, y, mapx, mapy, map, {"ak47": 1})
        
        self.width = BOSS_SIZE
        self.height = BOSS_SIZE
        self.image = self.game.boss_spritesheet.get_sprite(0, 2, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.boss_spritesheet.get_sprite(12,83, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(93,75, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(190, 75, self.width, self.height)]

        self.left_animations = [self.game.boss_spritesheet.get_sprite(18, 160, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(113, 160, self.width, self.height),
                            self.game.boss_spritesheet.get_sprite(203, 160, self.width, self.height)]
        self.max_hp = 100
        self.HP = self.max_hp
