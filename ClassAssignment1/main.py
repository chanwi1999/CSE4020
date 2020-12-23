import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# ClassAssignment1-1 #

gCamAng = 0.
gCamHeight = 0.
gPress = 0
gFov = 5.
gLastX = 240.
gLastY = 240.
gXoffset = 0.
gYoffset = 0.

def drawCube():
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
 
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-20.,0.,0.]))
    glVertex3fv(np.array([20.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,20.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,-20.]))
    glVertex3fv(np.array([0.,0.,20.]))
    glEnd()

def drawPlaneXZ():
    glBegin(GL_LINES)
    glColor3ub(100, 100, 100)
    arr = np.arange(-20.,20.,1.)
    for i in range(0, len(arr)):
        if arr[i]==0: # to make the x-axis and z-axis colors clear
            continue
        glVertex3fv(np.array([arr[i],0.,20.]))
        glVertex3fv(np.array([arr[i],0.,-20.]))
        glVertex3fv(np.array([20.,0.,arr[i]]))
        glVertex3fv(np.array([-20.,0.,arr[i]]))
    glEnd()

def render():
    global gCamAng, gCamHeight

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glLoadIdentity()

    glTranslatef(gXoffset, gYoffset, 0) # panning
    glOrtho(-gFov,gFov, -gFov,gFov, -100,100) # zoom in-out
    gluLookAt(1*np.sin(gCamAng),gCamHeight,1*np.cos(gCamAng), 0,0,0, 0,1,0) # orbit
    
    drawPlaneXZ()
    drawFrame()

    glColor3ub(255, 255, 255)
    drawCube()

def mouse_button_callback(window, button, action, mods):
    global gCamAng, gCamHeight, gPress

    if action == glfw.PRESS: 
        if button == glfw.MOUSE_BUTTON_LEFT:
            gPress = 1
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            gPress = 2

    elif action == glfw.RELEASE:
        gPress = 0


def scroll_callback(window, xoffset, yoffset): # zoom in-out
    global gFov

    if yoffset < 0:
        if gFov+.5 >= 45:
            gFov = gFov
        else:
            gFov += .5
    else:
        if gFov-.5 <= 0 :
            gFov = gFov
        else:
            gFov -= .5

        
def cursor_position_callback(window, xpos, ypos):
    global gLastX, gLastY, gCamAng, gCamHeight, gXoffset, gYoffset

    xoffset = xpos - gLastX
    yoffset = gLastY - ypos
    gLastX = xpos
    gLastY = ypos

    if gPress == 1: # orbit
        gCamAng += xoffset * 0.003
        gCamHeight += yoffset * 0.003
    
    elif gPress == 2: # panning
        gXoffset += xoffset * 0.003
        gYoffset += yoffset * 0.003


# ClassAssignment1-2 #

gCamAng2 = np.radians(60)
gCamHeight2 = 0.5
leg_angle = 0.
arm_angle = 0.

def drawSphere(numLats, numLongs):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)
        
        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        
        # Use Quad strips to draw the sphere
        glBegin(GL_QUAD_STRIP)

        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng) 
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)

        glEnd()

def render2():
    global gCamAng2, gCamHeight2, leg_angle, arm_angle
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2,2, -2,2, -10,10)
    gluLookAt(1*np.sin(gCamAng2),gCamHeight2,1*np.cos(gCamAng2), 0,0,0, 0,1,0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    t = glfw.get_time()
    leg_angle = np.sin(t + np.pi)*30.
    arm_angle = -np.sin(t)*30.

    glPushMatrix()

    # body 1
    glPushMatrix()
    glScalef(.2, .5, .2)
    glColor3ub(200, 200, 200)
    drawCube()
    glPopMatrix()

    # head 1-6
    glPushMatrix()
    glTranslatef(0., .7, 0.)

    glPushMatrix()
    glScalef(.2, .2, .2)
    glColor3ub(255, 255, 0)
    drawSphere(12, 12)
    glPopMatrix()

    # finish 1-6
    glPopMatrix()
   
    # left upleg 1-2
    glPushMatrix()
    glRotatef(leg_angle, 0, 0, 1)
    glTranslatef(0, -.8, .1)

    glPushMatrix()
    glScalef(.1, .3, .1)
    glColor3ub(255, 0, 0)
    drawCube()
    glPopMatrix()

    # left downleg 1-2-7
    glPushMatrix()
    glRotatef(arm_angle, 0, 0, 1)
    glTranslatef(0, -.55, 0)

    glPushMatrix()
    glScalef(.1, .25, .1)
    glColor3ub(200, 0, 0)
    drawCube()
    glPopMatrix()

    # left foot 1-2-7-11
    glPushMatrix()
    glRotatef(leg_angle, 0, 0, 1)
    glTranslatef(.1, -.3, 0)

    glPushMatrix()
    glScalef(.2, .05, .1)
    glColor3ub(150, 0, 0)
    drawSphere(12,12)
    glPopMatrix()

    # finish 1-2-7-11
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

    # right upleg 1-3
    glPushMatrix()
    glRotatef(-leg_angle, 0, 0, 1)
    glTranslatef(0, -.8, -.1)

    glPushMatrix()
    glScalef(.1, .3, .1)
    glColor3ub(0, 255, 0)
    drawCube()
    glPopMatrix()

    # right downleg 1-3-8
    glPushMatrix()
    glRotatef(-arm_angle, 0, 0, 1)
    glTranslatef(0, -.55, 0)

    glPushMatrix()
    glScalef(.1, .25, .1)
    glColor3ub(0, 200, 0)
    drawCube()
    glPopMatrix()

    # right foot 1-3-8-12
    glPushMatrix()
    glRotatef(-leg_angle, 0, 0, 1)
    glTranslatef(.1, -.3, 0)

    glPushMatrix()
    glScalef(.2, .05, .1)
    glColor3ub(0, 150, 0)
    drawSphere(12,12)
    glPopMatrix()

    # finish 1-3-8-12
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

    # left uparm 1-4
    glPushMatrix()
    glRotatef(arm_angle, 0, 0, 1)
    glTranslatef(0, .75, .3)

    glPushMatrix()
    glScalef(.1, .25, .1)
    glColor3ub(0, 0, 255)
    drawCube()
    glPopMatrix()

    # left downarm 1-4-9
    glPushMatrix()
    glRotatef(leg_angle, 0, 0, 1)
    glTranslatef(0, .5, 0)

    glPushMatrix()
    glScalef(.1, .25, .1)
    glColor3ub(0, 0, 200)
    drawCube()
    glPopMatrix()

    # finish 1-4-9
    glPopMatrix()
    glPopMatrix()

    # right uparm 1-5
    glPushMatrix()
    glRotatef(-arm_angle, 0, 0, 1)
    glTranslatef(0, .75, -.3)

    glPushMatrix()
    glScalef(.1, .25, .1)
    glColor3ub(0, 255, 255)
    drawCube()
    glPopMatrix()

    # right downarm 1-5-10
    glPushMatrix()
    glRotatef(-leg_angle, 0, 0, 1)
    glTranslatef(0, .5, 0)

    glPushMatrix()
    glScalef(.1, .25, .1)
    glColor3ub(0, 200, 200)
    drawCube()
    glPopMatrix()

    # finish 1-5-10
    glPopMatrix()
    glPopMatrix()

    glPopMatrix()

def main():

    # ClassAssignment1-1 #
    if not glfw.init():
        return
    
    window = glfw.create_window(640, 640, '2018008177_1', None, None) 
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

    # ClassAssignment1-2 #
    if not glfw.init():
        return

    window2 = glfw.create_window(640, 640, '2018008177_2', None, None)
    if not window2:
        glfw.terminate()
        return

    glfw.make_context_current(window2)

    while not glfw.window_should_close(window2):
        glfw.poll_events()
        render2()
        glfw.swap_buffers(window2)      

    glfw.terminate()

if __name__ == "__main__":
    main()

