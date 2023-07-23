from random import *
from pyglet.gl import *
from OpenGL.GL import *
import math

window = pyglet.window.Window(width=1000, height=600)

key_state_a = False
key_state_d = False

circle_list = []

class Circle:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.radius = 80
        self.velocity_x = vx
        self.velocity_y = vy
        self.collided = False
        #Phase: 1=biggest   2=medium   3=smallest
        self.phase = 1

    def draw(self):
        n = 20
        alpha = math.pi / n * 2
        angle = 0
        glBegin(GL_POLYGON)
        for i in range(n):
            glVertex2f(self.x + self.radius * math.cos(angle), self.y + self.radius * math.sin(angle))
            angle = angle + alpha
        glEnd()

    def collision(self, chain):
        if -self.radius <= self.x - chain.x <= self.radius and self.y <= chain.y2:
            self.collided = True
        distance_square = (self.x - chain.x) ** 2 + (self.y - chain.y2) ** 2
        if distance_square <= self.radius ** 2:
            self.collided = True

        if self.collided:
            chain.y2 = 0

            if self.phase < 3:
                c1 = Circle(self.x, self.y, self.velocity_x, self.velocity_y)
                c1.radius = int(self.radius / 2)
                c1.phase = self.phase + 1
                circle_list.append(c1)

                c2 = Circle(self.x, self.y, -self.velocity_x, self.velocity_y)
                c2.radius = int(self.radius / 2)
                c2.phase = self.phase + 1
                circle_list.append(c2)

            self.radius = 0
            self.collided = False

    def update(self, dt):
        self.x = self.x + self.velocity_x * dt
        self.y = self.y + self.velocity_y * dt
        if self.x < self.radius:
            self.x = self.radius
            self.velocity_x = - self.velocity_x
        if self.x > 1000 - self.radius:
            self.x = 1000 - self.radius
            self.velocity_x = - self.velocity_x
        if self.y < 0 + self.radius:
            self.y = self.radius
            self.velocity_y = - self.velocity_y
        if self.y > 600 - self.radius:
            self.y = 600 - self.radius
            self.velocity_y = - self.velocity_y


circle1 = Circle(300, 200, -90, 80)
circle2 = Circle(700, 200, 90, 80)
circle_list.append(circle1)
circle_list.append(circle2)



@window.event
def on_key_press(symbol, modifiers):
    global key_state_a, key_state_d
    if symbol == pyglet.window.key.A:
        key_state_a = True
    elif symbol == pyglet.window.key.D:
        key_state_d = True
    elif symbol == pyglet.window.key.SPACE:
        chain = Chain(player.x)
        chain_list.append(chain)
@window.event
def on_key_release(symbol, modifiers):
    global key_state_a, key_state_d
    if symbol == pyglet.window.key.A:
        key_state_a = False
    elif symbol == pyglet.window.key.D:
        key_state_d = False


class Player:
    def __init__(self):
        self.x = 500
    def draw(self):
        if 990 >= self.x >= 10:
            glBegin(GL_QUADS)
            glVertex2f(self.x - 10, 60)
            glVertex2f(self.x + 10, 60)
            glVertex2f(self.x + 10, 0)
            glVertex2f(self.x - 10, 0)
            glEnd()
    def update(self, dt):
        if key_state_a and self.x >= 20:
            self.x = self.x - 300 * dt
        if key_state_d and self.x <= 980:
            self.x = self.x + 300 * dt

player = Player()


class Chain:
    def __init__(self, x):
        self.x = x
        self.y1 = 0
        self.y2 = 10
        self.deleted = False
    def draw(self):
        if not self.deleted:
            glBegin(GL_LINES)
            glVertex2f(self.x, self.y1)
            glVertex2f(self.x, self.y2)
            glEnd()
    def update(self, dt):
        if self.y2 < 10 or self.y2 >= 600:
            self.deleted = True
            self.y2 = 0    # totally unnecessary
        else:
            self.y2 = self.y2 + 200 * dt

chain_list = []


@window.event
def on_draw():
    window.clear()

    player.draw()

    for c in circle_list:
        c.draw()
    for c in chain_list:
        c.draw()

def update(dt):

    player.update(dt)

    for c in circle_list:
        c.update(dt)
    for c in chain_list:
        c.update(dt)

    for circle in circle_list:
        for chain in chain_list:
            circle.collision(chain)


pyglet.clock.schedule_interval(update, 1 / 120)

pyglet.app.run()
