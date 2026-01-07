import pygame
import random
from config import *
from sprites.characters.enemy import Enemy
from sprites.characters.player import Player
from sprites.characters.boss import Boss
from sprites.map.block import Block
from sprites.map.entrance import Entrance
from sprites.map.ground import Ground
from sprites.characters.boss_bars import BossHPBar

class GameRoom(pygame.sprite.Sprite): 
    def __init__(self, tilemap, game, phase_num = 0):
        self._layer = MAP_LAYER
        self.mappingpos = [0, 0]
        self.tilemap = tilemap
        self.isDrawn = False
        self.game = game
        #start position of the map including the border
        self.x = 0
        self.y = 0
        #display a invisible rect to check if player is in the map, it not include the border(32 pixels block)
        self.image = pygame.Surface((WIN_WIDTH - TILE_SIZE*2, WIN_HEIGHT - TILE_SIZE*2))
        self.rect = self.image.get_rect()

        self.top = None
        self.bottom = None
        self.left = None
        self.right = None

        self.num_enemies = 0
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.entrances = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.open = True
        self.max_phase = phase_num
        self.current_phase = 0
        self.available_pos = []
        self.clear = False
        self.current_phase = 1

    def draw(self):
        self.create_tilemap()
        self.isDrawn = True

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
    
    def check_corner(self, i, j):
        if (i, j) in [(0,0), (0,19), (14,0), (14,19)]:
            return True
        if(self.top != None):
            if (i,j) in [(0,6), (0,13)]:
                return True
        if(self.bottom != None):
            if (i,j) in [(14,6), (14,13)]:
                return True
        if(self.left != None):
            if (i,j) in [(4, 0), (10,0)]:
                return True
        if(self.right != None):
            if (i,j) in [(4,19), (10,19)]:
                return True
        return False

    def update(self):
        self.display_hp_boss()
        self.update_phase()
        if self.rect.contains(self.game.player.rect) and self.enemies:
            for entrance in self.entrances:
                entrance.enable = True
            self.open = False
        else:
            for entrance in self.entrances:
                entrance.enable = False
            self.open = True

    def update_phase(self):
        #get num enemy in self.enemies
        num_enemies = len(self.enemies.sprites())

        if(num_enemies == 0 and self.current_phase >= self.max_phase):
            self.clear = True
        if( num_enemies == 0 and self.current_phase < self.max_phase):
            self.current_phase += 1
            #chon 5 vi tri random de tao enemy
            enemies_pos = random.sample(self.available_pos, random.randint(2, 8))
            for pos in enemies_pos:
                enemy = Enemy(self.game, pos[0], pos[1], self.rect.x-32, self.rect.y-32, self)
                self.enemies.add(enemy)

    def update_rect(self):
        #start position of the map including the border
        self.x = self.mappingpos[0] * WIN_WIDTH
        self.y = self.mappingpos[1] * WIN_HEIGHT
        self.rect.topleft = ( 32 + self.mappingpos[0] * WIN_WIDTH, 32 + self.mappingpos[1] * WIN_HEIGHT)
        
    def create_tilemap(self):
        for i, row in enumerate(self.tilemap):
            for j, col in enumerate(row):
                if col == 'B':
                    if(self.checkEntrance(i, j)):
                        sprite = Entrance(self.game, j, i, self.x, self.y)
                        self.entrances.add(sprite)
                    else: Block(self.game, j, i, self.x, self.y)
                    # if self.check_corner(i, j): 
                    #     Torch(self.game, j, i, self.x, self.y)
                if col == 'E':
                    enemy = Enemy(self.game, j, i, self.x, self.y, self)
                    self.enemies.add(enemy)
                if col == 'P':
                    self.game.player = Player(self.game, j, i, self.x, self.y)
                    self.game.player.set_weapons()
                if col == 'E' or col == 'P' or col == '.':
                    self.available_pos.append([j, i])
                if col == '5':
                    boss = Boss(self.game, j, i, self.x, self.y, self)
                    self.enemies.add(boss)
                    self.max_phase = 0
                if(col == ' '): continue
                Ground(self.game, j, i, self.x, self.y)

    def get_boss(self):
        for enemy in self.enemies:
            if isinstance(enemy, Boss):
                return enemy
        return None
    
    def display_hp_boss(self):
        if self.rect.contains(self.game.player.rect) and self.enemies:
            boss = self.get_boss()
            if boss:
                BossHPBar(self.game, boss )
      