import pygame
from config import *
from sprites.weapons.gun import Gun

class Sniper(Gun):
    def __init__(self, game, owner, delay = PLAYER_SNIPER_DELAY, bullet_dmg = PLAYER_SNIPER_DMG):
        # Local imports to avoid circular dependency
        from sprites.characters import Enemy, Boss
        
        self._layer = GUN_LAYER
        self.game = game
        self.owner = owner
        self.x = self.owner.rect.centerx
        self.y = self.owner.rect.centery
        self.width = 80
        self.height = 32
        self.groups = self.game.all_sprites, self.game.guns
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.sniper_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.shoot_animation = [self.game.sniper_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.sniper_spritesheet.get_sprite(80, 0, self.width, self.height),
                            self.game.sniper_spritesheet.get_sprite(160, 0, self.width, self.height),
                            self.game.sniper_spritesheet.get_sprite(240, 0, self.width, self.height),
                            self.game.sniper_spritesheet.get_sprite(320, 0, self.width, self.height)]
        
        self.timer = 0
        self.rad = self.owner.rad
        self.scope = SNIPER_SCOPE
        self.delay = delay
        self.bullet_dmg = bullet_dmg
        self.rad_offset = 0
        #pos against player to place gun when facing right
        self.place_right = (8, 4)
        self.headpos = (48, 6)
        self.manacost = 5
        self.speed = SNIPER_BULLET_SPEED
        if isinstance(self.owner, Enemy) and isinstance(self.owner, Boss) == False:
            self.delay *= 4
