import pygame
import math
from config import *

class Gun(pygame.sprite.Sprite):
    """Base class for all weapons"""
    
    def update(self):
        self.rad = self.owner.rad
        self.animate()
        self.movement()

    def animate(self):
        # Local import to avoid circular dependency
        from sprites.characters import Player
        
        next_image = self.shoot_animation[math.floor(self.animation_loop)].copy()
        if self.have_left_target(): 
            next_image = pygame.transform.flip(next_image.copy(), True, False)
            rad = self.rad + math.pi
            self.owner.facing = "left"
            if self.alive():
                self.game.all_sprites.change_layer(self, self.owner._layer - 1)
                self.game.guns.change_layer(self, self.owner._layer - 1)
            self.image = pygame.transform.rotate(next_image, math.degrees(-rad))
        else: 
            self.owner.facing = "right"
            if self.alive():
                self.game.all_sprites.change_layer(self, self.owner._layer + 1)
                self.game.guns.change_layer(self, self.owner._layer + 1)
            self.image = pygame.transform.rotate(next_image, math.degrees(-self.rad))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(center=self.rect.center)

        if self.owner.attacking:
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                self.animation_loop = 0
                self.owner.attacking = False

    def movement(self):
        if self.owner.facing == "right":
            self.rect.center = (self.owner.rect.centerx + self.place_right[0], self.owner.rect.centery + self.place_right[1])
        if self.owner.facing == "left":
            self.rect.center = (self.owner.rect.centerx - self.place_right[0], self.owner.rect.centery + self.place_right[1])

    def have_left_target(self):
        return (self.rad > -math.pi and self.rad < -math.pi/2) or (self.rad >= math.pi/2 and  self.rad <= math.pi)
    
    def shoot(self):
        from sprites.weapons.bullet import Bullet
        from sprites.characters import Player
        
        Bullet(self.game, self.find_heading(), self.rad, self.bullet_dmg, self.rad_offset, self.speed, self.owner)
        if isinstance(self.owner, Player):
            self.owner.mana -= self.manacost

    def can_shoot(self):
        # Local import to avoid circular dependency
        from sprites.characters import Enemy, Player
        
        now = pygame.time.get_ticks()
        if now - self.timer > self.delay and (isinstance(self.owner, Enemy) or self.owner.mana >= self.manacost):
            self.timer = now
            return True
        return False
    
    def find_heading(self):
        center_image = (self.width/2, self.height/2)
        vector = (self.headpos[0] - center_image[0], self.headpos[1] - center_image[1])
        hypotenuse = math.sqrt(vector[0]**2 + vector[1]**2)
        alpha = math.acos(vector[0]/hypotenuse)
        if self.owner.facing == "right":
            alpha = -alpha
        headx = self.rect.centerx +  hypotenuse * math.cos(self.rad+alpha)
        heady = self.rect.centery +  hypotenuse * math.sin(self.rad+alpha)
        return headx, heady
