from pico2d import *
import gfw
import gobj
from menu_ui import Menu_UI

HOME, FARM, TOWN, SHOP, COOP, BARN, FOREST, ANIMALSHOP = range(8)

inven = [[0] * 13 for i in range(3)]
current_map = 0

def build_world():
    global menu_ui
    menu_ui = Menu_UI(inven, current_map)
    gfw.world.add(gfw.layer.ui, menu_ui)


def enter():
    build_world()


def update():
    gfw.world.update()


def draw():
    gfw.world.draw()


def handle_event(e):
    # prev_dx = boy.dx
    if e.type == SDL_QUIT:
        return gfw.quit()
    elif e.type == SDL_KEYDOWN:
        if e.key == SDLK_ESCAPE or e.key == SDLK_e:
            return gfw.pop()

    menu_ui.handle_event(e)


def handle_mouse(e):
    global capture
    if capture is not None:
        holding = capture.handle_event(e)
        if not holding:
            capture = None
        return True

    for obj in gfw.world.objects_at(gfw.layer.ui):
        if obj.handle_event(e):
            capture = obj
            return True

    return False


def exit():
    global menu_ui, inven
    gfw.world.remove(menu_ui)
    inven = menu_ui.inven
    print("menu_state exits")


def pause():
    pass


def resume():
    build_world()


if __name__ == '__main__':
    gfw.run_main()
