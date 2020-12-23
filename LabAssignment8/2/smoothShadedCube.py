import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gCamAng = 0
gCamHeight = 1.
gLightColor = (1., 1., 1., 1.)
gObjectColor = (1., 0., 0., 1.)
gVertexArrayIndexed = None
gIndexArray = None

def render():
    global gCamAng, gCamHeight
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    drawFrame()

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_NORMALIZE)
    glPushMatrix()

    t = glfw.get_time()

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, gLightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, gLightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)

    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, gObjectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 50)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()

    drawCube_glDrawElements()
    glPopMatrix()

    glDisable(GL_LIGHTING)


def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)
    # lab8-2
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def createVertexAndIndexArrayIndexed():
    #lab8-2
    a = 0.4082482904639631
    b = 0.5773502691896258
    c = 0.8164965809277261
    varr = np.array([
            (-1, 1, 1, -b, b, b),
            (1, 1, 1, c, a, a),
            (1, -1, 1, a, -a, c),
            (-1, -1, 1, -a, -c, a),
            (-1, 1, -1, -a, a, -c),
            (1, 1, -1, a, c, -a),
            (1, -1, -1, b, -b, -b),
            (-1, -1, -1, -c, -a, -a)
            ], 'float32')

    iarr = np.array([
            (0, 2, 1),
            (0, 3, 2),
            (4, 5, 6),
            (4, 6, 7),
            (0, 1, 5),
            (0, 5, 4),
            (3, 6, 2),
            (3, 7, 6),
            (1, 2, 6),
            (1, 6, 5),
            (0, 7, 3),
            (0, 4, 7)
            ])

    return varr, iarr

def drawFrame():
    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

def main():
    global gVertexArraySeparate

    if not glfw.init():
        return
    
    global gVertexArrayIndexed, gIndexArray

    window = glfw.create_window(480,480,'2018008177', None,None)    
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed() 

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
