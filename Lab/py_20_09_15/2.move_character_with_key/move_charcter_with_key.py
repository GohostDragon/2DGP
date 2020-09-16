from pico2d import *

def handle_events():
    global running, dx, x
    evts = get_events()

    for e in evts:
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
            elif e.key == SDLK_LEFT:
                dx -= 1
            elif e.key == SDLK_RIGHT:
                dx += 1
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                dx += 1
            elif e.key == SDLK_RIGHT:
                dx -= 1
            #print('keyup',dx)

open_canvas()

gra = load_image('../../img/grass.png')
ch = load_image('../../img/run_animation.png')

running = True
x = 400
dx = 0
finx = 0

while running:
    clear_canvas()
    gra.draw(400, 30)
    ch.clip_draw(finx*100,0,100,100,x,85)
    update_canvas()

    handle_events()

    x += dx
    finx = (finx+1)%8

    delay(0.01)

close_canvas()