# After running the application, you need to create new map
#
# press SPACE to create a new map (can create as many times as you want and in any step)
# press ENTER for next step
# press A to complete the path instantly
#
# You can observe terminal to see current path
#
# pip install pyglet
# pip install opengl
# 


import math
import copy
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyglet.gl import *



WIDTH = 600
HEIGHT = 400
MAP = []
PATH = []
SIZE = 20
COST = 0
STEP = 0
CAND = None

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.choosen = False
        self.inPath = False
    def draw(self):
        x_center, y_center = self.x, self.y
        sides = 32
        radius = 3
        if self.choosen:
            glColor3ub(255, 0, 0)
        else:
            glColor3ub(255,255,255)
            
        glBegin(GL_POLYGON)
        for i in range(100):
            angle = i*2*math.pi/sides
            cosine = radius * math.cos(angle)+x_center
            sine = radius * math.sin(angle)+y_center
            glVertex2f(cosine, sine)
        glEnd()

def distanceOfTwo(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

def calculateCost(path):
    cost = 0
    N = len(path)
    for i in range(N):
        p1 = path[i]
        if i == N-1:
            p2 = path[0]
        else:
            p2 = path[i+1]
        cost += round(distanceOfTwo(p1, p2))
    return cost

def createMap(num):
    global MAP
    MAP.clear()
    for i in range(num):
        x = random.randint(20, WIDTH-20)
        y = random.randint(50, HEIGHT-50)
        
        glPushMatrix()
        p = Point(x,y)  
        glPopMatrix() 
        MAP.append(p) 
        

def insertCandidate(candidate):
    optimalCost = math.inf
    optimalPath = []

    N = len(PATH)
    for i in range(0,N):
        tempPath =  copy.copy(PATH)
        tempPath.insert(i,candidate)
        cost = calculateCost(tempPath)
        if cost < optimalCost:
            optimalCost = cost
            optimalPath = copy.copy(tempPath)
    return optimalCost, optimalPath

def getFarthestPoint():
    maxDistance = 0
    candidate = None
    for p in MAP:
        if not p.inPath:
            dist = 0
            for i in PATH: 
                dist += distanceOfTwo(p, i)
            if dist > maxDistance:
                maxDistance = dist
                candidate = p
    return candidate

def drawPath():
    glColor3ub(255,255,255)
    for i in range(len(PATH)):
        p1 = PATH[i]
        if i == len(PATH)-1:
            p2 = PATH[0]
        else:
            p2 = PATH[i+1]
        line(p1, p2)

def stepByStep():
    global MAP, PATH, STEP, CAND, COST
    window.clear()
    CAND.choosen = False
    for p in MAP:
        p.draw()

    if len(PATH)-1 == SIZE:
        drawLabel("Completed", WIDTH/2, 10)
        drawPath()
    else:
        if STEP%2==0:
            CAND = getFarthestPoint()
            CAND.choosen = True
            CAND.draw()
            drawPath()
            if len(PATH) == 2:
                glColor3ub(255,0,0)
                line(PATH[0], PATH[1])
            elif len(PATH) >= 3:
                newPath = insertCandidate(CAND)[1]
                glColor3ub(255,0,0)
                line(newPath[newPath.index(CAND)-1], newPath[newPath.index(CAND)+1])
        elif STEP%2==1:
            newPath = insertCandidate(CAND)
            CAND.inPath = True
            PATH = newPath[1]
            COST = newPath[0]
            drawPath()
    drawLabel(COST, 10, HEIGHT-20)
    STEP += 1

def newMap():
    global MAP, PATH, CAND, STEP, COST
    window.clear()
    PATH.clear()
    createMap(SIZE)
    for p in MAP:
        p.draw()
    CAND = copy.copy(MAP[random.randint(0, SIZE-1)])
    CAND.choosen = True
    CAND.inPath = True
    CAND.draw()
    PATH.append(CAND)
    STEP = 0
    COST = 0
    drawLabel(COST, 10, HEIGHT-20)

def drawCompletePath():
    global SIZE, PATH
    while len(PATH) <= SIZE:
        stepByStep()

def drawLabel(tag, x, y):
    label = pyglet.text.Label(str(tag),
                        font_name='Times New Roman',
                        font_size=18,
                        x=x, y=y)
    label.draw()

################# GUI

#window = window.Window(width=WIDTH, height=HEIGHT)
window = pyglet.window.Window(width=WIDTH, height=HEIGHT)


def line(p1, p2):
    
    glBegin(GL_LINES)
    glVertex2f(p1.x,p1.y)
    glVertex2f(p2.x,p2.y)
    glEnd()



@window.event
def on_key_press(key, e):
    if key == pyglet.window.key.ENTER:
        stepByStep()
        print("______________________")
        for i in range(len(PATH)):
            print(i,[PATH[i].x,PATH[i].y])
    elif key == pyglet.window.key.SPACE:
        newMap()
    elif key == pyglet.window.key.A:
        drawCompletePath()


pyglet.app.run()
