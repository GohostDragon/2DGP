from pico2d import *

def handle_events():
    global running
    evts = get_events()

    for e in evts:
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
            running = False

open_canvas()

gra = load_image('../../img/grass.png')
ch = load_image('../../img/run_animation.png')

running = True
x = 0
finx = 0

while running:
    clear_canvas()
    gra.draw(400, 30)
    ch.clip_draw(finx*100,0,100,100,x,85)
    update_canvas()

    handle_events()

    x += 2
    finx = (finx+1)%8

    delay(0.01)

close_canvas()