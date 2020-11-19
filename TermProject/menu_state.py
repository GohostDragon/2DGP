from pico2d import *
import gfw
import gobj
from menu_ui import Menu_UI

inven = [[0] * 13 for i in range(3)]

def build_world():
    global menu_ui
    menu_ui = Menu_UI(inven)
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
    global menu_ui
    gfw.world.remove(menu_ui)
    print("menu_state exits")
    pass


def pause():
    pass


def resume():
    build_world()


if __name__ == '__main__':
    gfw.run_main()
