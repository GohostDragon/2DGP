import gfw
from pico2d import *
import main_state
import gobj
import random
import loading_state
import tile_object

canvas_width = main_state.canvas_width
canvas_height = main_state.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2
clip_sy = 0
icon = [False, False]
timer = 0

scale = 3

cloudMax = 30

class Farm_Object:
    def __init__(self):
        self.tile = 0
        self.col = False
        self.pos = (0,0)

class Cloud:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.image = gfw.image.load(gobj.RES_DIR + '/logo/Clouds.png')
        if type == 0:
            self.sx = 0
            self.sy = 696 - 540
            self.width = 151
            self.heigt = 71
            self.speed = 2
        elif type == 1:
            self.sx = 151
            self.sy = 696 - 502
            self.width = 125
            self.heigt = 64
            self.speed = 3
        elif type == 2:
            self.sx = 408
            self.sy = 696 - 504
            self.width = 69
            self.heigt = 40
            self.speed = 4

    def draw(self):
        self.image.clip_draw(self.sx, self.sy, self.width, self.heigt, self.x, center_y + self.y + 440 - clip_sy, self.width * scale, self.heigt * scale)

    def update(self):
        self.x -= self.speed
        if (self.x < -100):
            self.x = canvas_width + 100

def enter():
    global back, logo, game_start, game_exit, cloud, cx, cloud, cloudMax, bg_music
    back = gfw.image.load(gobj.RES_DIR +'/logo/Stardew-Valley-Wallpaper-Wallpaper.jpg')
    logo = gfw.image.load(gobj.RES_DIR +'/logo/TitleButtons.ko-KR.png')

    cx = canvas_width + 100
    cloud = []
    for i in range(cloudMax):
        cloud.append(Cloud(random.randint(canvas_width/2,canvas_width),-400+ random.randint(0,800),random.randint(0,2)))

    game_start = gfw.image.load(gobj.RES_DIR +'/logo/TitleButtons.ko-KR.png')
    game_exit = gfw.image.load(gobj.RES_DIR +'/logo/TitleButtons.ko-KR.png')
    bg_music = load_music(gobj.RES_BG+'1-01 Stardew Valley Overture.mp3')
    bg_music.repeat_play()

def exit():
    global back, logo, game_start, game_exit, bg_music
    gfw.image.unload(gobj.RES_DIR +'/logo/Stardew-Valley-Wallpaper-Wallpaper.jpg')
    gfw.image.unload(gobj.RES_DIR +'/logo/TitleButtons.ko-KR.png')
    bg_music.stop()
    del bg_music
    del back
    del logo
    del game_start
    del game_exit


def update():
    global clip_sy, icon, timer,cx, cloud , cloudMax
    if clip_sy < 1440-1000:
        clip_sy += 3
    else:
        clip_sy = 440

    if timer == 155:
        icon[0] = True

    if timer == 165:
        icon[1] = True

    timer += 1

    for i in range(cloudMax):
        cloud[i].update()

def draw():
    global icon, scale, cloudMax
    #back.draw(center_x, center_y)
    back.clip_draw(0,clip_sy,2560,1000,center_x, center_y,canvas_width,canvas_height)
    for i in range(cloudMax):
        cloud[i].draw()

    logo.clip_draw(0,655-186,400,187,center_x, center_y +200+ 440 - clip_sy,1200,187*scale)

    if icon[0] == True:
        game_start.clip_draw(0, 655 - 245, 74, 58, center_x - 300, 59*3, 74*scale, 59*scale)
        if center_x - 300 - 74*scale//2 < mouse_pos[0] < center_x - 300 - 74*scale//2 + 74*scale and 59*3 - 59*scale//2 < mouse_pos[1] < 59*3 - 59*scale//2 + 59*scale:
            game_start.clip_draw(0, 655 - 303, 74, 58, center_x - 300, 59 * 3, 74 * scale, 59 * scale)
    if icon[1] == True:
        game_exit.clip_draw(222, 655 - 245, 74, 58, center_x + 300, 59*3, 74*scale, 59*scale)
        if center_x + 300 - 74*scale//2 < mouse_pos[0] < center_x + 300 - 74*scale//2 + 74*scale and 59*3 - 59*scale//2 < mouse_pos[1] < 59*3 - 59*scale//2 + 59*scale:
            game_start.clip_draw(222, 655 - 303, 74, 58, center_x + 300, 59 * 3, 74 * scale, 59 * scale)

def handle_event(e):
    global player, mouse_pos
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

    if e.type == SDL_MOUSEMOTION:
        mouse_pos = (e.x, get_canvas_height() - 1 - e.y)

    elif e.type == SDL_MOUSEBUTTONDOWN:
        mouse_pos = (e.x, get_canvas_height() - 1 - e.y)
        if center_x - 300 - 74 * scale // 2 < mouse_pos[
            0] < center_x - 300 - 74 * scale // 2 + 74 * scale and 59 * 3 - 59 * scale // 2 < mouse_pos[
            1] < 59 * 3 - 59 * scale // 2 + 59 * scale:
            gfw.change(loading_state)
            return
        elif center_x + 300 - 74*scale//2 < mouse_pos[0] < center_x + 300 - 74*scale//2 + 74*scale and 59*3 - 59*scale//2 < mouse_pos[1] < 59*3 - 59*scale//2 + 59*scale:
            gfw.quit()

IMAGE_FILES = [
    "res/kpu_1280x960.png",
    "res/animation_sheet.png",
    "res/walk_sheet.png",
    "res/spring_outdoorsTileSheet.ko-KR.png",
    "res/ax_sheet.png",
    "res/gok_sheet.png",
    "res/mainstate_item_ui.png",
    "res/Cursors.ko-KR.png",
]

FONT_PAIRS = [
    ("res/ENCR10B.TTF", 10),
    ("res/ENCR10B.TTF", 20),
    ("res/ENCR10B.TTF", 30),
]

if __name__ == '__main__':
    gfw.run_main()
