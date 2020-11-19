import random
from pico2d import *
import gfw
import gobj

class Menu_UI:
    bullets = []
    trashcan = []

    def __init__(self, inven):
        self.image = gfw.image.load(gobj.RES_DIR + '/menustate_ui1.png')

        self.item_tool.append(gfw.image.load(gobj.RES_DIR + '/tools.png'))
        self.reset()
        self.inven = inven

    def reset(self):
        pass

    def draw(self):
        self.image.draw(960, 540)

    def update(self):
        pass