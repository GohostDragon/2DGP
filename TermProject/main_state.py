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
import shop_state
import pickle

canvas_width = 1920
canvas_height = 1080

SAVE_FILENAME = 'zombies.pickle'

#FARM_XBOARD = 80
#FARM_YBOARD = 65
FARM_XBOARD = 80
FARM_YBOARD = 65

HOME, FARM, TOWN, SHOP = range(4)
MENU_STATE, SHOP_STATE = range(2)

whostate = 0

class Portal:
    def __init__(self, pos, nextmap, nextpos, key):
        self.pos = pos
        self.nextmap = nextmap
        self.nextpos = nextpos
        self.key = key

class Map:
    def __init__(self, bg, data):
        self.bg = bg
        self.portal = []

        self.data = data

    def addPortal(self, pos, nextmap, nextpos, key):
        self.portal.append(Portal(pos, nextmap, nextpos, key))

    def setTile(self, tile):
        self.tile = tile

    def setObject(self,objects):
        self.objcts = objects

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

def mapchange(map, pos):
    global current_map, player, bg, bg_tile

    gfw.world.clear_at(gfw.layer.object)


    current_map = map
    player.pos = pos

    gfw.world.remove(bg)
    bg = worldmap[current_map].bg

    f = open(worldmap[current_map].data, "rb")
    data_object = pickle.load(f)
    f.close()

    bg_tile = []
    for y in range(FARM_YBOARD):
        bg_tile.append([])
        for x in range(FARM_XBOARD):
            bg_tile[y].append(Tile_Object(data_object[y][x], bg))

    for y in range(FARM_YBOARD):
        for x in range(FARM_XBOARD):
            bg_tile[y][x].pos = (x, y)
            gfw.world.add(gfw.layer.object, bg_tile[y][x])

    player.farm_objects = bg_tile
    player.current_map = current_map
    player.bg = bg
    bg.target = player
    gfw.world.add(gfw.layer.bg, bg)

def start():
    global whostate
    menu_state.inven = player.inven
    whostate = MENU_STATE
    gfw.push(menu_state)

def shpstatchange():
    global whostate, main_ui
    shop_state.inven = player.inven
    shop_state.money = main_ui.money
    whostate = SHOP_STATE
    gfw.push(shop_state)

def enter():
    gfw.world.init(['bg','tile', 'object', 'player','ui'])
    #Zombie.load_all_images()

    global player,bg ,homy, farmtile, tile, bg_tile, tile_object, bg_music, current_map, worldmap

    worldmap = []
    worldmap.append(Map(InBackground('home.jpg'),'Home_Tile.pickle'))
    worldmap.append(Map(FixedBackground('farm.jpg'), 'Farm_Tile.pickle'))
    worldmap.append(Map(FixedBackground('town.jpg'), 'Town_Tile.pickle'))
    worldmap.append(Map(InBackground('shop.jpg'),'Shop_Tile.pickle'))

    worldmap[HOME].addPortal((11, 2), FARM, (4328.08, 3441.80), SDLK_DOWN)
    worldmap[FARM].addPortal((63, 41), HOME, (784.05, 249.96), SDLK_UP)
    worldmap[FARM].addPortal((78, 39), TOWN, (45.29, 4495.97), SDLK_RIGHT)
    worldmap[FARM].addPortal((78, 40), TOWN, (45.29, 4584.28), SDLK_RIGHT)
    worldmap[FARM].addPortal((78, 41), TOWN, (45.29, 4672.76), SDLK_RIGHT)

    worldmap[TOWN].addPortal((0, 54), FARM, (5337.16, 3280.91), SDLK_LEFT)
    worldmap[TOWN].addPortal((0, 55), FARM, (5337.16, 3360.38), SDLK_LEFT)
    worldmap[TOWN].addPortal((0, 56), FARM, (5337.16, 3443.38), SDLK_LEFT)

    worldmap[TOWN].addPortal((43, 52), SHOP, (842.17, 253.06), SDLK_UP)
    worldmap[TOWN].addPortal((44, 52), SHOP, (842.17, 253.06), SDLK_UP)

    worldmap[SHOP].addPortal((12, 2), SHOP, (2947.63, 4345.54), SDLK_DOWN)


    current_map = HOME

    bg = worldmap[current_map].bg

    farmtile = [[0] * FARM_XBOARD for i in range(FARM_YBOARD)]

    player = Player()
    gfw.world.add(gfw.layer.player, player)

    tile = Map_Tile()
    gfw.world.add(gfw.layer.tile, tile)

    bg_music = load_music(gobj.RES_BG + '1-02 Cloud Country.mp3')
    bg_music.repeat_play()
    player.bg = bg
    gfw.world.add(gfw.layer.bg, bg)
    bg.target = player

    try:
        f = open('HOME_Tile.pickle', "rb")
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
    global player, farmtile, bg_tile, farm_objects
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
        elif e.key == SDLK_e:
            player.set_pause()
            start()

        elif e.key == SDLK_k:
            player.set_pause()
            shpstatchange()

        elif e.key == SDLK_a:
            player_xindex = (int)(player.pos[0] // 68)
            player_yindex = (int)((player.pos[1] - 20) // 82)
            print('플레이어 좌표: ' + str(player.pos))
            print('플레이어 인덱스 좌표: ' + str(player_xindex) + ', ' + str(player_yindex))

        #elif e.key == worldmap[current_map].portal[0].key:
        elif e.key == SDLK_SPACE:
            player_xindex = (int)(player.pos[0] // 68)
            player_yindex = (int)((player.pos[1] - 20) // 82)
            for i in range(len(worldmap[current_map].portal)):
                if worldmap[current_map].portal[i].pos == (player_xindex, player_yindex):
                    mapchange(worldmap[current_map].portal[i].nextmap, worldmap[current_map].portal[i].nextpos)
                    break

    player.farmtile = farmtile
    player.farm_objects = bg_tile
    player.handle_event(e)
    farmtile = player.farmtile
    bg_tile = player.farm_objects

def resume():
    global player
    if whostate == MENU_STATE:
        player.inven = menu_state.inven
    elif whostate == SHOP_STATE:
        player.inven = shop_state.inven

def pause():
    pass

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
