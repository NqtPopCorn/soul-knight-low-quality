import pygame
from utils import get_asset_path

class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font(get_asset_path('Arial.ttf'), fontsize)
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
