import random
from pico2d import *
import gfw
import gobj


class Player:
    KEY_MAP = {
        (SDL_KEYDOWN, SDLK_LEFT):  (-1,  0),
        (SDL_KEYDOWN, SDLK_RIGHT): ( 1,  0),
        (SDL_KEYDOWN, SDLK_DOWN):  ( 0, -1),
        (SDL_KEYDOWN, SDLK_UP):    ( 0,  1),
        (SDL_KEYUP, SDLK_LEFT):    ( 1,  0),
        (SDL_KEYUP, SDLK_RIGHT):   (-1,  0),
        (SDL_KEYUP, SDLK_DOWN):    ( 0,  1),
        (SDL_KEYUP, SDLK_UP):      ( 0, -1),
    }
    KEYDOWN_SPACE  = (SDL_KEYDOWN, SDLK_SPACE)
    KEYDOWN_LSHIFT = (SDL_KEYDOWN, SDLK_LSHIFT)
    KEYUP_LSHIFT   = (SDL_KEYUP,   SDLK_LSHIFT)
    KEYDOWN_E = (SDL_KEYDOWN, SDLK_e)
    image = None

    #constructor
    def __init__(self):
        self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.delta = 0, 0
        self.target = None
        self.speed = 100
        self.image = []
        self.image.append(gfw.image.load(gobj.RES_DIR + '/walk_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/ax_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/gok_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/walk_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/walk_sheet.png'))

        self.ui_image = []
        self.ui_image.append(gfw.image.load(gobj.RES_DIR + '/mainstate_item_ui.png'))
        self.ui_image.append(gfw.image.load(gobj.RES_DIR + '/Cursors.ko-KR.png'))

        self.ui_menu_image = gfw.image.load(gobj.RES_DIR + '/menustate_ui1.png')

        self.item_tool = gfw.image.load(gobj.RES_DIR + '/tools.png')


        self.anim = 0
        self.time = 0
        self.fidx = 0
        self.fmax = 1
        self.action = 2
        self.mag = 1
        self.mirror = False

        self.mouse = False
        self.iven_pos = (573,63)
        self.item = 1

        self.menustate = False

    def drawitemrec(self):
        draw_rectangle(*self.iven_pos, self.iven_pos[0] + 65, self.iven_pos[1] + 70)
        draw_rectangle(self.iven_pos[0] - 1, self.iven_pos[1] - 1, self.iven_pos[0] - 1 + 65, self.iven_pos[1] - 1 + 70)
        draw_rectangle(self.iven_pos[0] + 1, self.iven_pos[1] + 1, self.iven_pos[0] + 1 + 65, self.iven_pos[1] + 1 + 70)

    def draw(self):
        if self.anim < 1:
            width,height = 70,130
        else:
            width, height = 250, 300

        sx = self.fidx * width
        sy = self.action * height
        if self.mirror == True:
            self.image[self.anim].clip_composite_draw(sx, sy, width, height,0,'h', *self.pos,width,height)
        else:
            self.image[self.anim].clip_draw(sx, sy, width, height, * self.pos)

        if self.menustate == False:
            self.ui_image[0].draw(960,100)
            self.ui_image[1].clip_draw(332, 2256 - 432 - 57, 73, 57, 1760, 950, 73 * 4, 57 * 4)

            self.drawitemrec()
        else:
            self.ui_menu_image.draw(960, 540)

    def update(self):
        if self.anim < 1:
            x,y = self.pos
            dx,dy = self.delta
            x += dx * self.speed * self.mag * gfw.delta_time
            y += dy * self.speed * self.mag * gfw.delta_time

            self.pos = x,y

        self.time += gfw.delta_time
        frame = self.time * 15
        if self.anim > 0:
            frame = self.time * 10
        #self.fidx = int(frame) % self.fmax
        self.fidx = (self.fidx + 1) % self.fmax
        if self.anim > 0 and self.fidx == 0:
            self.anim = 0
            self.fmax = 1
            self.fidx = 0
            self.delta = (0, 0)

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP and self.anim < 1 and self.mouse == False:
            pdx = self.delta[0]
            self.delta = gobj.point_add(self.delta, Player.KEY_MAP[pair])
            dx = self.delta[0]
            dy = self.delta[1]
            if dx < 0 and dy != 0:
                self.action = 1
                self.fmax = 6
                self.mirror = True
            elif dx > 0 and dy != 0:
                self.action = 1
                self.fmax = 6
                self.mirror = False
            elif dx > 0:
                self.action = 1
                self.fmax = 6
                self.mirror = False
            elif dx < 0:
                self.action = 1
                self.fmax = 6
                self.mirror = True
            elif dy > 0:
                self.action = 0
                self.fmax = 8
                self.mirror = False
            elif dy < 0:
                self.action = 2
                self.fmax = 8
                self.mirror = False
            else:
                self.fmax = 1
            # print(dx, pdx, self.action)
        elif pair == Player.KEYDOWN_LSHIFT:
            self.mag *= 2
        elif pair == Player.KEYUP_LSHIFT:
            self.mag //= 2
        elif pair == Player.KEYDOWN_E:
            self.menustate = False if self.menustate == True else True

        if e.type == SDL_MOUSEBUTTONDOWN:
            self.mouse = True
            if self.item > 0 and self.anim < 1 and self.fmax == 1:
                self.delta = (0,0)
                self.anim = self.item
                if self.item == 1:
                    if (self.action == 1):
                        self.fidex = 0
                        self.fmax = 4
                    else:
                        self.fidex = 0
                        self.fmax = 5

                elif self.item == 2:
                    if (self.action == 0):
                        self.fidex = 0
                        self.fmax = 4
                    else:
                        self.fidex = 0
                        self.fmax = 5
        elif e.type == SDL_MOUSEBUTTONUP:
            self.mouse = False

    def get_bb(self):
        hw = 20
        hh = 40
        x,y = self.pos
        return x - hw, y - hh, x + hw, y + hh

    def __getstate__(self):
        dict = self.__dict__.copy()
        del dict['image']
        return dict

    def __setstate__(self, dict):
        # self.__init__()
        self.__dict__.update(dict)
        self.image[0] = gfw.image.load(gobj.RES_DIR + '/walk_sheet.png')
        self.image[1] = gfw.image.load(gobj.RES_DIR + '/ax_sheet.png')
        self.image[2] = gfw.image.load(gobj.RES_DIR + '/gok_sheet.png')
        self.image[3] = gfw.image.load(gobj.RES_DIR + '/walk_sheet.png')
        self.image[4] = gfw.image.load(gobj.RES_DIR + '/walk_sheet.png')
