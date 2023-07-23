### Galaxy ###

import pyglet
from OpenGL.GL import *
from random import *
from pyglet.gl import *
import math
window = pyglet.window.Window(width =1000, height = 800)

def circle(x0, y0, r, n):
    alpha = 2 * math.pi / n
    angle = 0
    glBegin(GL_POLYGON)
    for i in range(n):
        x1 = x0 + r * math.cos(angle)
        y1 = y0 + r * math.sin(angle)
        glVertex2f(x1, y1)
        angle = angle + alpha
    glEnd()

class Star:
    def __init__(self):
        self.x = randint(0, 1000)
        self.y = randint(0, 800)

        self.speed_x = randint(1, 10)
        self.speed_y = randint(1, 5)

        self.brightness = randint(64, 255)

    def draw(self):
        glColor3ub(int(self.brightness), int(self.brightness), int(self.brightness))
        if 39 >= self.speed_x * self.speed_y >= 24:
            glPointSize(2)
        if 50 >= self.speed_x * self.speed_y > 39:
            glPointSize(3)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

    def update(self, dt):

        self.x = self.x + self.speed_x * dt
        self.y = self.y + self.speed_y * dt

        if self.x > 1000:
            self.x = 0
            self.y = randint(0, 800)
        if self.y > 800:
            self.x = randint(0, 1000)
            self.y = 0

star_list = []
for i in range(250):
    s = Star()
    star_list.append(s)

class Big_Star:
    def __init__(self):
        self.x = 500
        self.y = 400


        self.red_min = 200
        self.red_max = 255
        self.red = randint(self.red_min, self.red_max)
        self.green_min = 140
        self.green_max = 170
        self.green = randint(self.green_min, self.green_max)
        self.red_direction = 1
        self.green_direction = 1
    def draw(self):
        glColor3ub(int(self.red), int(self.green), 30)
        circle(self.x, self.y, 80, 32)
    def update(self, dt):
        self.red = self.red + 60 * dt * self.red_direction
        self.green = self.green + 60 * dt * self.green_direction
        if self.red >= self.red_max:
            self.red = self.red_max
            self.red_direction = -1
        if self.green >= self.green_max:
            self.green = self.green_max
            self.green_direction = -1
        if self.red <= self.red_min:
            self.red = self.red_min
            self.red_direction = 1
        if self.green <= self.green_min:
            self.green = self.green_min
            self.green_direction = 1


bStar_list = []
for i in range(1):
    bs = Big_Star()
    bStar_list.append(bs)


class Planet:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = float((1/(y-400))*1000)/6
        self.radius = randint(10, 40)
        self.angle = 1
        self.rotation_radius = self.y - 400

        self.red = randint(24, 200)
        self.green = randint(24, 200)
        self.blue = randint(24, 200)
    def draw(self):
        glColor3ub(self.red, self.green, self.blue)
        circle(self.x, self.y, self.radius, 32)
    def update(self, dt):
        #Circular Movement
        center_x = 500
        center_y = 400
        if self.angle > 360:
            self.angle = 0
        else:
            self.angle = self.angle + self.speed * dt

        self.x = center_x + self.rotation_radius * math.cos(self.angle)
        self.y = center_y + self.rotation_radius * math.sin(self.angle)


planet_list = []
planet_y = 400 + 150
for i in range(3):
    p = Planet(500, planet_y)
    planet_list.append(p)
    planet_y = planet_y + 100

@window.event
def on_draw():
    window.clear()

    for star in star_list:
        star.draw()

    for big_star in bStar_list:
        big_star.draw()

    for planet in planet_list:
        planet.draw()



def update(dt):
    for big_star in bStar_list:
        big_star.update(dt)
    for planet in planet_list:
        planet.update(dt)
    for star in star_list:
        star.update(dt)


pyglet.clock.schedule_interval(update, 1/120)
pyglet.app.run()


