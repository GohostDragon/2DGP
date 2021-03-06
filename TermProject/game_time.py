import random
from pico2d import *
import gfw
import gobj

'''
    font = gfw.font.load(gobj.RES_DIR + '/BMJUA_ttf.ttf', 35)
    week = ['월', '화', '수', '목', '금', '토', '일']
    game_week = 5
    game_day = 30
    game_time = [7, 0]

    game_timer = 0
'''

class Game_Time:
    bullets = []
    trashcan = []

    def __init__(self):
        self.font = gfw.font.load(gobj.RES_DIR + '/BMJUA_ttf.ttf', 35)
        self.week = ['월', '화', '수', '목', '금', '토', '일']
        self.game_week = 0
        self.game_day = 1
        self.game_time = [7, 0]

        self.game_timer = 0
        self.reset()

    def reset(self):
        pass

    def draw(self):
        self.font.draw(1760, get_canvas_height() - 50, self.week[self.game_week] + '. ' + str(self.game_day) + '일', (24, 10, 31))
        if self.game_time[0] < 21:
            self.font.draw(1735, get_canvas_height() - 142, str(self.game_time[0]).zfill(2) + ':' + str(self.game_time[1]).zfill(2) + 'am',(24, 10, 31))
        else:
            self.font.draw(1735, get_canvas_height() - 142, str(self.game_time[0]).zfill(2) + ':' + str(self.game_time[1]).zfill(2) + 'am', (255, 0, 0))
    def nextday(self):
        self.game_day += 1
        if self.game_day > 28:
            self.game_day = 1

        self.game_week = self.game_day % 7 - 1
        self.game_time = [7, 0]
        self.game_timer = 0


    def update(self):
        if self.game_timer < 60:
            self.game_timer += 1
        else:
            self.game_time[1] += 10
            self.game_timer = 0

        if self.game_time[1] >= 60:
            self.game_time[0] += 1
            self.game_time[1] = 0