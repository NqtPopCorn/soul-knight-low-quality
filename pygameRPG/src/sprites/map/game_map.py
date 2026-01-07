import pygame
from config import *
from .game_room import GameRoom
from config import *

class GameMap:
    def __init__(self, tilemaps, game):
        self.maps = []
        self.pipes = []
        self.game = game
        for tilemap in tilemaps:
            self.maps.append(GameRoom(tilemap, game, 2))

        self.maps[0].max_phase = 0
        self.link(self.maps[0], self.maps[1], "right")
        self.link(self.maps[1], self.maps[2], "top")
        self.link(self.maps[1], self.maps[3], "bottom")
        self.link(self.maps[1], self.maps[4], "right")
        self.link(self.maps[4], self.maps[5], "right")

    def draw(self):
        self.DFS_draw(self.maps[0])

    def DFS_draw(self, map):
        map.draw()
        for adj in [map.top, map.bottom, map.left, map.right]:
            if  adj != None and not adj.isDrawn:
                self.DFS_draw(adj)

    def link(self, m1, m2, dir):
        pipe = GameRoom(hpipemap, self.game)
        self.pipes.append(pipe)

        if(dir == "right"):
            pipe.tilemap = hpipemap
            m1.right = pipe
            pipe.right = m2
            m2.left = pipe
            m2.mappingpos = [m1.mappingpos[0] + 2, m1.mappingpos[1]]
            pipe.mappingpos = [m1.mappingpos[0] + 1, m1.mappingpos[1]]
        if(dir == "left"):
            pipe.tilemap = hpipemap
            m1.left = pipe
            pipe.left = m2
            m2.right = pipe
            m2.mappingpos = [m1.mappingpos[0] - 2, m1.mappingpos[1]]
            pipe.mappingpos = [m1.mappingpos[0] - 1, m1.mappingpos[1]]
        if(dir == "top"):
            pipe.tilemap = vpipemap
            m1.top = pipe
            pipe.top = m2
            m2.bottom = pipe
            m2.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] - 2]
            pipe.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] - 1]
        if(dir == "bottom"):
            pipe.tilemap = vpipemap
            m1.bottom = pipe
            pipe.bottom = m2
            m2.top = pipe
            m2.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] + 2]
            pipe.mappingpos = [m1.mappingpos[0], m1.mappingpos[1] + 1]

        m1.update_rect()
        m2.update_rect()
        pipe.update_rect()

    def check_win(self):
        #neu boss chet thi win
        for map in self.maps:
            if map.get_boss() != None:
                return False
        return True
