import random
from pico2d import *
import gfw
import gobj

class Menu_UI:
    bullets = []
    trashcan = []

    def __init__(self, inven):
        self.image = gfw.image.load(gobj.RES_DIR + '/menustate_ui1.png')

        self.selectui_image = gfw.image.load(gobj.RES_DIR + '/Cursors.ko-KR.png')

        self.item_tool = gfw.image.load(gobj.RES_DIR + '/tools.png')
        self.item_weapon = gfw.image.load(gobj.RES_DIR + '/weapons.png')
        self.item_image = gfw.image.load(gobj.RES_DIR + '/object/springobjects.ko-KR.png')

        self.font = gfw.font.load(gobj.RES_DIR + '/BMJUA_ttf.ttf', 20)

        self.reset()
        self.inven = inven
        self.capture = False
        self.select = 0

        self.selectui = 0

    def reset(self):
        pass

    def draw(self):
        if self.selectui == 0:
            self.image.draw(960, 540)

        for i in range(3):
            if i == self.selectui:
                self.selectui_image.clip_draw(i*16, 2256 - 383, 16, 16, 600+(i*16*4), 850, 16 * 4, 16 * 4)
            else:
                self.selectui_image.clip_draw(i*16, 2256 - 383, 16, 16, 600+(i*16*4), 800 + 16 * 4, 16 * 4, 16 * 4)

        if self.selectui == 0:
            for y in range(3):
                for x in range(12):
                    if y == 0:
                        posy = 760
                    elif y == 1:
                        posy = 680
                    else:
                        posy = 614

                    if self.inven[y][x].item == 1:
                        self.item_tool.clip_draw(79, 384 - (64 * 0 + 48), 17, 17, 604 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 2:
                        self.item_tool.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 3:
                        self.item_tool.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 4:
                        self.item_tool.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 5:
                        self.item_weapon.clip_draw(7*16, 16, 16, 16, 604 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 6:
                        self.item_image.clip_draw(16 * 16, 16 * 14, 16, 16, 604 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 7:
                        self.item_image.clip_draw(16 * 17, 16 * 14, 16, 16, 604 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 8:
                        self.item_image.clip_draw(16 * 18, 16 * 14, 16, 16, 604 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 9:
                        self.item_image.clip_draw(16 * 19, 16 * 14, 16, 16, 604 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 10:
                        self.item_image.clip_draw(16 * 0, 16 * 32, 16, 16, 604 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 11:
                        self.item_image.clip_draw(16 * 10, 16 * 23, 16, 16, 604 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 12:
                        self.item_image.clip_draw(16 * 22, 16 * 26, 16, 16, 604 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 13:
                        self.item_image.clip_draw(16 * 0, 16 * 25, 16, 16, 604 + 64 * x, posy, 17 * 3, 17 * 3)

                    if self.inven[y][x].item > 5:
                        self.font.draw(604 + 64 * x + 10, posy - 25, str(self.inven[y][x].count), (255, 255, 255))

            if self.capture:
                if self.select == 1:
                    self.item_tool.clip_draw(79, 384 - (64 * 0 + 48), 17, 17, *self.mouse_pos, 17 * 4, 17 * 4)
                elif self.select == 2:
                    self.item_tool.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, *self.mouse_pos, 17 * 4, 17 * 4)
                elif self.select == 3:
                    self.item_tool.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, *self.mouse_pos, 17 * 4, 17 * 4)
                elif self.select == 4:
                    self.item_tool.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, *self.mouse_pos, 17 * 4, 17 * 4)
                elif self.select == 5:
                    self.item_weapon.clip_draw(7 * 16, 16, 16, 16, *self.mouse_pos, 17 * 4, 17 * 4)
                elif self.select == 6:
                    self.item_image.clip_draw(16 * 16, 16 * 14, 16, 16, *self.mouse_pos, 17 * 3, 17 * 3)
                elif self.select == 7:
                    self.item_image.clip_draw(16 * 17, 16 * 14, 16, 16, *self.mouse_pos, 17 * 3, 17 * 3)
                elif self.select == 8:
                    self.item_image.clip_draw(16 * 18, 16 * 14, 16, 16, *self.mouse_pos, 17 * 3, 17 * 3)
                elif self.select == 9:
                    self.item_image.clip_draw(16 * 19, 16 * 14, 16, 16, *self.mouse_pos, 17 * 3, 17 * 3)
                elif self.select == 10:
                    self.item_image.clip_draw(16 * 0, 16 * 32, 16, 16, *self.mouse_pos, 17 * 3, 17 * 3)
                elif self.select == 11:
                    self.item_image.clip_draw(16 * 10, 16 * 23, 16, 16, *self.mouse_pos, 17 * 3, 17 * 3)
                elif self.select == 12:
                    self.item_image.clip_draw(16 * 22, 16 * 26, 16, 16, *self.mouse_pos, 17 * 3, 17 * 3)
                elif self.select == 13:
                    self.item_image.clip_draw(16 * 0, 16 * 25, 16, 16, *self.mouse_pos, 17 * 3, 17 * 3)


    def handle_event(self, e):
        if e.type == SDL_MOUSEBUTTONDOWN:
            self.mouse_pos = (e.x, get_canvas_height() - 1 - e.y)

            for i in range(3):
                if i != self.selectui:
                    if 600 + (i * 16 * 4) - 16 * 2< self.mouse_pos[0] < 600 + (i * 16 * 4) + 16 * 4 and 850 - 16*2< self.mouse_pos[1]  < 850 - 16*2 +16*4:
                        self.selectui = i


            if self.selectui == 0:
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
                                self.select = self.inven[y][x].item
                                self.inven[y][x].item = 0
                                self.selectposx = x
                                self.selectposy = y

                else:
                    self.inven[self.selectposy][self.selectposx].item = self.select
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