import random
from pico2d import *
import gfw
import gobj
from animal import *

canvas_width = 1920
canvas_height = 1080

class animalShop_UI:
    bullets = []
    trashcan = []

    def __init__(self, inven, money, animals):
        self.image = gfw.image.load(gobj.RES_DIR + '/animalshop_ui.png')

        self.selectui_image = gfw.image.load(gobj.RES_DIR + '/animalshop_ui2.png')

        self.font = gfw.font.load(gobj.RES_DIR + '/BMJUA_ttf.ttf', 30)

        self.reset()
        self.inven = inven
        self.animals = animals
        self.capture = False
        self.select = 0

        self.selectui = 0

        self.money = money
        self.mouse_pos = (0, 0)
    def reset(self):
        pass

    def draw(self):
        self.image.draw(960, 540)
        if 705 <= self.mouse_pos[0] <= 807 and 464 <= self.mouse_pos[1] <= 525:
            self.selectui_image.draw(960, 200)
            self.font.draw(795, 250, '닭', (0,0,0))
            self.font.draw(889, 155, '800', (0, 0, 0))

        elif 868 <= self.mouse_pos[0] <= 943 and 464 <= self.mouse_pos[1] <= 525:
            self.selectui_image.draw(960, 200)
            self.font.draw(795, 250, '소', (0, 0, 0))
            self.font.draw(889, 155, '1500', (0, 0, 0))

        elif 1022 <= self.mouse_pos[0] <= 1096 and 464 <= self.mouse_pos[1] <= 525:
            self.selectui_image.draw(960, 200)
            self.font.draw(795, 250, '먹이', (0, 0, 0))
            self.font.draw(889, 155, '30', (0, 0, 0))

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

            if 1191 <= self.mouse_pos[0] <= 1245 and 331 <= self.mouse_pos[1] <= 381:
                return gfw.pop()

            elif 705 <= self.mouse_pos[0] <= 807 and 464 <= self.mouse_pos[1] <= 525:
                price = 800
                if self.money >= price:
                    self.money -= price
                    self.animals.append(Chicken((canvas_width//2, canvas_height//2)))

            elif 868 <= self.mouse_pos[0] <= 943 and 464 <= self.mouse_pos[1] <= 525:
                price = 1500
                if self.money >= price:
                    self.money -= price
                    self.animals.append(Cow((canvas_width // 2, canvas_height // 2)))

            elif 1022 <= self.mouse_pos[0] <= 1096 and 464 <= self.mouse_pos[1] <= 525:
                price = 30
                if self.money >= price:
                    self.money -= price
                    ix, iy = self.seekinven(14)
                    self.inven[iy][ix].giveItem(14, 1)

        elif e.type == SDL_MOUSEMOTION:
            self.mouse_pos = (e.x, get_canvas_height() - 1 - e.y)



    def update(self):
        pass