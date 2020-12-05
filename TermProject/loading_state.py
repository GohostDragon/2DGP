import gfw
from pico2d import *
import main_state
from gobj import *

canvas_width = main_state.canvas_width
canvas_height = main_state.canvas_height

center_x = canvas_width // 2
center_y = canvas_height // 2

def enter():
    global back, index, file, bg_music
    back = gfw.image.load(res('/logo/loading.jpg'))
    index = 0

    global font, display
    font = gfw.font.load(res('ENCR10B.TTF'), 30)
    display = ''

    global frame_interval
    frame_interval = gfw.frame_interval
    gfw.frame_interval = 0

    bg_music = load_music(RES_BG+'1-18 Load Game.mp3')
    bg_music.repeat_play()

def exit():
    global back, bg_music
    bg_music.stop()
    del bg_music
    del back

    global frame_interval
    gfw.frame_interval = frame_interval

def update():
    global index, display
    image_count = len(IMAGE_FILES)
    font_count = len(FONT_PAIRS)
    if index < image_count:
        file = IMAGE_FILES[index]
        gfw.image.load(file)
        display = file
    elif index - image_count < font_count:
        file, size = FONT_PAIRS[index - image_count]
        gfw.font.load(file, size)
        display = '%s %dpt' % (file, size)
    else:
        gfw.change(main_state)
        return
    index += 1

def draw():
    back.draw(center_x, center_y)
    image_count = len(IMAGE_FILES)
    font_count = len(FONT_PAIRS)
    progress = index / (image_count + font_count)

    global display
    font.draw(300, 250, display)
    font.draw(50, 40, 'Loading(%.f%%)' % (progress * 100), (0, 0, 0))

def handle_event(e):
    global player
    if e.type == SDL_QUIT:
        gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE:
            gfw.pop()

IMAGE_FILES = [
    "res/walk_sheet.png",
    "res/spring_outdoorsTileSheet.ko-KR.png",
    "res/ax_sheet.png",
    "res/gok_sheet.png",
    "res/mainstate_item_ui.png",
    "res/Cursors.ko-KR.png",
    "res/map/farm.jpg",
    "res/map/town.jpg",
    "res/map/home.jpg",
    "res/map/shop.jpg",
    "res/map/coopmap.jpg",
    "res/map/barnmap.jpg",
    "res/map/forest.jpg",
    "res/map/animalshop.jpg",
]

FONT_PAIRS = [
    ("res/ENCR10B.TTF", 10),
    ("res/ENCR10B.TTF", 20),
    ("res/ENCR10B.TTF", 30),
]

if __name__ == '__main__':
    gfw.run_main()
