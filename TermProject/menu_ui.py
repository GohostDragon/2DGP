import random
from pico2d import *
import gfw
import gobj

class Menu_UI:
    bullets = []
    trashcan = []

    def __init__(self, inven):
        self.image = gfw.image.load(gobj.RES_DIR + '/menustate_ui1.png')

        self.item_tool = gfw.image.load(gobj.RES_DIR + '/tools.png')
        self.reset()
        self.inven = inven
        self.capture = False
        self.select = 0

    def reset(self):
        pass

    def draw(self):
        self.image.draw(960, 540)
        for y in range(3):
            for x in range(12):
                if y == 0:
                    posy = 760
                elif y == 1:
                    posy = 680
                else:
                    posy = 614

                if self.inven[y][x] == 1:
                    self.item_tool.clip_draw(79, 384 - (64 * 0 + 48), 17, 17, 604 + 64 * x, posy, 17 * 4, 17 * 4)
                elif self.inven[y][x] == 2:
                    self.item_tool.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * x, posy, 17 * 4, 17 * 4)
                elif self.inven[y][x] == 3:
                    self.item_tool.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * x, posy, 17 * 4, 17 * 4)
                elif self.inven[y][x] == 4:
                    self.item_tool.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * x, posy, 17 * 4, 17 * 4)

        if self.capture:
            if self.select == 1:
                self.item_tool.clip_draw(79, 384 - (64 * 0 + 48), 17, 17, *self.mouse_pos, 17 * 4, 17 * 4)
            elif self.select == 2:
                self.item_tool.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, *self.mouse_pos, 17 * 4, 17 * 4)
            elif self.select == 3:
                self.item_tool.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, *self.mouse_pos, 17 * 4, 17 * 4)
            elif self.select == 4:
                self.item_tool.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, *self.mouse_pos, 17 * 4, 17 * 4)


    def handle_event(self, e):
        if e.type == SDL_MOUSEBUTTONDOWN:
            self.mouse_pos = (e.x, get_canvas_height() - 1 - e.y)
            if self.capture == False:
                for y in range(3):
                    for x in range(12):
                        if y == 0:
                            posy = 760
                        elif y == 1:
                            posy = 680
                        else:
                            posy = 614
                        if 570 + x * 17 *4 < self.mouse_pos[0] < 570 + (x+1) * 17 *4 and posy - 34 < self.mouse_pos[1] < posy - 34 + 17 * 4:
                            self.capture = True
                            self.select = self.inven[y][x]
                            self.inven[y][x] = 0
                            self.selectposx = x
                            self.selectposy = y

            else:
                self.inven[self.selectposy][self.selectposx] = self.select
                for y in range(3):
                    for x in range(12):
                        if y == 0:
                            posy = 760
                        elif y == 1:
                            posy = 680
                        else:
                            posy = 614
                        if 570 + x * 17 *4 < self.mouse_pos[0] < 570 + (x+1) * 17 *4 and posy - 34 < self.mouse_pos[1] < posy - 34 + 17 * 4:
                            self.inven[y][x], self.inven[self.selectposy][self.selectposx] = self.inven[self.selectposy][self.selectposx], self.inven[y][x]

                self.capture = False
                self.select = 0

        elif e.type == SDL_MOUSEMOTION:
            if self.capture == True:
                self.mouse_pos = (e.x, get_canvas_height() - 1 - e.y)


    def update(self):
        pass