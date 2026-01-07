import pygame
from config import *
from utils import get_asset_path

class PlayerBars(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = BAR_LAYER
        self.groups = game.bars
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.font = pygame.font.Font(get_asset_path('Arial.ttf'), 16)
        self.icon_size = (20, 18)
        self.bar_size = (100, 18)
        self.gap = 8

        self.image = pygame.Surface((self.icon_size[0] + self.bar_size[0] + self.gap*3, self.icon_size[1]*3 + self.gap*4))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 10

        self.health_icon = pygame.Surface(self.icon_size)
        self.health_icon.fill(RED)
        self.armour_icon = pygame.Surface(self.icon_size)
        self.armour_icon.fill(GREY)
        self.mana_icon = pygame.Surface(self.icon_size)
        self.mana_icon.fill(BLUE)

        self.health_icon_rect = self.health_icon.get_rect()
        self.health_icon_rect.topleft = (self.gap, self.gap)
        self.armour_icon_rect = self.armour_icon.get_rect()
        self.armour_icon_rect.topleft = (self.health_icon_rect.left, self.health_icon_rect.bottom + self.gap)
        self.mana_icon_rect = self.mana_icon.get_rect()
        self.mana_icon_rect.topleft = (self.health_icon_rect.left, self.armour_icon_rect.bottom + self.gap)

        self.health_bg = pygame.Surface(self.bar_size)
        self.health_bg.fill(DARK_BROWN)
        self.armour_bg = pygame.Surface(self.bar_size)
        self.armour_bg.fill(DARK_BROWN)
        self.mana_bg = pygame.Surface(self.bar_size)
        self.mana_bg.fill(DARK_BROWN)

        self.health_bg_rect = self.health_bg.get_rect()
        self.armour_bg_rect = self.armour_bg.get_rect()
        self.mana_bg_rect = self.mana_bg.get_rect()
        self.health_bg_rect.topleft = (self.health_icon_rect.right + self.gap, self.health_icon_rect.top)
        self.armour_bg_rect.topleft = (self.armour_icon_rect.right + self.gap, self.armour_icon_rect.top)
        self.mana_bg_rect.topleft = (self.mana_icon_rect.right + self.gap, self.mana_icon_rect.top)
        
        self.health_bar = pygame.Surface(self.bar_size)
        self.health_bar.fill(RED)
        self.armour_bar = pygame.Surface(self.bar_size)
        self.armour_bar.fill(GREY)
        self.mana_bar = pygame.Surface(self.bar_size)
        self.mana_bar.fill(BLUE)

        #rect doi voi cac bg tuong ung
        self.health_bar_rect = self.health_bar.get_rect()
        self.health_bar_rect.topleft = (0 ,0)
        self.armour_bar_rect = self.armour_bar.get_rect()
        self.armour_bar_rect.topleft = (0 ,0)
        self.mana_bar_rect = self.mana_bar.get_rect()
        self.mana_bar_rect.topleft = (0 ,0)
        
        self.health_bg.blit(self.health_bar, self.health_bar_rect)
        self.armour_bg.blit(self.armour_bar, self.armour_bar_rect)
        self.mana_bg.blit(self.mana_bar, self.mana_bar_rect)

        self.image.fill(BROWN)
        self.image.blit(self.health_bg, self.health_bg_rect)
        self.image.blit(self.armour_bg, self.armour_bg_rect)
        self.image.blit(self.mana_bg, self.mana_bg_rect)
        self.image.blit(self.health_icon, self.health_icon_rect)
        self.image.blit(self.armour_icon, self.armour_icon_rect)
        self.image.blit(self.mana_icon, self.mana_icon_rect)
        
    def update(self):
        self.draw_HP()
        self.draw_AR()
        self.draw_MP()
        pass

    def draw_HP(self):
        self.health_bg.fill(DARK_BROWN)
        self.health_bar_rect.right = self.bar_size[0] * self.game.player.HP / self.game.player.max_hp
        info = self.font.render(f"{self.game.player.HP}/{self.game.player.max_hp}", True, WHITE)
        info_rect = info.get_rect()
        info_rect.center = self.health_bg_rect.center
        self.health_bg.blit(self.health_bar, self.health_bar_rect)
        self.image.blit(self.health_bg, self.health_bg_rect)
        self.image.blit(info, info_rect)
    
    def draw_AR(self):
        self.armour_bg.fill(DARK_BROWN)
        self.armour_bar_rect.right = self.bar_size[0] * self.game.player.armour / self.game.player.max_armour
        info = self.font.render(f"{self.game.player.armour}/{self.game.player.max_armour}", True, WHITE)
        info_rect = info.get_rect()
        info_rect.center = self.armour_bg_rect.center
        self.armour_bg.blit(self.armour_bar, self.armour_bar_rect)
        self.image.blit(self.armour_bg,  self.armour_bg_rect)
        self.image.blit(info, info_rect)
    
    def draw_MP(self):
        self.mana_bg.fill(DARK_BROWN)
        self.mana_bar_rect.right = self.bar_size[0] * self.game.player.mana / self.game.player.max_mana
        info = self.font.render(f"{self.game.player.mana}/{self.game.player.max_mana}", True, WHITE)
        info_rect = info.get_rect()
        info_rect.center = self.mana_bg_rect.center
        self.mana_bg.blit(self.mana_bar, self.mana_bar_rect)
        self.image.blit(self.mana_bg, self.mana_bg_rect)
        self.image.blit(info, info_rect)
