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
    def __init__(self, game, x, y, others):
        self.game = game
        # game.player = self 
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE + (others[0] * WIN_WIDTH) 
        self.y = y * TILE_SIZE + (others[1] * WIN_HEIGHT) 
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
        self.max_armour = 3
        self.max_mana = 128

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
        if self.weapons[index] == None: return False
        if self.weapons[index] == "glock":
            if self.weapon: self.weapon.kill()
            self.weapon = Glock(self.game)
        if self.weapons[index] == "ak47":
            if self.weapon: self.weapon.kill()
            self.weapon = AK47(self.game)
        if self.weapons[index] == "sniper":
            if self.weapon: self.weapon.kill()
            self.weapon = Sniper(self.game)

    def update(self):
        self.movement()
        self.animate()
        self.collide_enemy()

        if self.y_change != 0 or self.x_change != 0:
            self.rad = math.atan2(self.y_change, self.x_change)

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")
        
        self.x_change = 0
        self.y_change = 0

        #TODO: sau 4s khong chien dau se hoi 1 giap / s
        if self.armour < self.max_armour and pygame.time.get_ticks() - self.timer_attack > 4000:
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
            if self.game.player.weapon.find_nearest_enemy() == None: self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if(self.rect.centerx > WIN_WIDTH/2 - CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.x += PLAYER_SPEED
            self.x_change = PLAYER_SPEED
            if self.game.player.weapon.find_nearest_enemy() == None: self.facing = "right"
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
            if pygame.time.get_ticks() - self.timer_hit > 500:
                if(self.armour > 0):
                    self.armour -= 1
                else:
                    self.HP -= 1
                self.timer_attack = pygame.time.get_ticks()
                self.timer_hit = pygame.time.get_ticks()
                if(self.HP <= 0):
                    self.game.playing = False

    def collide_blocks(self, dir):
        if (dir == "x"):
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.game.entrances.has(hits[0]) == False or hits[0].enable == True:
                    if self.x_change > 0:
                        self.rect.right = hits[0].rect.left
                    if self.x_change < 0:
                        self.rect.left = hits[0].rect.right
                
        if (dir == "y"):
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.game.entrances.has(hits[0]) == False or hits[0].enable == True:
                    if self.y_change > 0:
                        self.rect.bottom = hits[0].rect.top
                    if self.y_change < 0:
                        self.rect.top = hits[0].rect.bottom

    def animate(self):
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
        
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.animation_loop >= 3:
            self.animation_loop = 1


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, others, room):
        self.game = game
        self._layer = ENERMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE + (others[0] * WIN_WIDTH)
        self.y = y * TILE_SIZE + (others[1] * WIN_HEIGHT)
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(["left", "right", "up", "down"])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(30, 60)

        self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x  = self.x
        self.rect.y = self.y

        self.down_animations = [self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 2, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(67, 2, self.width, self.height)]
        
        self.up_animations = [self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 34, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(67, 34, self.width, self.height)]

        self.right_animations = [self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(67, 66, self.width, self.height)]

        self.left_animations = [self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(35, 98, self.width, self.height),
                            self.game.enemy_spritesheet.get_sprite(67, 98, self.width, self.height)]
    
        self.HP = 3
        self.room = room

    def normal_movement(self):
        if self.facing == "up":
            self.y_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "down"
        elif self.facing == "down":
            self.y_change += ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "up"
        elif self.facing == "left":
            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "right"
        elif self.facing == "right":
            self.x_change += ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = "left"

        if self.movement_loop <= -self.max_travel:
            self.movement_loop = 0
            self.facing = random.choice(["left", "right", "up", "down"])
            self.max_travel = random.randint(30, 60)
        pass

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
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 2, self.width, self.height)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 34, self.width, self.height)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1

        if self.animation_loop >= 3:
            self.animation_loop = 1

    def collide_blocks(self, dir):
        if (dir == "x"):
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:

                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                if self.x_change < 0:
                    self.rect.left = hits[0].rect.right
                
        if (dir == "y"):
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
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
                self.game.player.score += 1
                if self.game.player.mana <= self.game.player.max_mana - 10:
                    self.game.player.mana += 10
                else :
                    self.game.player.mana = self.game.player.max_mana

    def movement(self):
        if(math.sqrt((self.game.player.rect.x - self.rect.x)**2 + (self.game.player.rect.y - self.rect.y)**2) < ENEMY_SCOPE and self.room.open == False):
            self.taunted_movement()
        else:
            self.normal_movement()

    def taunted_movement(self):
        dx = self.game.player.rect.centerx - self.rect.centerx
        dy = self.game.player.rect.centery - self.rect.centery
        self.rad = round(math.atan2(dy, dx),2)
        self.x_change = ENEMY_SPEED * math.cos(self.rad)
        self.y_change = ENEMY_SPEED * math.sin(self.rad)
        #facing update
        if abs(dx) > abs(dy):
            if dx > 0:
                self.facing = "right"
            else:
                self.facing = "left"
        else:
            if dy > 0:
                self.facing = "down"
            else:
                self.facing = "up"

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y, others):

        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE + (others[0] * WIN_WIDTH)
        self.y = y * TILE_SIZE + (others[1] * WIN_HEIGHT)
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(384, 576, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y, others):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE + (others[0] * WIN_WIDTH)
        self.y = y * TILE_SIZE + (others[1] * WIN_HEIGHT)
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(64, 352, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.game = game
        self.x = x
        self.y = y
        self.width = WEAPON_SIZE
        self.height = WEAPON_SIZE
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.collide()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]
        
        if direction == "up":
            self.image = up_animations[math.floor(self.animation_loop)]
        if direction == "down":
            self.image = down_animations[math.floor(self.animation_loop)]
        if direction == "left":
            self.image = left_animations[math.floor(self.animation_loop)]
        if direction == "right":
            self.image = right_animations[math.floor(self.animation_loop)]

        self.animation_loop += 0.5
        if self.animation_loop >= 5:
            self.kill()
    #end
#end           
class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, heading, rad, dmg, rad_offset):
        self._layer = BULLET_LAYER
        self.game = game
        self.dmg = dmg
        self.x = heading[0]
        self.y = heading[1]
        self.width = 10
        self.height = 10
        self.groups = self.game.all_sprites, self.game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, YELLOW, (self.width//2, self.height//2), self.width//2)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.x_change = 0
        self.y_change = 0
        self.rad = rad + random.randint(-abs(rad_offset), abs(rad_offset)) * math.pi/180
        self.max_travel = WIN_WIDTH
        
    def movement(self):
        self.rect.x += BULLET_SPEED * math.cos(self.rad)
        self.rect.y += BULLET_SPEED * math.sin(self.rad)
        self.max_travel -= BULLET_SPEED
        if self.max_travel <= 0:
            self.kill()

    def update(self):
        self.movement()
        self.collide_blocks()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

    def collide_blocks(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            self.kill()

class Gun(pygame.sprite.Sprite):
    def find_nearest_enemy(self):
        nearest_enemy = None
        self.rad = self.game.player.rad
        if(self.game.enemies.sprites()):
            nearest_enemy = min(self.game.enemies, key=lambda x: math.sqrt((x.rect.x - self.game.player.rect.x)**2 + (x.rect.y - self.game.player.rect.y)**2))
            if math.sqrt((nearest_enemy.rect.x - self.game.player.rect.x)**2 + (nearest_enemy.rect.y - self.game.player.rect.y)**2) < self.scope:
                dy = nearest_enemy.rect.y - self.game.player.rect.y
                dx = nearest_enemy.rect.x - self.game.player.rect.x
                self.rad = math.atan2(dy, dx)
        return nearest_enemy
    
    def update(self):
        self.animate()
        self.movement()

    def animate(self):
        next_image = self.shoot_animation[math.floor(self.animation_loop)].copy()
        if self.have_left_enemy(): 
            next_image = pygame.transform.flip(next_image.copy(), True, False)
            rad = self.rad + math.pi
            self.game.player.facing = "left"
            self._layer = PLAYER_LAYER - 1
            self.game.all_sprites.change_layer(self, PLAYER_LAYER - 1)
            self.game.guns.change_layer(self, PLAYER_LAYER - 1)
            self.image = pygame.transform.rotate(next_image, math.degrees(-rad))
        else: 
            self.game.player.facing = "right"
            self._layer = PLAYER_LAYER + 1
            self.game.all_sprites.change_layer(self, PLAYER_LAYER + 1)
            self.game.guns.change_layer(self, PLAYER_LAYER + 1)
            self.image = pygame.transform.rotate(next_image, math.degrees(-self.rad))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.game.player.attacking:
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.animation_loop = 0
                self.game.player.attacking = False

    def movement(self):
        if self.game.player.facing == "right":
            self.rect.center = (self.game.player.rect.centerx + self.place_right[0], self.game.player.rect.centery + self.place_right[1])
        if self.game.player.facing == "left":
            self.rect.center = (self.game.player.rect.centerx - self.place_right[0], self.game.player.rect.centery + self.place_right[1])

    def have_left_enemy(self):
        self.find_nearest_enemy()
        return (self.rad > -math.pi and self.rad < -math.pi/2) or (self.rad >= math.pi/2 and  self.rad <= math.pi)
    
    def shoot(self):
        Bullet(self.game, self.find_heading(), self.rad, self.bullet_dmg, self.rad_offset)
        self.game.player.mana -= self.manacost

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.timer > self.delay and self.game.player.mana >= self.manacost:
            self.timer = now
            return True
        return False
    
    def find_heading(self):
        center_image = (self.width/2, self.height/2)
        vector = (self.headpos[0] - center_image[0], self.headpos[1] - center_image[1])
        hypotenuse = math.sqrt(vector[0]**2 + vector[1]**2)
        alpha = math.acos(vector[0]/hypotenuse)
        if self.game.player.facing == "right":
            alpha = -alpha
        headx = self.rect.centerx +  hypotenuse * math.cos(self.rad+alpha)
        heady = self.rect.centery +  hypotenuse * math.sin(self.rad+alpha)
        return headx, heady

class Glock(Gun):
    def __init__(self, game):
        self._layer = GUN_LAYER
        self.game = game
        self.x = self.game.player.rect.centerx
        self.y = self.game.player.rect.centery
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
        self.rad = self.game.player.rad
        self.scope = GLOCK_SCOPE
        self.delay = GLOCK_DELAY
        self.bullet_dmg = 1
        self.rad_offset = 3

        #pos against player to place gun when facing right
        self.place_right = (8, 6)
        self.headpos = (40, 8)
        self.manacost = 0

class AK47(Gun):
    def __init__(self, game):
        self._layer = GUN_LAYER
        self.game = game
        self.x = self.game.player.rect.centerx
        self.y = self.game.player.rect.centery
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
        self.rad = self.game.player.rad
        self.scope = AK47_SCOPE
        self.delay = AK47_DELAY
        self.bullet_dmg = 1
        self.rad_offset = 4
        #pos against player to place gun when facing right
        self.place_right = (6, 4)
        self.headpos = (48, 4)
        self.manacost = 2

class Sniper(Gun):
    def __init__(self, game):
        self._layer = GUN_LAYER
        self.game = game
        self.x = self.game.player.rect.centerx
        self.y = self.game.player.rect.centery
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
        self.rad = self.game.player.rad
        self.scope = SNIPER_SCOPE
        self.delay = SNIPER_DELAY
        self.bullet_dmg = 3
        self.rad_offset = 1
        #pos against player to place gun when facing right
        self.place_right = (8, 4)
        self.headpos = (48, 6)
        self.manacost = 5

class Entrance(pygame.sprite.Sprite):
    def __init__(self, game, x, y, others):
        self.enable = True
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.entrances, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILE_SIZE + (others[0] * WIN_WIDTH)
        self.y = y * TILE_SIZE + (others[1] * WIN_HEIGHT)
        self.width = TILE_SIZE
        self.height = TILE_SIZE

        self.image = self.game.terrain_spritesheet.get_sprite(384, 576, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if(self.enable): 
            self.image = self.game.terrain_spritesheet.get_sprite(704, 160, self.width, self.height)
        else:
            self.image = self.game.terrain_spritesheet.get_sprite(95, 576, self.width, self.height)

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font('miniproject/pygameRPG/Arial.ttf', fontsize)
        self.content = content
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.width = width
        self.fg = fg

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(bg)
        self.rect = self.image.get_rect()
        
        self.rect.x = self.x
        self.rect.y = self.y
        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
        self.image.blit(self.text, self.text_rect)

    def isPressed(self, mousepos, pressed):
        if self.rect.collidepoint(mousepos):
            if pressed[0]:
                return True
        return False
    
class MyMap(pygame.sprite.Sprite): 
    def __init__(self, tilemap, game):
        self._layer = MAP_LAYER
        self.mappingpos = [0, 0]
        self.tilemap = tilemap
        self.isDrawn = False
        self.game = game
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None
        self.num_enemies = 0
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.entrances = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
    def draw(self):
        create_tilemap(self.game, self.tilemap, self.mappingpos, self)
        self.isDrawn = True
        self.draw_pipes()
         
    def draw_pipes(self):
        if(self.top != None):
            pipe_mapping_pos = [self.mappingpos[0], self.mappingpos[1] - 1]
            create_tilemap(self.game, vpipemap, pipe_mapping_pos)
        if(self.bottom != None):
            pipe_mapping_pos = [self.mappingpos[0], self.mappingpos[1] + 1]
            create_tilemap(self.game, vpipemap, pipe_mapping_pos)
        if(self.left != None):
            pipe_mapping_pos = [self.mappingpos[0] - 1, self.mappingpos[1]]
            create_tilemap(self.game, hpipemap, pipe_mapping_pos)
        if(self.right != None):
            pipe_mapping_pos = [self.mappingpos[0] + 1, self.mappingpos[1]]
            create_tilemap(self.game, hpipemap, pipe_mapping_pos)

    def checkEntrance(self, i, j):
        if(self.top != None):
            if i == 0 and j > 6 and j < 13:
                return True
        if(self.bottom != None):
            if i == 14 and j > 6 and j < 13:
                return True
        if(self.left != None):
            if j == 0 and i > 4 and i < 10:
                return True
        if(self.right != None):
            if j == 19 and i > 4 and i < 10:
                return True
        return False

    def update(self):
        count  = 0
        for sprite in self.enemy_sprites:
            if sprite.HP > 0: count += 1
        self.num_enemies = count
        if self.rect.contains(self.game.player.rect) and self.num_enemies > 0:
            for sprite in self.entrances:
                sprite.enable = True
            self.open = False
        else:
            for sprite in self.entrances:
                sprite.enable = False
            self.open = True

    def update_rect(self):
        self.image = pygame.Surface((WIN_WIDTH - TILE_SIZE*2, WIN_HEIGHT - TILE_SIZE*2))
        self.rect = self.image.get_rect()
        self.rect.topleft = ( 32 + self.mappingpos[0] * WIN_WIDTH, 32 + self.mappingpos[1] * WIN_HEIGHT)
        
class MapList:
    def __init__(self, tilemaps, game):
        self.maps = []
        for tilemap in tilemaps:
            self.maps.append(MyMap(tilemap, game))

        self.link(self.maps[0], self.maps[1], "right")
        self.link(self.maps[1], self.maps[2], "top")
        self.link(self.maps[1], self.maps[3], "bottom")

        for map in self.maps:
            map.update_rect()
        
    def draw(self):
        self.DFS_draw(self.maps[0])

    def DFS_draw(self, map):
        map.draw()
        for adj in [map.top, map.bottom, map.left, map.right]:
            if  adj != None and not adj.isDrawn:
                self.DFS_draw(adj)

    def link(self, m1, m2, dir):
        if(dir == "right"):
            m1.right = m2
            m2.left = m1
            m2.mappingpos = [m1.mappingpos[0] + 2, m1.mappingpos[1]]
        if(dir == "left"):
            m1.left = m2
            m2.right = m1
            m2.mappingpos = [m1.mappingpos[0] - 2, m1.mappingpos[1]]
        if(dir == "top"):
            m1.top = m2
            m2.bottom = m1
            m2.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] - 2]
        if(dir == "bottom"):
            m1.bottom = m2
            m2.top = m1
            m2.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] + 2]

def create_tilemap(game, tilemap, mappingpos, mymap: MyMap = None):
    for i, row in enumerate(tilemap):
        for j, col in enumerate(row):
            if col == 'B':
                if(mymap != None and mymap.checkEntrance(i, j)):
                    sprite = Entrance(game, j, i, mappingpos)
                    mymap.entrances.add(sprite)
                else: block = Block(game, j, i, mappingpos)
            if col == 'E':
                if(mymap != None):
                    enemy = Enemy(game, j, i, mappingpos, mymap)
                    mymap.enemy_sprites.add(enemy)
            if col == 'P':
                game.player = Player(game, j, i, mappingpos)
                game.player.set_weapons()
            if(col == ' '): continue
            Ground(game, j, i, mappingpos)

class PlayerBars(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = UI_LAYER
        self.groups = game.bars
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.font = pygame.font.Font('miniproject/pygameRPG/Arial.ttf', 16)

        self.image = pygame.Surface((180, 92))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

        self.health_background = pygame.Surface((128, 20))
        self.health_background.fill(DARK_BROWN)
        self.armour_background = pygame.Surface((128, 20))
        self.armour_background.fill(DARK_BROWN)
        self.mana_background = pygame.Surface((128, 20))
        self.mana_background.fill(DARK_BROWN)

        #just a surface
        self.health_icon = pygame.Surface((20, 20))
        self.health_icon.fill(RED)
        self.armour_icon = pygame.Surface((20, 20))
        self.armour_icon.fill(GREY)
        self.mana_icon = pygame.Surface((20, 20))
        self.mana_icon.fill(BLUE)
        
        self.health_bar = pygame.Surface((128, 20))
        self.health_bar.fill(RED)
        self.health_bar_rect = self.health_bar.get_rect()
        self.health_bar_rect.x = 42
        self.health_bar_rect.y = 8

        self.armour_bar = pygame.Surface((128, 20))
        self.armour_bar.fill(GREY)
        self.armour_bar_rect = self.armour_bar.get_rect()
        self.armour_bar_rect.x = 42
        self.armour_bar_rect.y = 36

        self.mana_bar = pygame.Surface((128, 20))
        self.mana_bar.fill(BLUE)
        self.mana_bar_rect = self.mana_bar.get_rect()
        self.mana_bar_rect.x = 42
        self.mana_bar_rect.y = 64
        
        self.image.fill(BROWN)
        self.image.blit(self.health_background, self.health_bar_rect)
        self.image.blit(self.armour_background, self.armour_bar_rect)
        self.image.blit(self.mana_background, self.mana_bar_rect)
        self.image.blit(self.health_icon, (10, 8))
        self.image.blit(self.armour_icon, (10, 36))
        self.image.blit(self.mana_icon, (10, 64))
        self.image.blit(self.health_bar, self.health_bar_rect)
        self.image.blit(self.armour_bar, self.armour_bar_rect)
        self.image.blit(self.mana_bar, self.mana_bar_rect)
        
    def update(self):
        self.draw_HP()
        self.draw_AR()
        self.draw_MP()
        pass

    def draw_HP(self):
        self.health_background.fill(DARK_BROWN)
        self.health_bar = pygame.Surface((128 * self.game.player.HP / self.game.player.max_hp, 20))
        info = self.font.render(f"{self.game.player.HP}/{self.game.player.max_hp}", True, WHITE)
        info_rect = info.get_rect()
        info_rect.center = self.health_bar_rect.center
        self.health_bar.fill(RED)
        self.image.blit(self.health_background, self.health_bar_rect)
        self.image.blit(self.health_bar, self.health_bar_rect)
        self.image.blit(info, info_rect)
    
    def draw_AR(self):
        self.armour_background.fill(DARK_BROWN)
        self.armour_bar = pygame.Surface((128 * self.game.player.armour / self.game.player.max_armour, 20))
        info = self.font.render(f"{self.game.player.armour}/{self.game.player.max_armour}", True, WHITE)
        info_rect = info.get_rect()
        info_rect.center = self.armour_bar_rect.center
        self.armour_bar.fill(GREY)
        self.image.blit(self.armour_background,  self.armour_bar_rect)
        self.image.blit(self.armour_bar, self.armour_bar_rect)
        self.image.blit(info, info_rect)
    
    def draw_MP(self):
        self.mana_background.fill(DARK_BROWN)
        self.mana_bar = pygame.Surface((128 * self.game.player.mana / self.game.player.max_mana, 20))
        info = self.font.render(f"{self.game.player.mana}/{self.game.player.max_mana}", True, WHITE)
        info_rect = info.get_rect()
        info_rect.center = self.mana_bar_rect.center
        self.mana_bar.fill(BLUE)
        self.image.blit(self.mana_background, self.mana_bar_rect)
        self.image.blit(self.mana_bar, self.mana_bar_rect)
        self.image.blit(info, info_rect)