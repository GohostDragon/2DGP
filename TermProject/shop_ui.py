import random
from pico2d import *
import gfw
import gobj

class Shop_UI:
    bullets = []
    trashcan = []

    def __init__(self, inven, money):
        self.image = gfw.image.load(gobj.RES_DIR + '/shop_ui.png')

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

        self.money = money

    def reset(self):
        pass

    def draw(self):
        if self.selectui == 0:
            self.image.draw(960, 540)

        if self.selectui == 0:
            for y in range(3):
                for x in range(12):
                    if y == 0:
                        posy = 346
                    elif y == 1:
                        posy = 264
                    else:
                        posy = 196

                    if self.inven[y][x].item == 1:
                        self.item_tool.clip_draw(79, 384 - (64 * 0 + 48), 17, 17, 964 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 2:
                        self.item_tool.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 964 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 3:
                        self.item_tool.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 964 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 4:
                        self.item_tool.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 964 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 5:
                        self.item_weapon.clip_draw(7*16, 16, 16, 16, 964 + 64 * x, posy, 17 * 4, 17 * 4)
                    elif self.inven[y][x].item == 6:
                        self.item_image.clip_draw(16 * 16, 16 * 14, 16, 16, 964 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 7:
                        self.item_image.clip_draw(16 * 17, 16 * 14, 16, 16, 964 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 8:
                        self.item_image.clip_draw(16 * 18, 16 * 14, 16, 16, 964 + 64 * x, posy, 17 * 3, 17 * 3)
                    elif self.inven[y][x].item == 9:
                        self.item_image.clip_draw(16 * 19, 16 * 14, 16, 16, 964 + 64 * x, posy, 17 * 3, 17 * 3)

                    if self.inven[y][x].item > 5:
                        self.font.draw(964 + 64 * x + 10, posy - 25, str(self.inven[y][x].count), (255, 255, 255))

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

    def seekinven(self, item):
        for y in range(3):
            for x in range(12):
                if self.inven[y][x].item == item:
                    return x,y

        for y in range(3):
            for x in range(12):
                if self.inven[y][x].item == 0:
                    return x,y

    def handle_event(self, e):
        if e.type == SDL_MOUSEBUTTONDOWN:
            self.mouse_pos = (e.x, get_canvas_height() - 1 - e.y)
            print(self.mouse_pos)

            for y in range(3):
                for x in range(12):
                    if y == 0:
                        posy = 346
                    elif y == 1:
                        posy = 264
                    else:
                        posy = 196
                    if 930 + 17 * 4 * x < self.mouse_pos[0] < 930 + 17 * 4 * (x+1) and posy - 34 < self.mouse_pos[
                        1] < posy - 34 + 17 * 4:
                        #self.inven[y][x].item = 0
                        print(self.inven[y][x].item)
                        self.selectposx = x
                        self.selectposy = y

            for y in range(4):
                if 700 < self.mouse_pos[0] < 1720 and 768-108*y < self.mouse_pos[
                    1] < 849-108*y:
                    if y == 0:
                        price = 20
                        if self.money >= price:
                            self.money -= price
                            ix, iy = self.seekinven(6)
                            self.inven[iy][ix].giveItem(6, 1)
                    elif y == 1:
                        price = 60
                        if self.money >= price:
                            self.money -= price
                            ix, iy = self.seekinven(7)
                            self.inven[iy][ix].giveItem(7, 1)
                    elif y == 2:
                        price = 80
                        if self.money >= price:
                            self.money -= price
                            ix, iy = self.seekinven(8)
                            self.inven[iy][ix].giveItem(8, 1)
                    elif y == 3:
                        price = 50
                        if self.money >= price:
                            self.money -= price
                            ix, iy = self.seekinven(9)
                            self.inven[iy][ix].giveItem(9, 1)



    def update(self):
        pass