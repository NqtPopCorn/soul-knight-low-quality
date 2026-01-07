import pygame
import math
from config import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, mapx, mapy):
        self.game = game
        # game.player = self 
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x =  mapx + x * TILE_SIZE
        self.y = mapy + y * TILE_SIZE
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0
        self.facing = "right"
        self.animation_loop = 1
        self.attack_loop = 0
        self.attacking = False

        self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x  = self.x
        self.rect.y = self.y

        self.right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(67, 66, self.width, self.height)]

        self.left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(67, 98, self.width, self.height)]
        
        self.rad = 0
        self.score = 0

        self.max_hp = 5
        self.max_armour = 4
        self.max_mana = 200

        self.HP = self.max_hp
        self.armour = self.max_armour
        self.mana = self.max_mana
        
        self.timer_hit = 0
        self.timer_armour = 0
        self.timer_attack = 0
        self.weapons = []
        self.weapon = None

    def set_weapons(self, weapons = None):
        if weapons == None:
            self.weapons = ["glock","ak47","sniper"]
            self.change_weapon(0)
        else:
            self.weapons = weapons
            self.change_weapon(0)

    def change_weapon(self, index):
        # Import locally to avoid circular dependency
        from sprites.weapons import Glock, AK47, Sniper
        
        if self.weapons[index] == None: return False
        if self.weapons[index] == "glock":
            if self.weapon: self.weapon.kill()
            self.weapon = Glock(self.game, self)
        if self.weapons[index] == "ak47":
            if self.weapon: self.weapon.kill()
            self.weapon = AK47(self.game, self)
        if self.weapons[index] == "sniper":
            if self.weapon: self.weapon.kill()
            self.weapon = Sniper(self.game, self)

    def update(self):
        self.movement()
        self.animate()
        self.find_nearest_enemy()
        self.collide_enemy()
        self.collide_bullet()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")
        
        self.x_change = 0
        self.y_change = 0

        #sau 3s khong chien dau se hoi 1 giap / s
        if self.armour < self.max_armour and pygame.time.get_ticks() - self.timer_attack > 3000:
            if pygame.time.get_ticks() - self.timer_armour > 1000:
                self.armour += 1
                self.timer_armour = pygame.time.get_ticks()
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if(self.rect.centerx < WIN_WIDTH/2 + CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.x -= PLAYER_SPEED
            self.x_change = -PLAYER_SPEED
            if self.find_nearest_enemy() == None: self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if(self.rect.centerx > WIN_WIDTH/2 - CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.x += PLAYER_SPEED
            self.x_change = PLAYER_SPEED
            if self.find_nearest_enemy() == None: self.facing = "right"
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if(self.rect.centery < WIN_HEIGHT/2 + CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.y += PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.y -= PLAYER_SPEED
            self.y_change = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if(self.rect.centery > WIN_HEIGHT/2 - CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.y -= PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.y += PLAYER_SPEED
            self.y_change = PLAYER_SPEED
        
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.take_dmg(0)

    def take_dmg(self, dmg):
        if pygame.time.get_ticks() - self.timer_hit > 800:
            if(self.armour > 0):
                self.armour -= dmg
            else:
                self.HP -= dmg
            self.timer_attack = pygame.time.get_ticks()
            self.timer_hit = pygame.time.get_ticks()
            if(self.HP <= 0):
                self.game.playing = False

    def collide_bullet(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies_bullets, False)
        if hits:
            self.take_dmg(1)
            hits[0].kill()

    def collide_blocks(self, dir):
        # Import locally to avoid circular dependency
        from sprites.map.entrance import Entrance
        
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
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

    def animate(self):
        if self.facing == "left":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
        
        if self.facing == "right":
            if self.x_change == 0 and self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.animation_loop >= 3:
            self.animation_loop = 1

    # auto aim toward nearest enemy
    def find_nearest_enemy(self):
        #update rad to place the gun
        if self.y_change != 0 or self.x_change != 0:
            self.rad = math.atan2(self.y_change, self.x_change)
        nearest_enemy = None
        if(self.game.enemies.sprites()):
            nearest_enemy = min(self.game.enemies, key=lambda x: math.sqrt((x.rect.x - self.rect.x)**2 + (x.rect.y - self.rect.y)**2))
            if math.sqrt((nearest_enemy.rect.x - self.rect.x)**2 + (nearest_enemy.rect.y - self.rect.y)**2) < self.weapon.scope:
                dy = nearest_enemy.rect.y - self.rect.y
                dx = nearest_enemy.rect.x - self.rect.x
                self.rad = math.atan2(dy, dx)
        
        #rad so voi vi tri con chuot -> disable auto aim
        # self.rad = math.atan2(pygame.mouse.get_pos()[1] - self.rect.centery, pygame.mouse.get_pos()[0] - self.rect.centerx)
        return nearest_enemy

    def earnManaAndPoints(self, mana, points):
        if self.mana + mana <= self.max_mana:
            self.mana += mana
        else:
            self.mana = self.max_mana

        self.score += points