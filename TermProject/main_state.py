import os.path
import gfw
from pico2d import *
from player import Player
from zombie import Zombie
import gobj

from background import FixedBackground as Background
from main_ui import Main_UI
from game_time import Game_Time

import menu_state

canvas_width = 1920
canvas_height = 1080

SAVE_FILENAME = 'zombies.pickle'

def start():
    gfw.push(menu_state)

def enter():
    gfw.world.init(['bg', 'zombie', 'player','ui'])
    #Zombie.load_all_images()

    global player

    player = Player()
    gfw.world.add(gfw.layer.player, player)

    # bg = gobj.ImageObject('town.jpg', (canvas_width // 2, canvas_height // 2))
    # gfw.world.add(gfw.layer.bg, bg)
    bg = Background('town.png')

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

def load():
    if not os.path.isfile(SAVE_FILENAME):
        return False

    gfw.world.load(SAVE_FILENAME)
    print('Loaded from:', SAVE_FILENAME)
    return True

def update():
    gfw.world.update()

def draw():
    gfw.world.draw()
    # gobj.draw_collision_box()
    
def handle_event(e):
    global player
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

def resume():
    pass

def pause():
    pass

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
