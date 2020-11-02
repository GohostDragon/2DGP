from pico2d import *

Object_Scale = 0.5

KEY_MAP = {
    (SDL_KEYDOWN, SDLK_LEFT):  (-1,  0),
    (SDL_KEYDOWN, SDLK_RIGHT): ( 1,  0),
    (SDL_KEYDOWN, SDLK_DOWN):  ( 0, -1),
    (SDL_KEYDOWN, SDLK_UP):    ( 0,  1),
    (SDL_KEYUP, SDLK_LEFT):    ( 1,  0),
    (SDL_KEYUP, SDLK_RIGHT):   (-1,  0),
    (SDL_KEYUP, SDLK_DOWN):    ( 0,  1),
    (SDL_KEYUP, SDLK_UP):      ( 0, -1),
}

Right_A = False
Left_A = False
Up_A = False
Down_A = False
menustate = False

class GameObject:#게임 오브젝트 클래스
    def __init__(self,image,pos):
        self.image = load_image(image)#이미지
        self.pos = pos#좌표
        self.rad = 0
        self.fidex = 0
        self.active_anim = False
        self.mirror = False

        self.scale = 1

    def setImage(self,image):
        self.image = load_image(image)#이미지 설정

    def setClip(self,left,bottom,width,height):#클립 크기 설정
        self.left = left
        self.bottom = bottom
        self.width = width
        self.height = height

    def setFrameIndex(self,fidex):#프레임 인덱스 설정
        self.fidex = fidex

    def setFrameMax(self,fmax):#프레임 최대 갯수 설정
        self.fidex = 0
        self.fmax = fmax

    def playAnime(self):#애니메이션 실행
        if self.fmax == 0:
            return
        self.setFrameIndex((self.fidex + 1) % self.fmax)

    def drawObject(self):
        self.image.draw(self.pos[0],self.pos[1],self.width*Object_Scale,self.height*Object_Scale)

    def drawClipObject(self):
        self.image.clip_draw(self.left,self.bottom,self.width,self.height,self.pos[0],self.pos[1],self.width*self.scale,self.height*self.scale)

    def drawClipObject2(self,w,h):
        self.image.clip_draw(self.left,self.bottom,self.width,self.height,self.pos[0],self.pos[1],w*self.scale,h*self.scale)

    def drawClip_composite(self):
        self.image.clip_composite_draw(self.left,self.bottom,self.width,self.height,self.rad,'h',self.pos[0], self.pos[1],self.width*self.scale,self.height*self.scale)

    def drawClip_composite2(self,w,h):
        self.image.clip_composite_draw(self.left,self.bottom,self.width,self.height,self.rad,'h',self.pos[0], self.pos[1],w*self.scale,h*self.scale)

class outtile(GameObject):
    def __init__(self,pos):
        self.setImage('res/spring_outdoorsTileSheet.ko-KR.png')
        self.setClip(16*7, 1264-95-(16*2), 16, 16)
        self.pos = pos
        self.scale = 4

class Ax(GameObject):
    def __init__(self):
        self.setImage('res/ax_sheet.png')
        self.setClip(0, 250*2, 250, 300)
        self.scale = 1
        self.rad = 0
        self.fidex = 0

class Gok(GameObject):
    def __init__(self):
        self.setImage('res/gok_sheet.png')
        self.setClip(0, 300*2, 250, 300)
        self.scale = 1
        self.rad = 0
        self.fidex = 0

class Character(GameObject):
    def __init__(self):
        self.setImage('res/walk_sheet.png')
        self.setClip(0, 130*2, 70, 130)

        self.fmax = 0
        self.pos = (400,400)
        self.fidex = 0
        self.rad = 0
        self.mirror = False

        self.movetype = 2
        self.active = False
        self.direct = 0#0아래 1오른쪽 2왼쪽 3위

        self.scale = 1

    def goTopMove(self):
        self.setFrameMax(8)
        self.movetype = 0
        self.direct = 3
        self.mirror = False
        self.active = True

    def goBottomMove(self):
        self.setFrameMax(8)
        self.movetype = 2
        self.direct = 0
        self.mirror = False
        self.active = True

    def goRightMove(self):
        self.setFrameMax(6)
        self.movetype = 1
        self.direct = 1
        self.mirror = False
        self.active = True

    def goLeftMove(self):
        self.setFrameMax(6)
        self.movetype = 1
        self.direct = 2
        self.mirror = True
        self.active = True

    def stopMove(self):
        self.setFrameMax(0)
        self.active = False


def handle_events():
    global running, dirx,diry, player, Right_Left, Right_A, Left_A, Up_A, Down_A, action,Ax,Gok,menustate,rx,mouse_pos
    evts = get_events()
    SDL_SCANCODE_R
    for e in evts:
        if e.type == SDL_QUIT:
            running = False
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_ESCAPE:
                running = False
            elif e.key == SDLK_RIGHT:
                dirx += 1
                player.goRightMove()
                Right_A = True

            elif e.key == SDLK_LEFT:
                dirx -= 1
                player.goLeftMove()
                Left_A = True

            elif e.key == SDLK_UP:
                diry += 1
                player.goTopMove()
                Up_A = True

            elif e.key == SDLK_DOWN:
                diry -= 1
                player.goBottomMove()
                Down_A = True

            elif e.key == SDLK_ESCAPE:
                running = False

            elif e.key == SDLK_e:
                if(menustate):
                    menustate = False
                else:
                    menustate = True
            elif e.key == SDLK_1:
                rx = 573+64*0

            elif e.key == SDLK_2:
                rx = 573+64*1

            elif e.key == SDLK_3:
                rx = 573+64*2

            elif e.key == SDLK_4:
                rx = 573+64*3

            elif e.key == SDLK_5:
                rx = 573+64*4

            elif e.key == SDLK_6:
                rx = 573+64*5

            elif e.key == SDLK_7:
                rx = 573+64*6

            elif e.key == SDLK_8:
                rx = 573+64*7

            elif e.key == SDLK_9:
                rx = 573+64*8

            elif e.key == SDLK_0:
                rx = 573+64*9

            elif e.key == SDLK_MINUS:
                rx = 573 + 64 * 10

            elif e.key == SDLK_EQUALS:
                rx = 573 + 64 * 11

        elif e.type == SDL_KEYUP:
            if e.key == SDLK_RIGHT:
                dirx -= 1
                Right_A = False
                if Up_A == False and Down_A == False:
                    player.stopMove()
            elif e.key == SDLK_LEFT:
                dirx += 1
                Left_A = False
                if Up_A == False and Down_A == False:
                    player.stopMove()
            elif e.key == SDLK_UP:
                diry -= 1
                Up_A = False
                if Left_A == False and Right_A == False:
                    player.stopMove()
            elif e.key == SDLK_DOWN:
                diry += 1
                Down_A = False
                if Left_A == False and Right_A == False:
                    player.stopMove()

        elif e.type == SDL_MOUSEWHEEL:
            print('test1')
            if(e.wheel.y > 0):
                rx += 65
                print('test2')
            elif(e.wheel.y < 0):
                rx -= 65

        elif e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                action = 1
                Ax.pos = player.pos
                if(player.movetype == 1):
                    Ax.fidex = 0
                    Ax.fmax = 3
                else:
                    Ax.fidex = 0
                    Ax.fmax = 4

            if e.button == SDL_BUTTON_RIGHT:
                action = 2
                Gok.pos = player.pos
                if(player.movetype == 0):
                    Gok.fidex = 0
                    Gok.fmax = 3
                else:
                    Gok.fidex = 0
                    Gok.fmax = 4

        if e.type == SDL_MOUSEMOTION:
            mouse_pos = (e.x,get_canvas_height()-1-e.y)

open_canvas(1920,1080,False,True)

'''
ch = load_image('img/farmer_base_bald.png')
sh = load_image('img/shirts.png')
ha = load_image('img/hairstyles.png')
'''
main_hud = load_image('res/Cursors.ko-KR.png')
mouse_cusor = load_image('res/Cursors.ko-KR.png')

main_ui = load_image('res/mainstate_item_ui.png')
menu_ui = load_image('res/menustate_ui1.png')

item_tool = load_image('res/tools.png')
item_tool2 = load_image('res/tools.png')
item_tool3 = load_image('res/tools.png')
item_tool4 = load_image('res/tools.png')

player = Character()
axe = Ax()
gokk = Gok()

action = 0
tile = []

for i in range(10):
    list = []
    for j in range(10):
        list.append(outtile((j*16*4,i*16*3.7)))
    tile.append(list)

x = 0

dirx = 0
diry = 0
rx , ry = (573,63)

Right_Left = True
hide_cursor()
mouse_pos = (0,0)
while x < 800:
    clear_canvas()
    player.setClip(70 * player.fidex, 130 * player.movetype, 70, 130)

    if action == 1:
        axe.setClip(250 * axe.fidex, 300 * player.movetype, 250, 300)
        if(axe.fidex+1 == axe.fmax):
            action = 0

    elif action == 2:
        gokk.setClip(250 * gokk.fidex, 300 * player.movetype, 250, 300)
        if(gokk.fidex+1 == gokk.fmax):
            action = 0

    for y in range(10):
        for x in range(10):
            tile[y][x].drawClipObject()


    if action == 0:
        if player.mirror == False:
            player.drawClipObject()
        else:
            player.drawClip_composite()
    elif action == 1:
        if player.mirror == False:
            axe.drawClipObject()
        else:
            axe.drawClip_composite()

    elif action == 2:
        if player.mirror == False:
            gokk.drawClipObject()
        else:
            gokk.drawClip_composite()

    if(menustate == False):
        main_ui.draw(960,100)
        draw_rectangle(rx, ry, rx + 65, ry + 70)
        draw_rectangle(rx - 1, ry - 1, rx - 1 + 65, ry - 1 + 70)
        draw_rectangle(rx + 1, ry + 1, rx + 1 + 65, ry + 1 + 70)

        item_tool.clip_draw(79, 384 - (48 + 64 * 0), 17, 17, 604 + 64 * 0, 100, 17 * 4, 17 * 4)
        item_tool2.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * 1, 100, 17 * 4, 17 * 4)
        item_tool3.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * 2, 100, 17 * 4, 17 * 4)
        item_tool4.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * 3, 100, 17 * 4, 17 * 4)
    else:
        menu_ui.draw(960,540)

        item_tool.clip_draw(79, 384 - (48 + 64 * 0), 17, 17, 604 + 64 * 0, 760, 17 * 4, 17 * 4)
        item_tool2.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * 1, 760, 17 * 4, 17 * 4)
        item_tool3.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * 2, 760, 17 * 4, 17 * 4)
        item_tool4.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * 3, 760, 17 * 4, 17 * 4)

        item_tool.clip_draw(79, 384 - (48 + 64 * 0), 17, 17, 604 + 64 * 0, 680, 17 * 4, 17 * 4)
        item_tool2.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * 1, 680, 17 * 4, 17 * 4)
        item_tool3.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * 2, 680, 17 * 4, 17 * 4)
        item_tool4.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * 3, 680, 17 * 4, 17 * 4)

        item_tool.clip_draw(79, 384 - (48 + 64 * 0), 17, 17, 604 + 64 * 4, 680, 17 * 4, 17 * 4)
        item_tool2.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * 5, 680, 17 * 4, 17 * 4)
        item_tool3.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * 6, 680, 17 * 4, 17 * 4)
        item_tool4.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * 7, 680, 17 * 4, 17 * 4)

        item_tool.clip_draw(79, 384 - (48 + 64 * 0), 17, 17, 604 + 64 * 0, 614, 17 * 4, 17 * 4)
        item_tool2.clip_draw(79, 384 - (64 * 1 + 48), 17, 17, 604 + 64 * 1, 614, 17 * 4, 17 * 4)
        item_tool3.clip_draw(79, 384 - (64 * 2 + 48), 17, 17, 604 + 64 * 2, 614, 17 * 4, 17 * 4)
        item_tool4.clip_draw(79, 384 - (64 * 3 + 48), 17, 17, 604 + 64 * 3, 614, 17 * 4, 17 * 4)

    main_hud.clip_draw(332,2256-432-57,73,57,1760,950,73*4,57*4)
    mouse_cusor.clip_draw(0,2256-10,8,10,mouse_pos[0],mouse_pos[1],8*4,10*4)



    update_canvas()

    handle_events()

    player.pos = (player.pos[0]+dirx*7,player.pos[1]+ diry * 7)
    for y in range(10):
        for x in range(10):
            tile[y][x].pos = (tile[y][x].pos[0]-dirx*7,tile[y][x].pos[1]- diry * 7)

    if action == 0:
        player.playAnime()
    elif action == 1:
        axe.playAnime()
    elif action == 2:
        gokk.playAnime()
    delay(0.1)

delay(1)
clear_canvas()