from pico2d import *

def handle_events():
    global running, dx, x, y
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
        elif e.type == SDL_MOUSEMOTION:
            x,y = e.x,get_canvas_height() - e.y -1

open_canvas()

gra = load_image('../../img/grass.png')
ch = load_image('../../img/run_animation.png')

running = True
x,y = 400,85
dx = 0
finx = 0

while running:
    clear_canvas()
    gra.draw(400, 30)
    ch.clip_draw(finx*100,0,100,100,x,y)
    update_canvas()

    handle_events()

    x += dx
    finx = (finx+1)%8

    delay(0.01)

close_canvas()
'''
이벤트 처리 폴링, 드리븐
폴링: 주도권을 가짐 루프를 돌면서 지금 처리하는 이벤트가 뭔지
드리븐 : 특정 종류의 이벤트 일때 혹은 모든 이벤트를 알려줘

속성+행위 = 인캡슐레이션
속성 : 변수
행동 : 함수
'''