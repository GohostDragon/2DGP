import gfw
from pico2d import *
import main_state
import gobj

canvas_width = main_state.canvas_width
canvas_height = main_state.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2
clip_sy = 0
icon = [False, False]
timer = 0

scale = 3

def enter():
    global back, logo, game_start, game_exit, cloud, cx
    back = gfw.image.load(gobj.RES_DIR +'/logo/Stardew-Valley-Wallpaper-Wallpaper.jpg')
    logo = gfw.image.load(gobj.RES_DIR +'/logo/TitleButtons.ko-KR.png')

    cx = canvas_width + 100
    cloud = []
    cloud.append(gfw.image.load(gobj.RES_DIR +'/logo/Clouds.png'))
    cloud.append(gfw.image.load(gobj.RES_DIR + '/logo/Clouds.png'))
    cloud.append(gfw.image.load(gobj.RES_DIR + '/logo/Clouds.png'))

    game_start = gfw.image.load(gobj.RES_DIR +'/logo/TitleButtons.ko-KR.png')
    game_exit = gfw.image.load(gobj.RES_DIR +'/logo/TitleButtons.ko-KR.png')

def exit():
    global back, logo, game_start, game_exit
    gfw.image.unload(gobj.RES_DIR +'/logo/Stardew-Valley-Wallpaper-Wallpaper.jpg')
    gfw.image.unload(gobj.RES_DIR +'/logo/TitleButtons.ko-KR.png')
    del back
    del logo
    del game_start
    del game_exit


def update():
    global clip_sy, icon, timer,cx
    if clip_sy < 1440-1000:
        clip_sy += 3
    else:
        clip_sy = 440

    if timer == 155:
        icon[0] = True

    if timer == 165:
        icon[1] = True

    timer += 1
    cx -= 3
    if(cx < -100):
        cx = canvas_width + 100

def draw():
    global icon, scale
    #back.draw(center_x, center_y)
    back.clip_draw(0,clip_sy,2560,1000,center_x, center_y,canvas_width,canvas_height)

    cloud[0].clip_draw(0,696-540,151,71,cx, center_y-100  + 440 - clip_sy,151*scale,71*scale)
    cloud[1].clip_draw(151, 696 - 502, 125, 64, cx, center_y + 150 + 440 - clip_sy, 125 * scale, 64 * scale)
    cloud[2].clip_draw(408, 696 - 504, 69, 40, cx, center_y - 400 + 440 - clip_sy, 69 * scale, 40 * scale)

    logo.clip_draw(0,655-186,400,187,center_x, center_y +200+ 440 - clip_sy,1200,187*scale)

    if icon[0] == True:
        game_start.clip_draw(0, 655 - 245, 74, 58, center_x - 300, 59*3, 74*scale, 59*scale)
    if icon[1] == True:
        game_exit.clip_draw(222, 655 - 245, 74, 58, center_x + 300, 59*3, 74*scale, 59*scale)

def handle_event(e):
    global player
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

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
