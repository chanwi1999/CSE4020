import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render(M):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
 # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)

 # draw point p
    glBegin(GL_POINTS)
    glColor3ub(255, 255, 255)
    glVertex2fv(M @ np.array([.7, .7]))
    glEnd()

 # draw vector v
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    glVertex2fv(M @ np.array([0., 0.]))
    glVertex2fv(M @ np.array([.4, .4]))
    glEnd()


def main():
        if not glfw.init():
                return
        window = glfw.create_window(480,480,"2018008177",None,None)
        if not window:
                glfw.terminate()
                return
		
        glfw.make_context_current(window)
        glfw.swap_interval(1)

        while not glfw.window_should_close(window):
                glfw.poll_events()

                t = glfw.get_time()
                th = t*np.radians(60)
                M = np.array([[np.cos(th), -np.sin(th)],
                        [np.sin(th), np.cos(th)]])
                render(M)
                glfw.swap_buffers(window)
        glfw.terminate()

if __name__== "__main__":
        main()
