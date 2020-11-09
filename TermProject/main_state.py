import os.path
import gfw
from pico2d import *
from player import Player
from zombie import Zombie
import gobj

from background import FixedBackground as Background
from main_ui import Main_UI

canvas_width = 1920
canvas_height = 1080

SAVE_FILENAME = 'zombies.pickle'

week = ['월','화','수','목','금','토','일']
game_week = 5
game_day = 30
game_time = (7,0)

def enter():
    gfw.world.init(['bg', 'zombie', 'player','ui'])
    #Zombie.load_all_images()

    global player

    if load():
        player = gfw.world.object(gfw.layer.player, 0)
    else:
        player = Player()
        gfw.world.add(gfw.layer.player, player)

        #bg = gobj.ImageObject('town.jpg', (canvas_width // 2, canvas_height // 2))
        #gfw.world.add(gfw.layer.bg, bg)
        bg = Background('town.png')

        player.bg = bg
        #bg.set_fixed_pos(100, 100)
        gfw.world.add(gfw.layer.bg, bg)
        bg.target = player

    global font
    font = gfw.font.load(gobj.RES_DIR + '/BMJUA_ttf.ttf',35)

    global main_ui
    #main_ui = Main_UI(canvas_width - 65, canvas_height - 230)
    main_ui = Main_UI(canvas_width - 40, canvas_height - 230)
    main_ui.money = 500
    gfw.world.add(gfw.layer.ui, main_ui)

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
    '''
    global zombie_time
    zombie_time -= gfw.delta_time
    if zombie_time <= 0:
        gfw.world.add(gfw.layer.zombie, Zombie())
        zombie_time = 5
    '''

def draw():
    gfw.world.draw()


    font.draw(1760,canvas_height - 50, week[game_week]+' ' + str(game_day) + '일',(24,10,31))

    font.draw(1735, canvas_height - 142, str(game_time[0]).zfill(2) + ':' + str(game_time[1]).zfill(2) + 'am', (24, 10, 31))
    # gobj.draw_collision_box()
    
def handle_event(e):
    global player
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

    player.handle_event(e)

    if e.type == SDL_KEYDOWN and e.key == SDLK_s:
        gfw.world.save(SAVE_FILENAME)
        print('Saved to:', SAVE_FILENAME)

def exit():
    pass

if __name__ == '__main__':
    gfw.run_main()
