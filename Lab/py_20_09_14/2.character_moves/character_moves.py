from pico2d import *

open_canvas()

grass = load_image('../../img/grass.png')
character = load_image('../../img/character.png')

x = 0
while (x < 800):
    clear_canvas_now()
    grass.draw_now(400, 30)
    character.draw_now(x, 90)
    x = x + 2
    delay(0.01)

close_canvas()
