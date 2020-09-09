import turtle as t

s = 70 #글자 크기
d = 15 #글자 간격

#펜이동 좌표:x,y 각도:angle
def movepen(x,y,angle):
    t.penup()
    t.goto(x, y)
    t.setheading(angle)
    t.pendown()

#ㄱ
def zaum_1(x,y):
    movepen(x,y,0)
    t.forward(s)
    t.right(120)
    t.forward(s + 20)

#ㄴ
def zaum_4(x,y):
    movepen(x,y,-90)
    t.forward(s - 10)
    t.left(90)
    t.forward(s + 10)

#ㅁ
def zaum_2(x,y):
    movepen(x,y,0)
    for i in range(4):
        t.forward(s)
        t.right(90)

#ㅅ
def zaum_3(x, y):
    movepen(x, y, 60)
    t.forward(s + 20)
    t.right(120)
    t.forward(s + 20)


#ㅇ
def zaum_6(x, y):
    movepen(x, y, 180)
    t.circle(30)


#ㅈ
def zaum_5(x, y):
    movepen(x, y, 60)
    t.forward(s + 20)
    t.right(120)
    t.forward(s + 20)
    t.penup()
    t.goto(x, y+s+10)
    t.left(60)
    t.pendown()
    t.forward(s + 20)

#ㅣ
def moum_1(x,y):
    movepen(x, y, -90)
    t.forward(s+10)

#ㅓ
def moum_2(x,y):
    movepen(x, y, -90)
    t.forward(s + 10)
    t.penup()
    t.right(180)
    t.forward((s + 10) / 2)
    t.left(90)
    t.pendown()
    t.forward(s / 3)

#ㅜ
def moum_3(x,y):
    movepen(x, y, 0)
    t.forward(s + 20)
    t.penup()
    t.goto((2*x+s+20)/ 2, y)
    t.right(90)
    t.pendown()
    t.forward(s / 3)

def WriteName(x, y):

    t.reset()
    zaum_1(x,y)

    uz_y = y-s-10#받침 자음 y 좌표

    moum_1(x+s+d,y)

    zaum_2(x+d,uz_y-d)

    zaum_3(x+s+2*d,uz_y)

    moum_2(x+2*s+4*d,y)

    zaum_4(x+s+3*d,uz_y-d)

    z3_x = x+2*s+5*d
    zaum_5(z3_x,uz_y)

    moum_3(z3_x, uz_y-5)

    zaum_6((z3_x*2+s+20)/2, uz_y-5-s/3)
    t.exitonclick()


# x,y = eval(input("x,y 좌표 입력:"))
WriteName(-200, 100)



