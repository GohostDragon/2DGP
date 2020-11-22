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
                if farmtile[y][x] == 1:
                    hompos = bg.to_screen((68 * x, 82 * y))
                    self.hoedirt.clip_draw_to_origin(0, 64 - 16, 16, 16, *hompos,68,82)

    def update(self):
        pass


def start():
    menu_state.inven = player.inven
    gfw.push(menu_state)

def enter():
    gfw.world.init(['bg','tile', 'zombie', 'player','ui'])
    #Zombie.load_all_images()

    global player,bg ,homy, farmtile, tile

    farmtile = [[0] * FARM_XBOARD for i in range(FARM_YBOARD)]

    player = Player()
    gfw.world.add(gfw.layer.player, player)

    tile = Map_Tile()
    gfw.world.add(gfw.layer.tile, tile)

    # bg = gobj.ImageObject('town.jpg', (canvas_width // 2, canvas_height // 2))
    # gfw.world.add(gfw.layer.bg, bg)
    #bg = Background('town.png')
    bg = FixedBackground('farm.jpg')
    bg = FixedBackground('town.jpg')
    #bg = InBackground('home.jpg')
    #bg = gfw.image.load(gobj.RES_DIR + '/map/home.jpg')

    player.bg = bg
    # bg.set_fixed_pos(100, 100)
    gfw.world.add(gfw.layer.bg, bg)
    bg.target = player

    global main_ui
    #main_ui = Main_UI(canvas_width - 65, canvas_height - 230)
    main_ui = Main_UI(canvas_width - 40, canvas_height - 230)
    main_ui.money = 500
    gfw.world.add(gfw.layer.ui, main_ui)

    global game_time
    game_time = Game_Time()
    gfw.world.add(gfw.layer.ui, game_time)

    global zombie_time
    zombie_time = 1

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

    hompos = bg.to_screen(((68 * 10 + 68 * (10 + 1)) // 2, (82 * (10) + 82 * (10 + 1)) // 2))
    #homy.clip_draw(32,64-32,16,16, *hompos,68,82)

    #hompos = bg.to_screen(((68 * 10 + 68 * (10 + 1)) // 2, (82 * (12) + 82 * (12 + 1)) // 2))
    hompos2 = bg.to_screen(((68 * 10 + 68 * (10 + 1)) // 2, (82 * (11) + 82 * (11 + 1)) // 2))
    hompos3 = bg.to_screen(((68 * 10 + 68 * (10 + 1)) // 2, (82 * (10) + 82 * (10 + 1)) // 2))
    hompos4 = bg.to_screen(((68 * 10 + 68 * (10 + 1)) // 2, (82 * (9) + 82 * (9 + 1)) // 2))
    #homy.clip_draw(0, 64 - 16, 16, 16, *hompos, 68, 82)
    homy.clip_draw(0, 64 - 32, 16, 16, *hompos2, 68, 82)
    homy.clip_draw(0, 64 - 48, 16, 16, *hompos3, 68, 82)
    homy.clip_draw(0, 64 - 64, 16, 16, *hompos4, 68, 82)

    hompos = bg.to_screen((68*11, 82*12))

    homy.clip_draw_to_origin(0, 64 - 16, 16, 16, *hompos,68,82)


    for y in range(FARM_YBOARD):
        for x in range(FARM_XBOARD):
            minrec = bg.to_screen((68 * x, 82* (y)))
            maxrec = bg.to_screen((68 * (x+1), 82* (y+1)))
            draw_rectangle(*minrec,*maxrec)

    # gobj.draw_collision_box()
    
def handle_event(e):
    global player, farmtile
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()
        elif e.key == SDLK_e:
            player.set_pause()
            start()

    player.handle_event(e)

    if e.type == SDL_MOUSEBUTTONDOWN:
        if player.equip == 1:
            player_xindex = (int)(player.pos[0] // 68)
            player_yindex = (int)((player.pos[1] - 20) // 82)

            print('player pos' + str(player.pos))
            print('x: '+str(player_xindex) +' y: '+ str(player_yindex))
            if player.action == 0:
                farmtile[player_yindex+1][player_xindex] = 1
            elif player.action == 1:
                if player.mirror == True:
                    farmtile[player_yindex][player_xindex - 1] = 1
                else:
                    farmtile[player_yindex][player_xindex + 1] = 1
            else:
                farmtile[player_yindex - 1][player_xindex] = 1

def resume():
    global player
    player.inven = menu_state.inven

def pause():
    pass

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
