import random
from pico2d import *
import gfw
import gobj

class Chicken:
    bullets = []
    trashcan = []

    def __init__(self, pos):
        self.name = 'chicken'
        self.pos = pos
        self.image = gfw.image.load(gobj.RES_DIR + '/White Chicken.png')
        self.fidx = 0
        self.fmax = 4
        self.feed = False
        self.product = True

    def reset(self):
        pass

    def draw(self):
        sx = self.fidx * 16

        self.image.clip_draw(sx, 0, 16, 16, *self.pos, 16*4, 16*4)
        #draw_rectangle(*self.get_bb())

    def handle_event(self, e):
        pass

    def update(self):
        self.fidx = (self.fidx + 1) % self.fmax

    def get_bb(self):
        return self.pos[0] - 16*2, self.pos[1] - 16*2, self.pos[0] + 16*2, self.pos[1] + 16*2

class Cow:
    bullets = []
    trashcan = []

    def __init__(self, pos):
        self.name = 'cow'
        self.pos = pos
        self.image = gfw.image.load(gobj.RES_DIR + '/White Cow.png')
        self.fidx = 0
        self.fmax = 4
        self.feed = False
        self.product = True

    def reset(self):
        pass

    def draw(self):
        sx = self.fidx * 32

        self.image.clip_draw(sx, 0, 32, 32, *self.pos, 4*32, 4*32)
        #draw_rectangle(*self.get_bb())

    def handle_event(self, e):
        pass

    def update(self):
        self.fidx = (self.fidx + 1) % self.fmax

    def get_bb(self):
        return self.pos[0] - 40, self.pos[1] - 32*2, self.pos[0] + 40, self.pos[1] + 40