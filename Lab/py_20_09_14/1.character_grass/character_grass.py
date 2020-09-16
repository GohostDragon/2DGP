from pico2d import *

open_canvas()

grass = load_image('../../img/grass.png')
character = load_image('../../img/character.png')

grass.draw_now(400, 30)
character.draw_now(400, 90)

delay(5)

close_canvas()
