import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

global gKey
gKey = []


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
 # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
 
    global gKey
    for i in gKey:
        if i==2: # 'Q'
            glTranslatef(-0.1, 0., 0.)
        elif i==3: # 'E'
            glTranslatef(0.1, 0., 0.)
        elif i==4: # 'A'
            glRotatef(10, 1., 0., 1.)
        elif i==5: # 'D'
            glRotatef(-10, 1., 0., 1.)
        elif i==1:            
            gKey.clear()
    drawTriangle()

    
def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()


def key_callback(window, key, scancode, action, mods):
    global gKey
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_Q:
            gKey.insert(0,2)
        elif key==glfw.KEY_E:
            gKey.insert(0,3)
        elif key==glfw.KEY_A:
            gKey.insert(0,4)
        elif key==glfw.KEY_D:
            gKey.insert(0,5)
        elif key==glfw.KEY_1:
            gKey.insert(0,1)


def main():
    if not glfw.init():
        return

    window = glfw.create_window(480,480,'2018008177', None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()

