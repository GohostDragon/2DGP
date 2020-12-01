from pico2d import *
import gfw
import gobj
from shop_ui import Shop_UI
from main_ui import Main_UI

inven = [[0] * 13 for i in range(3)]
money = 0

def build_world():
    global shop_ui
    shop_ui = Shop_UI(inven)
    gfw.world.add(gfw.layer.ui, shop_ui)

    global main_ui
    main_ui = Main_UI(872, 366)
    main_ui.money = money
    main_ui.display = money
    gfw.world.add(gfw.layer.ui, main_ui)

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

    shop_ui.handle_event(e)


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
    global shop_ui, inven, main_ui
    gfw.world.remove(shop_ui)
    gfw.world.remove(main_ui)
    inven = shop_ui.inven
    print("shop_state exits")


def pause():
    pass


def resume():
    build_world()


if __name__ == '__main__':
    gfw.run_main()
