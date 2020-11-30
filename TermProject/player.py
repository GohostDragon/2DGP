import random
from pico2d import *
import gfw
import gobj

class Inven:
    def __init__(self):
        self.item = 0
        self.count = 0

    def inputItem(self, item, count):
        self.item = item
        self.count = count

    def useItem(self):
        if self.item not in range(1, 6) and self.count > 0:
            self.count -= 1

        if self.count == 0:
            self.item = 0

    def emptyItem(self):
        if self.count == 0:
            return True
        return False

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

    RUNNING, HOE, PICKAX, AX, POT, NAT = range(6)
    #constructor
    def __init__(self):
        #self.pos = get_canvas_width() // 2, get_canvas_height() // 2

        self.pos = (5000,2000)
        self.pos = get_canvas_width() // 2, get_canvas_height() // 2
        self.delta = (0, 0)
        self.target = None
        self.speed = 100
        self.image = []
        self.image.append(gfw.image.load(gobj.RES_DIR + '/walk_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/geng_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/gok_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/ax_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/mul_sheet.png'))
        self.image.append(gfw.image.load(gobj.RES_DIR + '/nat_sheet.png'))

        self.ui_image = []
        self.ui_image.append(gfw.image.load(gobj.RES_DIR + '/mainstate_item_ui.png'))
        self.ui_image.append(gfw.image.load(gobj.RES_DIR + '/Cursors.ko-KR.png'))

        self.ui_menu_image = gfw.image.load(gobj.RES_DIR + '/menustate_ui1.png')

        self.item_tool = gfw.image.load(gobj.RES_DIR + '/tools.png')
        self.weapon_image = gfw.image.load(gobj.RES_DIR + '/weapons.png')
        self.item_image = gfw.image.load(gobj.RES_DIR + '/object/springobjects.ko-KR.png')

        self.tool_effect_sound = []
        self.tool_effect_sound.append(load_wav(gobj.RES_EF + 'hoeHit.wav'))
        self.tool_effect_sound.append(load_wav(gobj.RES_EF + 'axchop.wav'))

        self.state = Player.RUNNING
        self.time = 0
        self.fidx = 0
        self.fmax = 1
        self.action = 2
        self.mag = 1
        self.mirror = False

        self.iven_pos = (573,63)

        self.font = gfw.font.load(gobj.RES_DIR + '/BMJUA_ttf.ttf', 20)

        self.inven = []
        for y in range(3):
            self.inven.append([])
            for x in range(13):
                self.inven[y].append(Inven())

        for i in range(5):
            self.inven[0][i].inputItem(i + 1, 1)
        self.inven[0][5].inputItem(6, 3)

        self.equip = self.inven[0][0].item
        self.farm_objects = []

        self.mousecap = False
        self.keycap = False

    def drawitemrec(self):
        draw_rectangle(*self.iven_pos, self.iven_pos[0] + 65, self.iven_pos[1] + 70)
        draw_rectangle(self.iven_pos[0] - 1, self.iven_pos[1] - 1, self.iven_pos[0] - 1 + 65, self.iven_pos[1] - 1 + 70)
        draw_rectangle(self.iven_pos[0] + 1, self.iven_pos[1] + 1, self.iven_pos[0] + 1 + 65, self.iven_pos[1] + 1 + 70)

    def draw(self):
        if self.state == Player.RUNNING:
            width,height = 70,130
        else:
            width, height = 250, 300

        sx = self.fidx * width
        sy = self.action * height

        pos = self.bg.to_screen(self.pos)
        if self.mirror == True:
            self.image[self.state].clip_composite_draw(sx, sy, width, height,0,'h', *pos,width,height)
        else:
            self.image[self.state].clip_draw(sx, sy, width, height, *pos)

        if pos[1] < get_canvas_height() // 2 - 200:
            invenui_y = 1000
            self.iven_pos = (self.iven_pos[0], 963)
        else:
            invenui_y = 100
            self.iven_pos = (self.iven_pos[0], 63)

        self.ui_image[0].draw(960,invenui_y)
        self.ui_image[1].clip_draw(332, 2256 - 432 - 57, 73, 57, 1760, 950, 73 * 4, 57 * 4)
        for i in range(13):
            if self.inven[0][i].item == 1:
                self.item_tool.clip_draw(79, 384 - (64 * 0 + 48), 17, 17, 604 + 64 * i, invenui_y, 17 * 4, 17 * 4)
            elif self.inven[0][i].item == 2:
                self.item_tool.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * i, invenui_y, 17 * 4, 17 * 4)
            elif self.inven[0][i].item == 3:
                self.item_tool.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * i, invenui_y, 17 * 4, 17 * 4)
            elif self.inven[0][i].item == 4:
                self.item_tool.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * i, invenui_y, 17 * 4, 17 * 4)
            elif self.inven[0][i].item == 5:
                self.weapon_image.clip_draw(7*16, 16, 16, 16, 604 + 64 * i, invenui_y, 17 * 3, 17 * 3)
            elif self.inven[0][i].item == 6:
                self.item_image.clip_draw(16*16, 16*14, 16, 16, 604 + 64 * i + 5, invenui_y, 17 * 3, 17 * 3)

            if self.inven[0][i].item > 5:
                self.font.draw(604 + 64 * i + 10, invenui_y - 25, str(self.inven[0][i].count), (255, 255, 255))
        self.drawitemrec()
        draw_rectangle(pos[0] - 30, pos[1] - 65, pos[0] + 30, pos[1])

    def get_bb(self):
        #pos = self.bg.to_screen(self.pos)
        return self.dpos[0] - 30, self.dpos[1] - 65, self.dpos[0] + 30, self.dpos[1]

    def update(self):
        if self.state == Player.RUNNING:
            x, y = self.pos
            dx,dy = self.delta
            x += dx * self.speed * self.mag * gfw.delta_time
            y += dy * self.speed * self.mag * gfw.delta_time

            self.dpos = self.bg.to_screen((x,y))

            for cy in range(65):
                for cx in range(80):
                    if self.farm_objects[cy][cx].col == True:
                        if gobj.collides_box(self, self.farm_objects[cy][cx]):
                            x, y = self.pos

            self.pos = x,y

        self.time += gfw.delta_time
        frame = self.time * 15
        if self.state != Player.RUNNING:
            frame = self.time * 10
        #self.fidx = int(frame) % self.fmax
        self.fidx = (self.fidx + 1) % self.fmax
        if self.state != Player.RUNNING and self.fidx == 0:
            self.set_pause()
            if self.equip == 1:
                if self.farm_objects[self.y_tile][self.x_tile].tile == 0 and self.farm_objects[self.y_tile][self.x_tile].col == False:
                    self.farmtile[self.y_tile][self.x_tile] = 1

            elif self.equip == 2:
                if self.farm_objects[self.y_tile][self.x_tile].tile == 2:
                    self.farm_objects[self.y_tile][self.x_tile].tile = 0
                    self.farm_objects[self.y_tile][self.x_tile].col = False

            elif self.equip == 3:
                if self.farm_objects[self.y_tile][self.x_tile].tile == 3:
                    self.farm_objects[self.y_tile][self.x_tile].tile = 0
                    self.farm_objects[self.y_tile][self.x_tile].col = False

            elif self.equip == 4:
                if self.farmtile[self.y_tile][self.x_tile] == 1:
                    self.farmtile[self.y_tile][self.x_tile] = 2

            elif self.equip == 5:
                if self.farm_objects[self.y_tile][self.x_tile].tile == 1:
                    self.farm_objects[self.y_tile][self.x_tile].tile = 0
                    self.farm_objects[self.y_tile][self.x_tile].col = False

    def handle_event(self, e):
        pair = (e.type, e.key)

        if pair in Player.KEY_MAP:
            self.delta = gobj.point_add(self.delta, Player.KEY_MAP[pair])
            if self.state == Player.RUNNING:

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

        elif pair == Player.KEYDOWN_LSHIFT:
            self.mag *= 2
        elif pair == Player.KEYUP_LSHIFT:
            self.mag //= 2
        elif pair == Player.KEYDOWN_E:
            pass
            #self.menustate = False if self.menustate == True else True

        elif pair in Player.KEY_ITEM_MAP:
            self.iven_pos = Player.KEY_ITEM_MAP[pair]
            self.equip = self.inven[0][(self.iven_pos[0]-573) // 64].item

        elif e.type == SDL_MOUSEBUTTONDOWN:
            if self.equip in range(1, 6) and self.state == Player.RUNNING and self.fmax == 1:
                self.equip = self.inven[0][(self.iven_pos[0] - 573) // 64].item
                self.state = self.equip
                self.tool_effect_sound[self.state-1].play()
                player_xindex = (int)(self.pos[0] // 68)
                player_yindex = (int)((self.pos[1] - 20) // 82)

                if self.action == 0:
                    self.x_tile = player_xindex
                    self.y_tile = player_yindex + 1
                elif self.action == 1:
                    if self.mirror == True:
                        self.x_tile = player_xindex - 1
                        self.y_tile = player_yindex
                    else:
                        self.x_tile = player_xindex + 1
                        self.y_tile = player_yindex
                else:
                    self.x_tile = player_xindex
                    self.y_tile = player_yindex - 1

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
                    if self.action == 2:
                        self.fidex = 0
                        self.fmax = 5
                    else:
                        self.fidex = 0
                        self.fmax = 7

                elif self.equip == 5:
                    self.fidex = 0
                    self.fmax = 3

            if self.equip == 6:
                if self.farmtile[self.y_tile][self.x_tile] == 1 or self.farmtile[self.y_tile][self.x_tile] == 2:
                    if self.farm_objects[self.y_tile][self.x_tile].tile == 0:
                        self.farm_objects[self.y_tile][self.x_tile].tile = 4
                        self.farm_objects[self.y_tile][self.x_tile].col = False
                        self.inven[0][(self.iven_pos[0] - 573) // 64].useItem()

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
        self.state = Player.RUNNING
        self.fmax = 1
        self.fidx = 0
        if self.delta[0] < 0 and self.delta[1] != 0:
            self.action = 1
            self.mirror = True
        elif self.delta[0] > 0 and self.delta[1] != 0:
            self.action = 1
            self.mirror = False
        elif self.delta[0] > 0:
            self.action = 1
            self.mirror = False
        elif self.delta[0] < 0:
            self.action = 1
            self.mirror = True
        elif self.delta[1] > 0:
            self.action = 0
            self.mirror = False
        elif self.delta[1] < 0:
            self.action = 2
            self.mirror = False

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
