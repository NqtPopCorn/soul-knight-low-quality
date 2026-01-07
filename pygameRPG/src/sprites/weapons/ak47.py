import pygame
import math
from config import *
from sprites.weapons.gun import Gun

class AK47(Gun):
    def __init__(self, game, owner, delay = PLAYER_AK47_DELAY, bullet_dmg = PLAYER_AK47_DMG):
        # Local imports to avoid circular dependency
        from sprites.characters import Enemy, Boss
        
        self._layer = GUN_LAYER
        self.game = game
        self.owner = owner
        self.x = self.owner.rect.centerx
        self.y = self.owner.rect.centery
        self.width = 64
        self.height = 16
        self.groups = self.game.all_sprites, self.game.guns
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.ak47_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.shoot_animation = [self.game.ak47_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.ak47_spritesheet.get_sprite(64, 0, self.width, self.height),
                            self.game.ak47_spritesheet.get_sprite(128, 0, self.width, self.height),
                            self.game.ak47_spritesheet.get_sprite(192, 0, self.width, self.height),
                            self.game.ak47_spritesheet.get_sprite(256, 0, self.width, self.height)]
        self.timer = 0
        self.rad = self.owner.rad
        self.scope = AK47_SCOPE
        self.delay = delay
        self.bullet_dmg = bullet_dmg
        self.rad_offset = 4
        #pos against player to place gun when facing right
        self.place_right = (6, 4)
        self.headpos = (48, 4)
        self.manacost = 2
        self.speed = AK47_BULLET_SPEED

        # Adjust delay for enemies
        if isinstance(self.owner, Enemy) and isinstance(self.owner, Boss) == False:
            self.delay *= 4

    def shoot(self):
        from sprites.weapons.bullet import Bullet
        from sprites.characters import Player
        
        # test: đạn bắn 4 hướng
        # rads = [self.rad + math.pi, self.rad + math.pi/2, self.rad + -math.pi/2, self.rad]
        # for rad in rads:
        #     Bullet(self.game, self.find_heading(), rad, self.bullet_dmg, self.rad_offset, self.speed, self.owner)

        Bullet(self.game, self.find_heading(), self.rad, self.bullet_dmg, self.rad_offset, self.speed, self.owner)

        if isinstance(self.owner, Player):
            self.owner.mana -= self.manacost
