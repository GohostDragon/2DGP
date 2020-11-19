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

    KEY_ITEM_MAP = {
        (SDL_KEYDOWN, SDLK_1): (573,63),
        (SDL_KEYDOWN, SDLK_2): (573+64,63),
        (SDL_KEYDOWN, SDLK_3): (573+64*2,63),
        (SDL_KEYDOWN, SDLK_4): (573+64*3,63),
        (SDL_KEYDOWN, SDLK_5): (573+64*4, 63),
        (SDL_KEYDOWN, SDLK_6): (573 + 64*5, 63),
        (SDL_KEYDOWN, SDLK_7): (573 + 64 * 6, 63),
        (SDL_KEYDOWN, SDLK_8): (573 + 64 * 7, 63),
        (SDL_KEYDOWN, SDLK_9): (573 + 64 * 8, 63),
        (SDL_KEYDOWN, SDLK_0): (573 + 64 * 9, 63),
        (SDL_KEYDOWN, SDLK_MINUS): (573 + 64 * 10, 63),
        (SDL_KEYDOWN, SDLK_EQUALS): (573 + 64 * 11, 63),
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
        self.image.append(gfw.image.load(gobj.RES_DIR + '/geng_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/gok_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/ax_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/walk_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/walk_sheet.png'))

        self.ui_image = []
        self.ui_image.append(gfw.image.load(gobj.RES_DIR + '/mainstate_item_ui.png'))
        self.ui_image.append(gfw.image.load(gobj.RES_DIR + '/Cursors.ko-KR.png'))

        self.ui_menu_image = gfw.image.load(gobj.RES_DIR + '/menustate_ui1.png')

        self.item_tool = []
        self.item_tool.append(gfw.image.load(gobj.RES_DIR + '/tools.png'))
        self.item_tool.append(gfw.image.load(gobj.RES_DIR + '/tools.png'))
        self.item_tool.append(gfw.image.load(gobj.RES_DIR + '/tools.png'))
        self.item_tool.append(gfw.image.load(gobj.RES_DIR + '/tools.png'))

        self.anim = 0
        self.time = 0
        self.fidx = 0
        self.fmax = 1
        self.action = 2
        self.mag = 1
        self.mirror = False

        self.iven_pos = (573,63)

        self.inven = [[0] * 13 for i in range(3)]

        self.inven[0][0] = 1
        self.inven[0][1] = 2
        self.inven[0][2] = 3
        self.inven[0][3] = 4

        self.equip = self.inven[0][0]

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

        pos = self.bg.to_screen(self.pos)
        if self.mirror == True:
            self.image[self.anim].clip_composite_draw(sx, sy, width, height,0,'h', *pos,width,height)
        else:
            self.image[self.anim].clip_draw(sx, sy, width, height, *pos)

        if self.menustate == False:
            self.ui_image[0].draw(960,100)
            self.ui_image[1].clip_draw(332, 2256 - 432 - 57, 73, 57, 1760, 950, 73 * 4, 57 * 4)

            self.item_tool[0].clip_draw(79, 384 - (64 * 0 + 48), 17, 17, 604 + 64 * 0, 100, 17 * 4, 17 * 4)
            self.item_tool[1].clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * 1, 100, 17 * 4, 17 * 4)
            self.item_tool[2].clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * 2, 100, 17 * 4, 17 * 4)
            self.item_tool[3].clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * 3, 100, 17 * 4, 17 * 4)

            self.drawitemrec()
        else:
            self.ui_menu_image.draw(960, 540)

            self.item_tool[0].clip_draw(79, 384 - (48 + 64 * 0), 17, 17, 604 + 64 * 0, 760, 17 * 4, 17 * 4)
            self.item_tool[1].clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * 1, 760, 17 * 4, 17 * 4)
            self.item_tool[2].clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * 2, 760, 17 * 4, 17 * 4)
            self.item_tool[3].clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * 3, 760, 17 * 4, 17 * 4)

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
            self.set_pause()

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP and self.anim < 1:
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
            pass
            #self.menustate = False if self.menustate == True else True

        elif pair in Player.KEY_ITEM_MAP:
            self.iven_pos = Player.KEY_ITEM_MAP[pair]
            self.equip = self.inven[0][(self.iven_pos[0]-573) // 64]


        elif e.type == SDL_MOUSEBUTTONDOWN:
            if self.equip > 0 and self.anim < 1 and self.fmax == 1:
                self.delta = (0,0)
                self.anim = self.equip
                if self.equip == 1:
                    if self.action == 1:
                        self.fidex = 0
                        self.fmax = 4
                    else:
                        self.fidex = 0
                        self.fmax = 5

                elif self.equip == 2:
                    if self.action == 0:
                        self.fidex = 0
                        self.fmax = 4
                    else:
                        self.fidex = 0
                        self.fmax = 5

                elif self.equip == 3:
                    if self.action == 1:
                        self.fidex = 0
                        self.fmax = 4
                    else:
                        self.fidex = 0
                        self.fmax = 5

                elif self.equip == 4:
                    if self.action == 1:
                        self.fidex = 0
                        self.fmax = 4
                    else:
                        self.fidex = 0
                        self.fmax = 5

        elif e.type == SDL_MOUSEBUTTONUP:
            pass

        elif e.type == SDL_MOUSEWHEEL:
            print('mouse wheel')
            if e.wheel.y > 0:
                if self.iven_pos[0] == 573 + 64 * 11:
                    self.iven_pos[0] = 573
                else:
                    self.iven_pos[0] += 64
            elif e.wheel.y < 0:
                if self.iven_pos[0] == 573:
                    self.iven_pos[0] = 573 + 64 * 11
                else:
                    self.iven_pos[0] -= 64
    def set_pause(self):
        self.anim = 0
        self.fmax = 1
        self.fidx = 0
        self.delta = (0, 0)

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
