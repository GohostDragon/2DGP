import turtle as t

count = 10 #갯수
s = 45 #크기

def movepen(x,y,d):
    t.penup()
    t.goto(x, y)
    t.setheading(d)
    t.pendown()

def drawline(x,y,d):
    movepen(x,y,d)
    t.forward(s*count)

t.speed(0)
for i in range(count+1):
    drawline(i*s,0,90)
    drawline(0, i*s, 0)
t.exitonclick()