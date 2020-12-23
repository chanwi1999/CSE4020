import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import ctypes

gCamAng = 0.
gCamHeight = 5.
gPress = 0
gFov = 10.

eye = [0., 0., 0.]
target = [0., 0., 0.]
upV = [0., 1., 0.]

gLastX = 240.
gLastY = 240.

def drawPlaneXZ():
    glBegin(GL_LINES)
    glColor3ub(100, 100, 100)
    arr = np.arange(-20.,20.,1.)
    for i in range(0, len(arr)):
        glVertex3fv(np.array([arr[i],0.,20.]))
        glVertex3fv(np.array([arr[i],0.,-20.]))
        glVertex3fv(np.array([20.,0.,arr[i]]))
        glVertex3fv(np.array([-20.,0.,arr[i]]))
    glEnd()

def mouse_button_callback(window, button, action, mods):
    global gPress
    
    if action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_LEFT:
            gPress = 1
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            gPress = 2
    elif action == glfw.RELEASE:
        gPress = 0

def scroll_callback(window, xoffset, yoffset):
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
    global gLastX, gLastY, gCamAng, gCamHeight, gPress, target, gFov, upV

    xoffset = xpos - gLastX
    yoffset = ypos - gLastY
    gLastX = xpos
    gLastY = ypos

    if gPress == 1: # orbit
        gCamAng += xoffset * .1
        gCamHeight += yoffset * .1

    # change method for lighting
    if gPress == 2: # panning
        eye = [ target[0] + (gFov*np.cos(np.radians(gCamHeight))*np.cos(np.radians(gCamAng))),
		        target[1] + (gFov*np.sin(np.radians(gCamHeight))),
		        target[2] + (gFov*np.cos(np.radians(gCamHeight))*np.sin(np.radians(gCamAng))) ]
        at = np.array(target)
        up = np.array(upV)

        w = (eye - at) / np.sqrt(np.dot(eye - at, eye - at))
        u = np.cross(up, w) / np.sqrt(np.dot(np.cross(up, w), np.cross(up, w)))
        v = np.cross(w, u)

        target += xoffset * -u * 0.001 * gFov
        target += yoffset *  v * 0.001 * gFov


# ClassAssignment2 #

gPath = ''
gFave = [0, 0, 0]

gVertexArrayIndexed = None
gIndexArray = None
gNormal = None
gNormal2 = None

gObj = 0
gZkey = 1
gSkey = 1

def render():
    global gObj, gZkey, eye, target, upV

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    if gZkey==1: # wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else: # solid
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # change method for lighting
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    eye = [ target[0] + (gFov*np.cos(np.radians(gCamHeight))*np.cos(np.radians(gCamAng))),
            target[1] + (gFov*np.sin(np.radians(gCamHeight))),
            target[2] + (gFov*np.cos(np.radians(gCamHeight))*np.sin(np.radians(gCamAng))) ]
    gluLookAt(eye[0],eye[1],eye[2], target[0],target[1],target[2], upV[0],upV[1],upV[2])

    # grid plane
    drawPlaneXZ()

    # light
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

    # light 0
    glPushMatrix()
    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
	
    # light 1
    glPushMatrix()
    glRotatef(120,0,1,0)
    lightPos = (-3.,-4.,5.,1.) 
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()

    # light 2
    glPushMatrix()
    glRotatef(240,0,1,0)
    lightpos = (-3.,4.,-5.,1.)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos)
    glPopMatrix()
	
    ambientLightColor = (.1,.0,.0,1.)
    diffuseLightColor = (.5,.0,.0,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor)
    
    ambientLightColor1 = (.0,.1,.0,1.)
    diffuseLightColor1 = (.0,.5,.0,1.)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor1)

    ambientLightColor2 = (.0,.0,.1,1.)
    diffuseLightColor2 = (.0,.0,.5,1.)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor2)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, diffuseLightColor2)

    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
	
    glPushMatrix()

    if gObj==1:
        drawObj_glDrawElements()
    glPopMatrix()

    glDisable(GL_LIGHTING)

def drop_callback(window, paths):
    global gPath, gVertexArrayIndexed, gIndexArray, gNormal, gNormal2, gObj
    
    gPath = ''.join(paths)
    gVertexArrayIndexed, gIndexArray, gNormal, gNormal2 = createVertexAndIndexArrayIndexed()
    print_inform()
    gObj = 1

def key_callback(window, key, scancode, action, mods):
    global gZkey, gSkey

    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_Z:
            gZkey *= -1
        elif key==glfw.KEY_S:
            gSkey *= -1
   
def drawObj_glDrawElements():
    global gVertexArrayIndexed, gIndexArray, gNormal, gNormal2, gSkey
    
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    narr = gNormal
    narr2 = gNormal2
    
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)
    
    if gSkey==1: # shading using normal data
        glNormalPointer(GL_FLOAT, 3*varr.itemsize, narr)
    else: # forced smooth shading
        glNormalPointer(GL_FLOAT, 3*varr.itemsize, narr2)

    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def print_inform():
    global gPath, gFace
    
    print("File name: " + gPath)
    print("Total number of faces: " + str(gFace[0] + gFace[1] + gFace[2]))
    print("Number of faces with 3 vertices: " + str(gFace[0]))
    print("Number of faces with 4 vertices: " + str(gFace[1]))
    print("Number of faces more than 4 vertices: " + str(gFace[2]))

def createVertexAndIndexArrayIndexed():
    global gPath, gFace
    
    v_coords = []
    n_coords = []

    v_index = []
    n_index = []

    tmp_v = []
    tmp_n = []

    gFace = [0, 0, 0]

    for line in open(gPath, 'r'):
        if line.startswith('#'):
            continue

        values = line.split()
        valNum = values[1:]
        
        if not values:
            continue

        if values[0]=='v':
            tmp = [float(values[1]), float(values[2]), float(values[3])]
            v_coords.append(tmp)
        if values[0]=='vn':
            tmp = [float(values[1]), float(values[2]), float(values[3])]
            n_coords.append(tmp)
        if values[0]=='f':

            if len(valNum) == 3:
                gFace[0] += 1
            elif len(valNum) == 4:
                gFace[1] += 1
            else:
                gFace[2] += 1

            for i in range(1, len(valNum)-1):
                face_i = []
                norm_i = []

                for v in values[i:i+2]:
                    w = v.split('/')
                    face_i.append(int(w[0])-1)
                    norm_i.append(int(w[2])-1)
                v = values[len(valNum)]
                w = v.split('/')
                face_i.append(int(w[0])-1)
                norm_i.append(int(w[2])-1)

                if i != 1: # n-polygon
                    tmp_v.append(face_i)
                    tmp_n.append(norm_i)
                else:
                    v_index.append(face_i)
                    n_index.append(norm_i)

    # n-polygon
    for i in range(len(tmp_v)-1, -1, -1):
        v_index.insert(len(n_coords), tmp_v[i])
        n_index.insert(len(n_coords), tmp_n[i])

    narr = [[0.]*3]*len(v_coords)
    narr2 = [[0.]*3]*len(v_coords)
    for i in range(len(v_index)):
        t1 = np.subtract(v_coords[v_index[i][1]], v_coords[v_index[i][0]])
        t2 = np.subtract(v_coords[v_index[i][2]], v_coords[v_index[i][0]])

        nv = np.cross(t1, t2)
        nv = nv / np.sqrt(np.dot(nv, nv))

        for j in range(3):
            narr[v_index[i][j]] = n_coords[n_index[i][j]]
            narr2[v_index[i][j]] += nv

    for i in range(len(v_coords)):
        narr2[i] = narr2[i] / np.sqrt(np.dot(narr2[i], narr2[i]))
    
    varr = np.array(v_coords, 'float32')
    iarr = np.array(v_index)
    narr = np.array(narr)
    narr2 = np.array(narr2)
    
    return varr, iarr, narr, narr2

def main():
    if not glfw.init():
        return

    window = glfw.create_window(640, 640, '2018008177', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_drop_callback(window, drop_callback)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
