### Parkour ###
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyglet.gl import *
import random
import math
window = pyglet.window.Window(width=1280, height=800)

w_pressed = False
a_pressed = False
s_pressed = False
d_pressed = False

once = True
angle_x = 0
angle_y = 0
eye_x = 0
eye_y = 4
eye_z = 0
jump_state = 0
jump_on = False


def square():
    glBegin(GL_QUADS)
    glVertex3f(-0.5, -0.5, 0)
    glVertex3f(0.5, -0.5, 0)
    glVertex3f(0.5, 0.5, 0)
    glVertex3f(-0.5, 0.5, 0)
    glEnd()


def cube():
    glBegin(GL_QUADS)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)

    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)

    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)

    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-.5, 0.5, 0.5)

    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)

    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glEnd()


class Tree:
    def __init__(self):
        self.x = random.randint(-100, 100)
        self.y = 0
        self.z = random.randint(-100, 100)

    def draw(self):
        glPushMatrix()
        glColor3ub(170, 90, 90)
        glTranslatef(self.x, self.y, self.z)
        glPushMatrix()
        glScalef(0.5, 4.2, 0.5)
        cube()

        glPopMatrix()
        glColor3ub(83, 111, 27)
        glTranslatef(0, 2.8, 0)
        glScalef(1.8, 1.5, 1.8)
        cube()
        glPopMatrix()

    def collision(self):
        global eye_x, eye_z
        optimal_distance = 2

        if self.x - optimal_distance <= eye_x <= self.x + optimal_distance and \
                self.z - optimal_distance <= eye_z <= self.z + optimal_distance:

            if eye_y < self.y + 5:
                dtop = eye_x - (self.x - optimal_distance)
                dbottom = (self.x + optimal_distance) - eye_x
                dright = (self.z + optimal_distance) - eye_z
                dleft = eye_z - (self.z - optimal_distance)

                if dtop < dbottom and dtop < dleft and dtop < dright:
                    eye_x = self.x - optimal_distance
                elif dbottom < dtop and dbottom < dleft and dbottom < dright:
                    eye_x = self.x + optimal_distance
                elif dright < dtop and dright < dbottom and dright < dleft:
                    eye_z = self.z + optimal_distance
                elif dleft < dtop and dleft < dbottom and dleft < dright:
                    eye_z = self.z - optimal_distance

tree_list = []
for i in range(50):
    tree = Tree()
    tree_list.append(tree)


class Platform:
    def __init__(self):
        self.x = random.randint(-100, 100)
        self.y = random.randint(2, 14)
        self.z = random.randint(-100, 100)

        self.red = random.randint(150, 224)
        self.green = random.randint(16, 64)
        self.blue = random.randint(16, 64)

    def draw(self):
        glPushMatrix()
        glColor3ub(self.red, self.green, self.blue)
        glTranslatef(self.x, self.y, self.z)
        glPushMatrix()
        glScalef(10, 1, 10)
        cube()
        glPopMatrix()
        glPopMatrix()

    def collision(self):
        global eye_x, eye_y, eye_z
        global jump_state, jump_on
        optimal_distance = 7

        if self.x - optimal_distance < eye_x < self.x + optimal_distance and \
                self.z - optimal_distance < eye_z < self.z + optimal_distance:

            # On Platform
            if self.y + 3.9 <= eye_y <= self.y + 4.2:
                eye_y = self.y + 4.2
                jump_state = 0
            # In Platform
            elif self.y - 1.8 <= eye_y < self.y + 3.9:
                dfront = eye_x - (self.x - optimal_distance)
                dback = (self.x + optimal_distance) - eye_x
                dright = (self.z + optimal_distance) - eye_z
                dleft = eye_z - (self.z - optimal_distance)

                if dfront < dback and dfront < dleft and dfront < dright:
                    eye_x = self.x - optimal_distance
                elif dback < dfront and dback < dleft and dback < dright:
                    eye_x = self.x + optimal_distance
                elif dright < dfront and dright < dback and dright < dleft:
                    eye_z = self.z + optimal_distance
                elif dleft < dfront and dleft < dback and dleft < dright:
                    eye_z = self.z - optimal_distance
            # Under Platform
            if self.y - 2 < eye_y < self.y - 1.8:
                eye_y = self.y - 2
                jump_on = False




platform_list = []
for i in range(25):
    p = Platform()
    platform_list.append(p)

p1 = Platform()
p1.x = 10
p1.y = 3
p1.z = 10
p1.red = 0
p1.green = 64
p1.blue = 64
platform_list.append(p1)

p2 = Platform()
p2.x = 30
p2.y = 7
p2.z = 15
p2.red = 0
p2.green = 64
p2.blue = 120
platform_list.append(p2)

p3 = Platform()
p3.x = 45
p3.y = 13
p3.z = 10
p3.red = 0
p3.green = 64
p3.blue = 160
platform_list.append(p3)

class Cloud:
    def __init__(self):
        self.x = random.randint(-100, 100)
        self.y = random.randint(20, 30)
        self.z = random.randint(-100, 100)

    def draw(self):
        glPushMatrix()
        glColor3ub(255, 255, 255)
        glTranslatef(self.x, self.y, self.z)
        glPushMatrix()
        glScalef(3, 1, 2)
        cube()

        glPopMatrix()

        glColor3ub(255, 255, 255)
        glTranslatef(2, -1, 2)
        glScalef(3, 1, 4)
        cube()
        glPopMatrix()

cloud_list = []
for i in range(50):
    cloud = Cloud()
    cloud_list.append(cloud)


rain_speed = 60
class Rain:
    def __init__(self):
        self.x = random.randint(-100, 100)
        self.y = random.randint(0, 60)
        self.z = random.randint(-100, 100)

    def draw(self):
        glColor3ub(0, 150, 255)
        glBegin(GL_LINES)
        glVertex3f(self.x, self.y, self.z)
        glVertex3f(self.x + 1, self.y - 5, self.z)
        glEnd()

    def update(self, dt):
        self.y = self.y - rain_speed * dt
        self.x = self.x + (rain_speed / 5) * dt

        if self.y < 0:
            self.x = random.randint(-100, 100)
            self.y = 60
        elif self.x > 100:
            self.x = random.randint(-100, 100)
            self.y = 60

rain_list = []
for i in range(150):
    rain = Rain()
    rain_list.append(rain)


@window.event
def on_draw():
    global once, eye_x, eye_y, eye_z
    glClearColor(0.7, 0.7, 1, 1)
    window.clear()

    if once:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, 1280/ 800, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        once = False

    lookAt_x = eye_x + math.cos(math.radians(angle_x))
    lookAt_y = eye_y - math.cos(math.radians(angle_y))
    lookAt_z = eye_z + math.sin(math.radians(angle_x))

    glLoadIdentity()
    gluLookAt(eye_x, eye_y, eye_z, lookAt_x, lookAt_y, lookAt_z, 0, 1, 0)

    # Ground
    glPushMatrix()
    glColor3ub(0, 128, 0)
    glTranslatef(0, 0, 0)
    glRotatef(90, 1, 0, 0)
    glScalef(200, 200, 1)
    square()
    glPopMatrix()

    # Tree
    for t in tree_list:
        t.draw()
    # Cloud
    for c in cloud_list:
        c.draw()
    # Rain
    for r in rain_list:
        r.draw()
    # Platform
    for p in platform_list:
        p.draw()

@window.event
def on_key_press(key, e):
    global w_pressed, a_pressed, s_pressed, d_pressed
    global jump_state, jump_on
    if key == pyglet.window.key.W:
        w_pressed = True
    if key == pyglet.window.key.A:
        a_pressed = True
    if key == pyglet.window.key.S:
        s_pressed = True
    if key == pyglet.window.key.D:
        d_pressed = True
    if key == pyglet.window.key.SPACE:
        if jump_state == 0:
            jump_on = True
            jump_state = 1
        elif jump_state == 1:
            jump_on = True
            jump_state = -1

@window.event
def on_key_release(key, e):
    global w_pressed, a_pressed, s_pressed, d_pressed
    if key == pyglet.window.key.W:
        w_pressed = False
    if key == pyglet.window.key.A:
        a_pressed = False
    if key == pyglet.window.key.S:
        s_pressed = False
    if key == pyglet.window.key.D:
        d_pressed = False

@window.event
def on_mouse_motion(x, y, dx, dy):
    global angle_x, angle_y
    angle_x = angle_x + dx * 0.6
    angle_y = angle_y + dy * 0.2


jump_speed = 9
jump_height = 5
def update(dt):
    global w_pressed, a_pressed, s_pressed, d_pressed
    global angle_x
    global eye_x, eye_y, eye_z
    global jump_on, jump_state, jump_speed, jump_height

    if w_pressed:
        eye_x = eye_x + math.cos(math.radians(angle_x)) * 8 * dt
        eye_z = eye_z + math.sin(math.radians(angle_x)) * 8 * dt
    if s_pressed:
        eye_x = eye_x - math.cos(math.radians(angle_x)) * 8 * dt
        eye_z = eye_z - math.sin(math.radians(angle_x)) * 8 * dt
    if a_pressed:
        eye_x = eye_x - math.cos(math.radians(angle_x + 90)) * 8 * dt
        eye_z = eye_z - math.sin(math.radians(angle_x + 90)) * 8 * dt
    if d_pressed:
        eye_x = eye_x - math.cos(math.radians(angle_x - 90)) * 8 * dt
        eye_z = eye_z - math.sin(math.radians(angle_x - 90)) * 8 * dt

    if jump_on:
        eye_y = eye_y + jump_speed * dt
        jump_height = jump_height - jump_speed * dt

        if jump_height <= 0:
            jump_on = False
            jump_height = 4

    # Gravity
    if not jump_on:
        if eye_y > 4:
            eye_y = eye_y - jump_speed * dt
        elif eye_y <= 4:
            eye_y = 4
            jump_state = 0

    for t in tree_list:
        t.collision()
    for r in rain_list:
        r.update(dt)
    for p in platform_list:
        p.collision()


pyglet.clock.schedule_interval(update, 1 / 120)
pyglet.app.run()
