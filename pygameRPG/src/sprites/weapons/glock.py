import pygame
import random
from config import *
from sprites.weapons.gun import Gun

class Glock(Gun):
    def __init__(self, game, owner, delay = PLAYER_GLOCK_DELAY, bullet_dmg = PLAYER_GLOCK_DMG):
        # Local imports to avoid circular dependency
        from sprites.characters import Enemy, Boss
        
        self._layer = GUN_LAYER
        self.game = game
        self.owner = owner
        self.x = self.owner.rect.centerx
        self.y = self.owner.rect.centery
        self.width = 48
        self.height = 32
        self.groups = self.game.all_sprites, self.game.guns
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.glock_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.shoot_animation = [self.game.glock_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(48, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(96, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(144, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(192, 0, self.width, self.height)]
        self.timer = 0
        self.rad = self.owner.rad
        self.scope = GLOCK_SCOPE
        self.delay = delay
        self.bullet_dmg = bullet_dmg
        self.rad_offset = 3

        #pos against player to place gun when facing right
        self.place_right = (8, 6)
        self.headpos = (40, 8)
        self.manacost = 0
        self.speed = GLOCK_BULLET_SPEED
        if isinstance(self.owner, Enemy) and isinstance(self.owner, Boss) == False:
            self.delay *= 4

    def shoot(self):
        from sprites.weapons.bullet import Bullet
        from sprites.characters import Player
        
        rand_num = random.randint(1, 8)
        for i in range(rand_num):
            Bullet(self.game, self.find_heading(), self.rad, self.bullet_dmg, self.rad_offset, self.speed, self.owner)
        if isinstance(self.owner, Player):
            self.owner.mana -= self.manacost
