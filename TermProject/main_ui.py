import random
from pico2d import *
import gfw
import gobj

class Main_UI:
    bullets = []
    trashcan = []
    def __init__(self, right, y):
        # self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.right, self.y = right, y
        self.image = gfw.image.load(gobj.RES_DIR + '/number_24x32.png')
        self.digit_width = self.image.w // 10
        self.reset()

    def reset(self):
        self.money = 0
        self.display = 0

    def draw(self):
        x = self.right
        #money = self.money
        money = self.display
        while money > 0:
            digit = money % 10
            sx = digit * self.digit_width
            # print(type(sx), type(digit), type(self.digit_width))
            x -= self.digit_width
            #self.image.clip_draw(sx, 0, self.digit_width, self.image.h, x, self.y,20,30)
            self.image.clip_draw_to_origin(sx, 0, self.digit_width, self.image.h, x, self.y,18,30)
            money //= 10

    def update(self):
        if self.display < self.money:
            self.display += 9
        else:
            self.display = self.money