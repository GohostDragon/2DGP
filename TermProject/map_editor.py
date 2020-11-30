import gfw
from pico2d import *

from background import *

import main_state
import gobj

import pickle

import random

canvas_width = main_state.canvas_width
canvas_height = main_state.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2

FARM_XBOARD = 80
FARM_YBOARD = 65

FILE_NAME = 'Shop_Tile.pickle'

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
        self.speed = 300
        self.mag = 1

    def draw(self):
        pass

    def update(self):
        x,y = self.pos
        dx,dy = self.delta
        x += dx * self.speed * self.mag * gfw.delta_time
        y += dy * self.speed * self.mag * gfw.delta_time

        self.pos = x, y

    def handle_event(self, e):
        pair = (e.type, e.key)
        if pair in Player.KEY_MAP:
            self.delta = gobj.point_add(self.delta, Player.KEY_MAP[pair])

        elif pair == Player.KEYDOWN_LSHIFT:
            self.mag *= 2
        elif pair == Player.KEYUP_LSHIFT:
            self.mag //= 2

class Farm_Object:
    def __init__(self):
        self.tile = 0
        self.col = False
        self.pos = (0,0)
        #self.tile_object = gfw.image.load(gobj.RES_DIR + '/object/springobjects.ko-KR.png')

    '''
    def clearobject(self):
        self.tile = 0
        self.col = False

    def setbg(self, bg):
        self.bg = bg
    
    def draw(self):
        if self.tile == 1:
            self.tile_object.clip_draw_to_origin(16 * 3, 16 * 5, 16, 16, self.pos[0], self.pos[1], 68, 82)
        elif self.tile == 2:
            self.tile_object.clip_draw_to_origin(16 * 7, 16 * 19, 16, 16, self.pos[0], self.pos[1], 68, 82)
        elif self.tile == 3:
            self.tile_object.clip_draw_to_origin(16 * 7, 16 * 21, 16, 16, self.pos[0], self.pos[1], 68, 82)

    def get_bb(self):
        hw = 68 // 2
        hh = 82 // 2
        return self.x - hw, self.y - hh, self.x + hw, self.y + hh

    def update(self):
        pass
    '''

def enter():
    gfw.world.init(['bg', 'tile', 'zombie', 'player', 'ui'])
    # Zombie.load_all_images()

    global player, bg, homy, farmtile, tile, data_tile, xicon, tile_object, set_tile
    data_tile = []
    for y in range(FARM_YBOARD):
        data_tile.append([])
        for x in range(FARM_XBOARD):
            data_tile[y].append(Farm_Object())

    try:
        f = open(FILE_NAME, "rb")
        data_tile = pickle.load(f)
        f.close()
    except:
        print("No highscore file")

    farmtile = [[0] * FARM_XBOARD for i in range(FARM_YBOARD)]

    player = Player()
    gfw.world.add(gfw.layer.player, player)

    bg = InBackground('shop.jpg')
    #bg = FixedBackground('farm.jpg')
    # bg = gfw.image.load(gobj.RES_DIR + '/map/home.jpg')

    player.bg = bg
    # bg.set_fixed_pos(100, 100)
    gfw.world.add(gfw.layer.bg, bg)
    bg.target = player

    xicon = gfw.image.load(gobj.RES_DIR + '/x_icon.png')
    tile_object = gfw.image.load(gobj.RES_DIR + '/object/springobjects.ko-KR.png')

    set_tile = 0

def exit():
    pass

def update():
    gfw.world.update()

def draw():
    global bg
    gfw.world.draw()
    for y in range(FARM_YBOARD):
        for x in range(FARM_XBOARD):
            minrec = bg.to_screen((68 * x, 82* (y)))
            maxrec = bg.to_screen((68 * (x+1), 82* (y+1)))
            draw_rectangle(*minrec,*maxrec)

    for y in range(FARM_YBOARD):
        for x in range(FARM_XBOARD):
            if data_tile[y][x].tile != 0:
                pos = bg.to_screen((68 * x, 82 * y))
                if data_tile[y][x].tile == 1:
                    tile_object.clip_draw_to_origin(16 * 3, 16 * 5, 16, 16, *pos, 68, 82)
                elif data_tile[y][x].tile == 2:
                    tile_object.clip_draw_to_origin(16 * 7, 16 * 19, 16, 16, *pos, 68, 82)
                elif data_tile[y][x].tile == 3:
                    tile_object.clip_draw_to_origin(16 * 7, 16 * 21, 16, 16, *pos, 68, 82)
            else:
                if data_tile[y][x].col == True:
                    pos = bg.to_screen((68*x,82*y))
                    xicon.draw_to_origin(*pos,68,82)



def handle_event(e):
    global player, set_tile
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_SPACE:
            f = open(FILE_NAME, "wb")
            pickle.dump(data_tile, f)
            f.close()

        elif e.key == SDLK_a:
            set_tile += 1
            if set_tile > 3:
                set_tile = 0

        if e.key == SDLK_ESCAPE:
            gfw.pop()

    player.handle_event(e)

    if e.type == SDL_MOUSEBUTTONDOWN:
        mouse_pos = bg.translate((e.x, get_canvas_height() - 1 - e.y))
        player_xindex = (int)(mouse_pos[0] // 68)
        player_yindex = (int)(mouse_pos[1] // 82)
        if e.button == SDL_BUTTON_LEFT:
            data_tile[player_yindex][player_xindex].tile = set_tile
            data_tile[player_yindex][player_xindex].pos = (player_xindex, player_yindex)
            data_tile[player_yindex][player_xindex].col = True
        elif e.button == SDL_BUTTON_RIGHT:
            data_tile[player_yindex][player_xindex].tile = 0
            data_tile[player_yindex][player_xindex].pos = (0,0)
            data_tile[player_yindex][player_xindex].col = False

if __name__ == '__main__':
    gfw.run_main()
