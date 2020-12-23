import glfw
from OpenGL.GL import *
import numpy as np

global gComposedM
gComposedM = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])

def render(T):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        glBegin(GL_LINES)
        glColor3ub(255,0,0)
        glVertex2fv(np.array([0.,0.]))
        glVertex2fv(np.array([1.,0.]))
        glColor3ub(0,255,0)
        glVertex2fv(np.array([0.,0.]))
        glVertex2fv(np.array([0.,1.]))
        glEnd()

        glBegin(GL_TRIANGLES)
        glColor3ub(255,255,255)
        glVertex2fv((T @ np.array([0.0,0.5,1.]))[:-1])
        glVertex2fv((T @ np.array([0.0,0.0,1.]))[:-1])
        glVertex2fv((T @ np.array([0.5,0.0,1.]))[:-1])
        glEnd()


def key_callback(window, key, scancode, action, mods):
        
        global gComposedM

        if key==glfw.KEY_1: # identity
            if action==glfw.PRESS:
                gComposedM = np.array([[1., 0., 0.],
                                    [0., 1., 0.],
                                    [0., 0., 1.]])
                render(gComposedM)

        elif key==glfw.KEY_W: # non-uniform scale
            if action==glfw.PRESS:
                R = np.array([[0.9, 0., 0.],
                            [0.,1.,0.],
                            [0.,0.,1.]])
                gComposedM = R @ gComposedM
                render(gComposedM)
    
        elif key==glfw.KEY_E:
            if action==glfw.PRESS:
                R = np.array([[1.1, 0., 0.],
                            [0.,1.,0.],
                            [0.,0.,1.]])
                gComposedM = R @ gComposedM
                render(gComposedM)
        
        elif key==glfw.KEY_S: # rotate
            if action==glfw.PRESS:
                th = np.radians(10)
                R = np.array([[np.cos(th), -np.sin(th), 0.],
                            [np.sin(th), np.cos(th), 0.],
                            [0., 0., 1.]])
                gComposedM = R @ gComposedM
                render(gComposedM)
       
        elif key==glfw.KEY_D:
            if action==glfw.PRESS:
                th = np.radians(-10)
                R = np.array([[np.cos(th), -np.sin(th), 0.],
                            [np.sin(th), np.cos(th), 0.],
                            [0., 0., 1.]])
                gComposedM= R @ gComposedM
                render(gComposedM)
        
        elif key==glfw.KEY_X: # shear
            if action==glfw.PRESS:
                R = np.array([[1., -0.1, 0.],
                            [0.,1.,0.],
                            [0.,0.,1.]])
                gComposedM = R @ gComposedM
                render(gComposedM)
        
        elif key==glfw.KEY_C:
            if action==glfw.PRESS:
                R = np.array([[1., 0.1, 0.],
                            [0.,1.,0.],
                            [0.,0.,1.]])
                gComposedM = R @ gComposedM
                render(gComposedM)
        
        elif key==glfw.KEY_R: # reflection
            if action==glfw.PRESS:
                R = np.array([[1., 0., 0.],
                            [0.,-1.,0.],
                            [0.,0.,1.]])
                gComposedM = R @ gComposedM
                render(gComposedM)


def main():
        if not glfw.init():
                return

        window = glfw.create_window(480,480,"2018008177",None,None)
        if not window:
                glfw.terminate()
                return
		
        glfw.set_key_callback(window, key_callback)
        glfw.make_context_current(window)

        glfw.swap_interval(1)

        render(gComposedM)

        while not glfw.window_should_close(window):
                glfw.poll_events()

                glfw.swap_buffers(window)
        glfw.terminate()

if __name__== "__main__":

        main()

