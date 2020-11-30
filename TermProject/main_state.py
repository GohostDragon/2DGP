import os.path
import gfw
from pico2d import *
from player import Player
from zombie import Zombie
import gobj

from background import *
from main_ui import Main_UI
from game_time import Game_Time

import menu_state
import pickle

canvas_width = 1920
canvas_height = 1080

SAVE_FILENAME = 'zombies.pickle'

FARM_XBOARD = 80
FARM_YBOARD = 65

class Map_Tile:
    def __init__(self):
        self.hoedirt = gfw.image.load(gobj.RES_DIR + '/hoeDirt.png')

    def reset(self):
        pass

    def draw(self):
        for y in range(FARM_YBOARD):
            for x in range(FARM_XBOARD):
                hompos = bg.to_screen((68 * x, 82 * y))
                if farmtile[y][x] == 1:
                    self.hoedirt.clip_draw_to_origin(0, 64 - 16, 16, 16, *hompos,68,82)
                elif farmtile[y][x] == 2:
                    self.hoedirt.clip_draw_to_origin(16*4, 64 - 16, 16, 16, *hompos, 68, 82)

    def update(self):
        pass

class Farm_Object:
    def __init__(self):
        self.tile = 0
        self.col = False
        self.pos = (0,0)

class Tile_Object:
    def __init__(self,obj,bg):
        self.tile = obj.tile
        self.col = obj.col
        self.pos = obj.pos
        self.bg = bg
        self.bgpos = bg.to_screen((68 * self.pos[0], 82 * self.pos[1]))
        self.tile_object = gfw.image.load(gobj.RES_DIR + '/object/springobjects.ko-KR.png')
        self.crop_object = gfw.image.load(gobj.RES_DIR + '/object/crops.png')

    def deleteobject(self):
        self.tile = 0
        self.col = False

    def draw(self):
        if self.tile == 1:
            self.tile_object.clip_draw_to_origin(16 * 3, 16 * 5, 16, 16, *self.bgpos, 68, 82)
        elif self.tile == 2:
            self.tile_object.clip_draw_to_origin(16 * 7, 16 * 19, 16, 16, *self.bgpos, 68, 82)
        elif self.tile == 3:
            self.tile_object.clip_draw_to_origin(16 * 7, 16 * 21, 16, 16, *self.bgpos, 68, 82)
        elif self.tile == 4:
            self.crop_object.clip_draw_to_origin(1, 672-33, 16, 16, *self.bgpos, 68, 82)

    def get_bb(self):
        return self.bgpos[0], self.bgpos[1], self.bgpos[0] + 68, self.bgpos[1] + 82

    def update(self):
        self.bgpos = bg.to_screen((68 * self.pos[0], 82 * self.pos[1]))

def start():
    menu_state.inven = player.inven
    gfw.push(menu_state)

def enter():
    gfw.world.init(['bg','tile', 'object', 'player','ui'])
    #Zombie.load_all_images()

    global player,bg ,homy, farmtile, tile, bg_tile, tile_object

    farmtile = [[0] * FARM_XBOARD for i in range(FARM_YBOARD)]

    player = Player()
    gfw.world.add(gfw.layer.player, player)
    #player.coltile = coltile

    tile = Map_Tile()
    gfw.world.add(gfw.layer.tile, tile)

    # bg = gobj.ImageObject('town.jpg', (canvas_width // 2, canvas_height // 2))
    # gfw.world.add(gfw.layer.bg, bg)
    #bg = Background('town.png')
    bg = FixedBackground('farm.jpg')
    bg = FixedBackground('town.jpg')
    bg = InBackground('home.jpg')
    bg = InBackground('shop.jpg')
    #bg = gfw.image.load(gobj.RES_DIR + '/map/home.jpg')

    #bg = FixedBackground('town.jpg')
    #bg = FixedBackground('farm.jpg')
    player.bg = bg
    gfw.world.add(gfw.layer.bg, bg)
    bg.target = player
    '''
    try:
        f = open('Farm_Tile.pickle', "rb")
        data_object = pickle.load(f)
        f.close()
    except:
        print("No Map file")

    farm_objects = []
    for y in range(FARM_YBOARD):
        farm_objects.append([])
        for x in range(FARM_XBOARD):
            farm_objects[y].append(Farm_Manage_Object(data_object[y][x], bg))

    for y in range(FARM_YBOARD):
        for x in range(FARM_XBOARD):
            farm_objects[y][x].pos = (x, y)
            gfw.world.add(gfw.layer.object, farm_objects[y][x])
    '''
    try:
        f = open('Shop_Tile.pickle', "rb")
        data_object = pickle.load(f)
        f.close()
    except:
        print("No Map file")

    bg_tile = []
    for y in range(FARM_YBOARD):
        bg_tile.append([])
        for x in range(FARM_XBOARD):
            bg_tile[y].append(Tile_Object(data_object[y][x], bg))

    for y in range(FARM_YBOARD):
        for x in range(FARM_XBOARD):
            bg_tile[y][x].pos = (x, y)

    #player.farm_objects = farm_objects
    player.farm_objects = bg_tile

    global main_ui
    main_ui = Main_UI(canvas_width - 40, canvas_height - 230)
    main_ui.money = 500
    gfw.world.add(gfw.layer.ui, main_ui)

    global game_time
    game_time = Game_Time()
    gfw.world.add(gfw.layer.ui, game_time)

    homy = gfw.image.load(gobj.RES_DIR + '/hoeDirt.png')

def load():
    if not os.path.isfile(SAVE_FILENAME):
        return False

    gfw.world.load(SAVE_FILENAME)
    print('Loaded from:', SAVE_FILENAME)
    return True

def update():
    gfw.world.update()

def draw():
    global bg,homy
    gfw.world.draw()

    for y in range(FARM_YBOARD):
        for x in range(FARM_XBOARD):
            minrec = bg.to_screen((68 * x, 82* (y)))
            maxrec = bg.to_screen((68 * (x+1), 82* (y+1)))
            draw_rectangle(*minrec,*maxrec)

    # gobj.draw_collision_box()
    
def handle_event(e):
    global player, farmtile, bg_tile
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
        elif e.key == SDLK_e:
            player.set_pause()
            start()

    player.farmtile = farmtile
    player.farm_objects = bg_tile
    player.handle_event(e)
    farmtile = player.farmtile
    farm_objects = player.farm_objects

def resume():
    global player
    player.inven = menu_state.inven

def pause():
    pass

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
