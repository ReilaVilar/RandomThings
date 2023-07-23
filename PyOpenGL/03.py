import pyglet
from random import *
from pyglet.gl import *
from OpenGL.GL import *
import math
window = pyglet.window.Window(width=1000, height=600)

speed  = 1


class Square:
    def __init__(self):
        self.lenght = randint(10, 30)
        self.x = randint(0, 1000 - self.lenght)
        self.y = randint(0 + self.lenght, 600)

        self.speed_x = randint(-20, 20)
        self.speed_y = randint(-20, 20)

        self.red = 255
        self.green = 255
        self.blue = 255

    def draw(self):
        glBegin(GL_QUADS)
        glColor3ub(self.red, self.green, self.blue)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.lenght, self.y)
        glVertex2f(self.x + self.lenght, self.y - self.lenght)
        glVertex2f(self.x, self.y - self.lenght)
        glEnd()
    def update(self, dt):
        self.x = self.x + self.speed_x * dt * speed
        self.y = self.y + self.speed_y * dt * speed

        #LEFT
        if self.x < 0:
            self.x = 0
            self.speed_x = - self.speed_x
            self.red = 0
            self.green = 255
            self.blue = 0
        #RIGHT
        if self.x > 1000 - self.lenght:
            self.x = 1000 - self.lenght
            self.speed_x = - self.speed_x
            self.red = 255
            self.green = 0
            self.blue = 0
        #BOTTOM
        if self.y < 0 + self.lenght:
            self.y = self.lenght
            self.speed_y = - self.speed_y
            self.red = 255
            self.green = 255
            self.blue = 0
        #TOP
        if self.y > 600:
            self.y = 600
            self.speed_y = - self.speed_y
            self.red = 0
            self.green = 0
            self.blue = 255

square_list = []
for i in range(30):
    s = Square()
    square_list.append(s)

@window.event
def on_key_press(symbol, modifier):
    global speed

    if symbol == pyglet.window.key.W:
        speed += 1
    if symbol == pyglet.window.key.S:
        speed -= 1
    if speed < 0:
        speed = 0
    if symbol == pyglet.window.key.SPACE:
        newSquare = Square()
        square_list.append(newSquare)



@window.event
def on_draw():
    window.clear()
    global speed

    for s in square_list:
        s.draw()

    lbl = pyglet.text.Label("speed = " + str(speed) ,font_name="Times New Roman", font_size=20,x=50, y=550)
    lbl.draw()


def update(dt):
    for s in square_list:
        s.update(dt)

pyglet.clock.schedule_interval (update, 1/120)
pyglet.app.run()