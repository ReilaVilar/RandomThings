import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyglet.gl import *
import math

window = pyglet.window.Window(width=1280, height=800)



def square():
    glBegin(GL_QUADS)
    glTexCoord2f(4, 0)
    glVertex3f(-0.5, -0.5, 0)
    glTexCoord2f(4, 4)
    glVertex3f(0.5, -0.5, 0)
    glTexCoord2f(0, 4)
    glVertex3f(0.5, 0.5, 0)
    glTexCoord2f(0, 0)
    glVertex3f(-0.5, 0.5, 0)
    glEnd()



once = True
front = -5

@window.event
def on_draw():
    global once, angle,front
    glClearColor(0.25, 0.6, 1, 1)
    window.clear()

    if once:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, 1280 / 800, 0.1, 100)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        once = False


    glLoadIdentity()
    gluLookAt(0, 0, -10, 0, 0, 0, 0, 1, 0)
    glTranslatef(0, 0, -5)


    glDisable(GL_BLEND)
    glColor4ub(255, 255, 255, 0)
    square()

    glEnable(GL_BLEND)
    glPushMatrix()
    glColor4ub(255, 0, 0, 128)
    glTranslatef(front,0,-1)
    square()
    glPopMatrix()


def update(dt):
    global front


    front = front +dt


pyglet.clock.schedule(update)
pyglet.app.run()

