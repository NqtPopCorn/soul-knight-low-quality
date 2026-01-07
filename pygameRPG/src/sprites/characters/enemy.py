import pygame
import math
import random
from config import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mapx, mapy, map, weapon_ratio_dict = ENEMY_WEAPON_RATIO):
        self.game = game
        self._layer = ENERMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = mapx + x * TILE_SIZE
        self.y = mapy + y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "right"
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(30, 60)

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x  = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(67, 66, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(67, 98, self.width, self.height)]
    
        self.HP = 3
        self.room = map
        self.rad = 0

        # Import locally to avoid circular dependency
        from sprites.weapons import Glock, AK47, Sniper
        
        rand_weapon = random.choices(list(weapon_ratio_dict.keys()), weights=weapon_ratio_dict.values(), k=1)[0]
        if rand_weapon == "glock":
            self.weapon = Glock(self.game, self, PLAYER_GLOCK_DELAY)
        elif rand_weapon == "ak47":
            self.weapon = AK47(self.game, self, PLAYER_AK47_DELAY)
        else:
            self.weapon = Sniper(self.game, self, PLAYER_SNIPER_DELAY)
        
        self.attacking = False
        self.rand = random.randint(1, 4)

    def update(self):
        self.movement()
        self.collide_bullet()
        self.animate()
        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0

    def animate(self):
        if self.facing == "left":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
        if self.facing == "right":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.animation_loop >= 3:
            self.animation_loop = 1
        
    def collide_blocks(self, dir):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        hits += pygame.sprite.spritecollide(self, self.game.entrances, False)
        if hits:
            if (dir == "x"):
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                if self.x_change < 0:
                    self.rect.left = hits[0].rect.right
            if (dir == "y"):
                if self.y_change > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.y_change < 0:
                    self.rect.top = hits[0].rect.bottom

    def collide_bullet(self):
        hits = pygame.sprite.spritecollide(self, self.game.bullets, False)
        if hits:
            self.HP -= hits[0].dmg
            hits[0].kill()
            if self.HP <= 0:
                self.kill()
                # self.game.player.score += 1
                # if self.game.player.mana <= self.game.player.max_mana - 10:
                #     self.game.player.mana += 10
                # else :
                #     self.game.player.mana = self.game.player.max_mana
                self.game.player.earnManaAndPoints(10, 1)

    def movement(self):
        if self.y_change != 0 or self.x_change != 0:
            self.rad = math.atan2(self.y_change, self.x_change)
        player = self.game.player
        distance = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + (player.rect.centery - self.rect.centery)**2)
        if distance < self.weapon.scope + 96 and self.room.open == False:
            self.taunted_movement(distance)
        else:
            self.normal_movement()
    
    def normal_movement(self):
        if self.rand == 1:
            self.y_change -= ENEMY_SPEED
        if self.rand == 2:
            self.y_change += ENEMY_SPEED
        if self.rand == 3:
            self.x_change -= ENEMY_SPEED
            self.facing = "left"
            self.rad = math.pi
        if self.rand == 4:
            self.x_change += ENEMY_SPEED
            self.facing = "right"
            self.rad = 0

        self.movement_loop -= 1
        if self.movement_loop <= -self.max_travel:
            self.movement_loop = 0
            self.rand = random.randint(1, 4)
            self.max_travel = random.randint(30, 60)
        pass

    def taunted_movement(self, distance):
        player = self.game.player
        dy = player.rect.centery - self.rect.centery
        dx = player.rect.centerx - self.rect.centerx
        self.rad = math.atan2(dy, dx)
        if distance > self.weapon.scope:
            self.x_change += ENEMY_SPEED * math.cos(self.rad)
            self.y_change += ENEMY_SPEED * math.sin(self.rad)
        elif self.weapon.can_shoot():
            self.weapon.shoot()

    #TODO: cu cach 1 khoang thoi gian, boss lai lam mot hanh dong ngau nhien
        
    def kill(self):
        self.weapon.kill()
        pygame.sprite.Sprite.kill(self)

    def take_dmg(self, dmg):
        self.HP -= dmg
        if self.HP <= 0:
            self.kill()
            self.game.player.earnManaAndPoints(10, 1)
