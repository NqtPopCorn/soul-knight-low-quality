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
    
    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if(self.rect.centerx < WIN_WIDTH/2 + CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.x += PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.x -= PLAYER_SPEED
            self.x_change = -PLAYER_SPEED
            if self.game.player_weapon.target_nearest_enemy() == None: self.facing = "left"
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if(self.rect.centerx > WIN_WIDTH/2 - CAMERA_SIZE):
                for sprite in self.game.all_sprites:
                    sprite.rect.x -= PLAYER_SPEED
                for attack in self.game.attacks:
                    attack.rect.x += PLAYER_SPEED
            self.x_change = PLAYER_SPEED
            if self.game.player_weapon.target_nearest_enemy() == None: self.facing = "right"
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
            self.game.playing = False

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
    def __init__(self, game, x, y, others):
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
        Player.collide_blocks(self, "x")
        self.rect.y += self.y_change
        Player.collide_blocks(self, "y")

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
            self.HP -= 1
            hits[0].kill()
            if self.HP <= 0:
                self.kill()
                self.game.player.score += 1

    def movement(self):
        if(math.sqrt((self.game.player.rect.x - self.rect.x)**2 + (self.game.player.rect.y - self.rect.y)**2) > ENEMY_SCOPE):
            self.normal_movement()
        else:
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
    def __init__(self, game, x, y):
        self._layer = BULLET_LAYER
        self.game = game
        self.x = x
        self.y = y
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
        self.rad = self.game.player.rad
        if(self.game.enemies.sprites()):
            nearest_enemy = min(self.game.enemies, key=lambda x: math.sqrt((x.rect.centerx - self.rect.centerx)**2 + (x.rect.centery - self.rect.centery)**2))
            if math.sqrt((nearest_enemy.rect.x - x)**2 + (nearest_enemy.rect.y - y)**2) < GLOCK_SCOPE:
                dy = nearest_enemy.rect.y - y
                dx = nearest_enemy.rect.x - x
                #tao do lech cho dan
                random_x = random.randint(-abs(dx)//3, abs(dx)//3)
                random_y = random.randint(-abs(dy)//3, abs(dy)//3)
                dx += random_x
                dy += random_y
                self.rad = math.atan2(dy, dx)

    def movement(self):
        self.rect.x += BULLET_SPEED * math.cos(self.rad)
        self.rect.y += BULLET_SPEED * math.sin(self.rad)

    def update(self):
        self.movement()
        self.collide_blocks()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
    
    def collide_blocks(self):
        hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
        if hits:
            self.kill()

class Glock(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = GUN_LAYER
        self.game = game
        self.x = self.game.player.rect.centerx - 8
        self.y = self.game.player.rect.centery + 8
        self.width = 48
        self.height = 32
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.animation_loop = 0
        self.image = self.game.glock_spritesheet.get_sprite(0, 0, self.width, self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.shoot_animation = [self.game.glock_spritesheet.get_sprite(0, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(48, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(96, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(144, 0, self.width, self.height),
                            self.game.glock_spritesheet.get_sprite(192, 0, self.width, self.height)]
        self.timer = 0
        self.rad = 0
        self.scope = GLOCK_SCOPE
        self.delay = GLOCK_DELAY

    def update(self):
        self.movement()
        self.animate()

    def target_nearest_enemy(self):
        nearest_enemy = None
        self.rad = self.game.player.rad
        if(self.game.enemies.sprites()):
            nearest_enemy = min(self.game.enemies, key=lambda x: math.sqrt((x.rect.centerx - self.rect.centerx)**2 + (x.rect.centery - self.rect.centery)**2))
            if math.sqrt((nearest_enemy.rect.x - self.rect.x)**2 + (nearest_enemy.rect.y - self.rect.y)**2) < GLOCK_SCOPE:
                dy = nearest_enemy.rect.y - self.rect.y
                dx = nearest_enemy.rect.x - self.rect.x
                self.rad = round(math.atan2(dy, dx),2)
        return nearest_enemy
    
    def animate(self):
        self.target_nearest_enemy()
        next_image = self.shoot_animation[math.floor(self.animation_loop)].copy()
        if (self.rad > -math.pi and self.rad < -math.pi/2) or (self.rad > math.pi/2 and  self.rad <= math.pi): 
            next_image = pygame.transform.flip(next_image.copy(), True, False)
            self.rad = self.rad - math.pi
            self.game.player.facing = "left"
        else: self.game.player.facing = "right"
        self.image = pygame.transform.rotate(next_image, int(math.degrees(-self.rad)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.game.player.attacking:
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.animation_loop = 0
                self.game.player.attacking = False

    def movement(self):
        self.rect.x = self.game.player.rect.x
        self.rect.y = self.game.player.rect.y

    def shoot(self):
        # headx = (self.rect.right-8) * math.cos(self.rad) - (self.rect.centery-8) * math.sin(self.rad)
        # heady = (self.rect.centery-8) * math.sin(self.rad) + (self.rect.right-8) * math.cos(self.rad)
        if (self.rad > -math.pi and self.rad < -math.pi/2) or (self.rad > math.pi/2 and  self.rad <= math.pi): 
            self.game.player.facing = "left"
        else: self.game.player.facing = "right"
        Bullet(self.game, self.rect.right-8, self.rect.centery-8)

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.timer > GLOCK_DELAY:
            self.timer = now
            return True
        return False

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