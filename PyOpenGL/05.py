from random import *
from pyglet.gl import *
from OpenGL.GL import *
import math
window = pyglet.window.Window(width=1280, height=800)


def circle():
    n = 20
    angle = 0
    alpha = 2 * math.pi / n
    glBegin(GL_POLYGON)
    for i in range(n):
        glVertex2f(math.cos(angle), math.sin(angle))
        angle = angle + alpha
    glEnd()


rotate_angle = 0
rotate_speed = 40


class Circle:
    def __init__(self):
        self.radius = randint(20, 70)
        self.x = randint(self.radius, 1280 - self.radius)
        self.y = randint(self.radius, 800 - self.radius)
        self.velocity_x = randint(-150, 150)
        self.velocity_y = randint(-150, 150)
        self.dying_count = 255
        self.state = 1
        self.moons = 1

    def draw(self):
        glLoadIdentity()

        if self.state != 1:
            glColor3f(self.dying_count / 400, 0, 0)

        glTranslatef(self.x, self.y, 0)
        glScalef(self.radius, self.radius, 1)
        circle()

        glColor3ub(255, 255, 255)

        initial_position = 0
        if self.moons != 0:
            initial_position = 2 * math.pi / self.moons

        angle = 0
        for i in range(self.moons):
            glLoadIdentity()
            glTranslatef(self.x, self.y, 0)
            glRotatef(rotate_angle, 0, 0, 1)

            # places of moons (not rotation)
            glTranslatef((self.radius + 15) * math.cos(angle), (self.radius + 15) * math.sin(angle), 0)
            glScalef(4, 4, 1)

            circle()
            angle += initial_position

    def collision(self, other):
        distance_square = (self.x - other.x) ** 2 + (self.y - other.y) ** 2
        if distance_square <= (self.radius + other.radius) ** 2:
            if self.moons < other.moons:
                other.moons = other.moons + self.moons
                self.moons = 0
                self.state = 0
            if self.moons > other.moons:
                self.moons = other.moons + self.moons
                other.moons = 0
                other.state = 0
            if self.moons == other.moons:
                if self.radius < other.radius:
                    other.moons = other.moons + self.moons
                    self.moons = 0
                    self.state = 0
                if self.radius > other.radius:
                    self.moons = other.moons + self.moons
                    other.moons = 0
                    other.state = 0

    def update(self, dt):

        if self.dying_count <= 0:
            self.radius = 0

        if self.state != 1:
            self.dying_count = self.dying_count - dt * 500
            return

        self.x = self.x + self.velocity_x * dt
        self.y = self.y + self.velocity_y * dt
        if self.x < self.radius:
            self.x = self.radius
            self.velocity_x = - self.velocity_x
        if self.x > 1280 - self.radius:
            self.x = 1280 - self.radius
            self.velocity_x = - self.velocity_x
        if self.y < 0 + self.radius:
            self.y = self.radius
            self.velocity_y = - self.velocity_y
        if self.y > 800 - self.radius:
            self.y = 800 - self.radius
            self.velocity_y = - self.velocity_y




circle_list = []
for i in range(10):
    cr = Circle()
    circle_list.append(cr)


@window.event
def on_draw():
    window.clear()

    for c in circle_list:
        c.draw()


def update(dt):
    global rotate_angle
    for c in circle_list:
        c.update(dt)

    for i in range(len(circle_list)):
        for j in range(i + 1, len(circle_list)):
            circle_list[i].collision(circle_list[j])

    rotate_angle = rotate_angle + rotate_speed * dt

pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()