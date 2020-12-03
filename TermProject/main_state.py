import os.path
import gfw
from pico2d import *
from player import Player
import gobj

from background import *
from main_ui import Main_UI
from game_time import Game_Time

import menu_state
import shop_state
import pickle

canvas_width = 1920
canvas_height = 1080

FARM_XBOARD = 80
FARM_YBOARD = 65

HOME, FARM, TOWN, SHOP, COOP, BARN, FOREST, ANIMALSHOP = range(8)
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
        self.grow = 0

    def deleteobject(self):
        self.tile = 0
        self.col = False

    def setgrowmaxlevel(self, maxlevel):
        self.maxlevel = maxlevel

    def growup(self):
        if self.grow < self.maxlevel:
            self.grow += 1

    def draw(self):
        if self.tile == 1:
            self.tile_object.clip_draw_to_origin(16 * 3, 16 * 5, 16, 16, *self.bgpos, 68, 82)
        elif self.tile == 2:
            self.tile_object.clip_draw_to_origin(16 * 7, 16 * 19, 16, 16, *self.bgpos, 68, 82)
        elif self.tile == 3:
            self.tile_object.clip_draw_to_origin(16 * 7, 16 * 21, 16, 16, *self.bgpos, 68, 82)
        elif self.tile == 4:
            self.crop_object.clip_draw_to_origin(16 * self.grow, 672-29, 16, 16, *self.bgpos, 68, 82)
        elif self.tile == 5:
            self.crop_object.clip_draw_to_origin(128 + 16 * self.grow, 672 - 93, 16, 20, *self.bgpos, 68, 82)
        elif self.tile == 6:
            self.crop_object.clip_draw_to_origin(16 * self.grow, 672 - 64, 16, 16, *self.bgpos, 68, 82)
        elif self.tile == 7:
            self.crop_object.clip_draw_to_origin(128 + 16 * self.grow, 672 - 61, 16, 18, *self.bgpos, 68, 82)

    def get_bb(self):
        return self.bgpos[0], self.bgpos[1], self.bgpos[0] + 68, self.bgpos[1] + 82

    def update(self):
        self.bgpos = bg.to_screen((68 * self.pos[0], 82 * self.pos[1]))

def mapchange(map, pos):
    global current_map, player, bg, bg_tile, mapdatalist
    mapno = worldmap[current_map].data
    mapdatalist[mapno] = player.farm_objects

    gfw.world.clear_at(gfw.layer.object)


    current_map = map
    player.pos = pos

    gfw.world.remove(bg)
    bg = worldmap[current_map].bg

    mapno = worldmap[current_map].data

    bg_tile = []
    for y in range(FARM_YBOARD):
        bg_tile.append([])
        for x in range(FARM_XBOARD):
            bg_tile[y].append(Tile_Object(mapdatalist[mapno][y][x], bg))

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
    menu_state.current_map = current_map
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

    global player, bg, farmtile, bg_tile, tile_object, bg_music, current_map, worldmap, mapdatalist

    worldmap = []
    worldmap.append(Map(InBackground('home.jpg'), HOME))
    worldmap.append(Map(FixedBackground('farm.jpg'), FARM))
    worldmap.append(Map(FixedBackground('town.jpg'), TOWN))
    worldmap.append(Map(InBackground('shop.jpg'), SHOP))
    worldmap.append(Map(InBackground('coopmap.jpg'), COOP))
    worldmap.append(Map(InBackground('barnmap.jpg'), BARN))
    worldmap.append(Map(FixedBackground('forest.jpg'), FOREST))
    worldmap.append(Map(FixedBackground('animalshop.jpg'), ANIMALSHOP))

    worldmap[HOME].addPortal((11, 2), FARM, (4328.08, 3441.80), SDLK_DOWN)
    worldmap[FARM].addPortal((63, 41), HOME, (784.05, 249.96), SDLK_UP)
    #worldmap[FARM].addPortal((78, 39), TOWN, (45.29, 4495.97), SDLK_RIGHT)
    worldmap[FARM].addPortal((78, 39), TOWN, (40.08, 3597.50), SDLK_RIGHT)
    worldmap[FARM].addPortal((78, 40), TOWN, (40.08, 3683.43), SDLK_RIGHT)
    worldmap[FARM].addPortal((78, 41), TOWN, (40.08, 3683.43), SDLK_RIGHT)

    worldmap[FARM].addPortal((52, 41), COOP, (782.63, 323.72), SDLK_RIGHT)
    worldmap[FARM].addPortal((44, 41), BARN, (1115.72, 173.34), SDLK_RIGHT)

    worldmap[FARM].addPortal((39, 0), FOREST, (504.02, 1713.75), SDLK_RIGHT)
    worldmap[FARM].addPortal((40, 0), FOREST, (444.88, 1713.75), SDLK_RIGHT)

    worldmap[TOWN].addPortal((0, 43), FARM, (5337.16, 3280.91), SDLK_LEFT)
    worldmap[TOWN].addPortal((0, 44), FARM, (5337.16, 3360.38), SDLK_LEFT)

    worldmap[TOWN].addPortal((43, 40), SHOP, (814.25, 159.36), SDLK_UP)
    worldmap[TOWN].addPortal((44, 40), SHOP, (814.25, 159.36), SDLK_UP)

    worldmap[TOWN].addPortal((0, 8), FOREST, (3144.10, 155.48), SDLK_UP)
    worldmap[TOWN].addPortal((0, 7), FOREST, (3144.10, 231.22), SDLK_UP)
    worldmap[TOWN].addPortal((0, 6), FOREST, (3144.10, 231.22), SDLK_UP)
    worldmap[TOWN].addPortal((0, 5), FOREST, (3144.10, 231.22), SDLK_UP)
    worldmap[TOWN].addPortal((0, 4), FOREST, (3144.10, 330.76), SDLK_UP)

    worldmap[SHOP].addPortal((11, 1), TOWN, (2957.37, 3371.08), SDLK_DOWN)
    worldmap[SHOP].addPortal((12, 1), TOWN, (2957.37, 3371.08), SDLK_DOWN)

    worldmap[COOP].addPortal((11, 3), FARM, (3567.72, 3433.51), SDLK_DOWN)
    worldmap[BARN].addPortal((16, 1), FARM, (3027.83, 3434.74), SDLK_DOWN)

    worldmap[FOREST].addPortal((25, 8), ANIMALSHOP, (800, 10), SDLK_DOWN)

    worldmap[FOREST].addPortal((4, 20), FARM, (2694.14, 84.64), SDLK_DOWN)
    worldmap[FOREST].addPortal((5, 20), FARM, (2694.14, 84.64), SDLK_DOWN)
    worldmap[FOREST].addPortal((6, 20), FARM, (2694.14, 84.64), SDLK_DOWN)
    worldmap[FOREST].addPortal((7, 20), FARM, (2754.34, 85.05), SDLK_DOWN)
    worldmap[FOREST].addPortal((8, 20), FARM, (2754.34, 85.05), SDLK_DOWN)
    worldmap[FOREST].addPortal((9, 20), FARM, (2754.34, 85.05), SDLK_DOWN)

    worldmap[FOREST].addPortal((46, 3), TOWN, (26.56, 576.70), SDLK_DOWN)
    worldmap[FOREST].addPortal((46, 2), TOWN, (26.56, 483.82), SDLK_DOWN)
    worldmap[FOREST].addPortal((46, 1), TOWN, (26.56, 483.82), SDLK_DOWN)

    worldmap[ANIMALSHOP].addPortal((11, 0), FOREST, (1734.62, 740.94), SDLK_DOWN)

    current_map = HOME

    bg = worldmap[current_map].bg

    farmtile = [[0] * FARM_XBOARD for i in range(FARM_YBOARD)]

    player = Player()
    gfw.world.add(gfw.layer.player, player)

    bg_music = load_music(gobj.RES_BG + '1-02 Cloud Country.mp3')
    bg_music.repeat_play()
    player.bg = bg
    gfw.world.add(gfw.layer.bg, bg)
    bg.target = player

    mapdatalist = []

    f = open('HOME_Tile.pickle', "rb")
    mapdatalist.append(pickle.load(f))
    f.close()

    f = open('Farm_Tile.pickle', "rb")
    mapdatalist.append(pickle.load(f))
    f.close()

    f = open('Town_Tile.pickle', "rb")
    mapdatalist.append(pickle.load(f))
    f.close()

    f = open('Shop_Tile.pickle', "rb")
    mapdatalist.append(pickle.load(f))
    f.close()

#coop
    f = open('Coop_Tile.pickle', "rb")
    mapdatalist.append(pickle.load(f))
    f.close()
#barn
    f = open('Barn_Tile.pickle', "rb")
    mapdatalist.append(pickle.load(f))
    f.close()
#forest
    f = open('Forest_Tile.pickle', "rb")
    mapdatalist.append(pickle.load(f))
    f.close()
# animalshop
    f = open('Animalshop_Tile.pickle', "rb")
    mapdatalist.append(pickle.load(f))
    f.close()

    bg_tile = []
    for y in range(FARM_YBOARD):
        bg_tile.append([])
        for x in range(FARM_XBOARD):
            bg_tile[y].append(Tile_Object(mapdatalist[HOME][y][x], bg))

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

    global sleep_image, sleeping
    sleep_image = gfw.image.load(gobj.RES_DIR + '/logo/loading.jpg')
    sleeping = 0

    global font
    font = gfw.font.load(gobj.RES_DIR + '/ENCR10B.TTF', 30)

def update():
    gfw.world.update()

    global sleeping, bg_music
    if sleeping > 1:
        sleeping -= 1
    elif sleeping == 1:
        bg_music.stop()
        bg_music = load_music(gobj.RES_BG + '1-02 Cloud Country.mp3')
        bg_music.repeat_play()

        global game_time, farmtile, bg_tile, player
        game_time.nextday()
        player.health = 160
        for y in range(FARM_YBOARD):
            for x in range(FARM_XBOARD):
                if farmtile[y][x] == 2 and bg_tile[y][x].tile in range(4, 8):
                    farmtile[y][x] = 1
                    bg_tile[y][x].growup()

        sleeping = 0

def draw():
    global bg
    gfw.world.draw()

    for y in range(FARM_YBOARD):
        for x in range(FARM_XBOARD):
            minrec = bg.to_screen((68 * x, 82* (y)))
            maxrec = bg.to_screen((68 * (x+1), 82* (y+1)))
            draw_rectangle(*minrec,*maxrec)

    if sleeping > 0:
        global font
        sleep_image.draw(canvas_width//2, canvas_height//2)
        font.draw(50, 40, 'Sleep..', (0, 0, 0))
    # gobj.draw_collision_box()
    
def handle_event(e):
    global player, farmtile, bg_tile, farm_objects, game_time
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

        elif e.key == SDLK_z:
            game_time.nextday()
            for y in range(FARM_YBOARD):
                for x in range(FARM_XBOARD):
                    if farmtile[y][x] == 2 and bg_tile[y][x].tile in range(4, 8):
                        farmtile[y][x] = 1
                        bg_tile[y][x].growup()

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

            if current_map == HOME:
                if 17 <= player_xindex <= 18 and 3 <= player_yindex <= 4:
                    global bg_music, sleeping
                    bg_music.stop()
                    bg_music = load_music(gobj.RES_BG+'1-18 Load Game.mp3')
                    bg_music.repeat_play()
                    sleeping = 50
                    
            elif current_map == SHOP:
                if 9 <= player_xindex <= 10 and player_yindex == 8:
                    player.set_pause()
                    shpstatchange()

    player.farmtile = farmtile
    player.farm_objects = bg_tile
    player.handle_event(e)
    farmtile = player.farmtile
    bg_tile = player.farm_objects

    if current_map == FARM:
        if 5360 <= player.pos[0]:
            mapchange(TOWN, (40.08, 3683.43))
        elif player.pos[1] <= 0:
            mapchange(FOREST, (504.02, 1713.75))

    elif current_map == TOWN:
        if player.pos[0] <= 0:
            if player.pos[1] > 3000:
                mapchange(FARM, (5337.16, 3280.91))
            else:
                mapchange(FOREST, (3144.10, 231.22))

    elif current_map == FOREST:
        if 3169 <= player.pos[0]:
            mapchange(TOWN, (26.56, 483.82))
        elif player.pos[1] >= 1718:
            mapchange(FARM, (2754.34, 85.05))

    elif current_map == ANIMALSHOP:
        if player.pos[1] <= 0:
            mapchange(FOREST, (1734.62, 740.94))

def resume():
    global player
    if whostate == MENU_STATE:
        player.inven = menu_state.inven
    elif whostate == SHOP_STATE:
        player.inven = shop_state.inven
        main_ui.money = shop_state.money


def pause():
    pass

def exit():
    global bg_music
    bg_music.stop()
    del bg_music


if __name__ == '__main__':
    gfw.run_main()
