import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import ctypes

gCamAng = 0.
gCamHeight = 50.
gPress = 0
gFov = 30.

eye = [0., 0., 0.]
target = [0., 0., 0.]
upV = [0., 1., 0.]

gLastX = 0.
gLastY = 0.

gPath = ''

gVertexArrayIndexed = None
gIndexArray = None
gNormal = None

cube = []
cylinder = []
sphere = []

cubepos = [0, 0]
cylinderpos = [60, 0]
spherepos = [120, 0]

cubeAng = 0
cyAng = 0
spAng = 0

cubeFov = 2.
cyFov = 2.
spFov = 2.

gZkey = 0 # change main model
gQkey = 1 # change camera mode

size = 0

def drawPlaneXZ():
    glBegin(GL_LINES)
    glColor3ub(100, 100, 100)
    arr = np.arange(-100.,100.,1.)
    for i in range(0, len(arr)):
        glVertex3fv(np.array([arr[i],0.,100.]))
        glVertex3fv(np.array([arr[i],0.,-100.]))
        glVertex3fv(np.array([100.,0.,arr[i]]))
        glVertex3fv(np.array([-100.,0.,arr[i]]))
    glEnd()

def first_person_view(pos, ang, fov):
    global target, upV, eye, gLastX, gLastY, gCamHeight, gCamAng
    gCamHeight = 10
    gCamAng = ang

    xoffset = pos[0] - gLastX
    xoffset *= 15

    gLastX = pos[0]
    gLastY = pos[1]

    eye = [ target[0] + (fov*np.cos(np.radians(gCamHeight))*np.cos(np.radians(gCamAng))),
            target[1] + (fov*np.sin(np.radians(gCamHeight))),
            target[2] + (fov*np.cos(np.radians(gCamHeight))*np.sin(np.radians(gCamAng))) ]
    at = np.array(target)
    up = np.array(upV)

    w = (eye - at) / np.sqrt(np.dot(eye - at, eye - at))
    u = np.cross(up, w) / np.sqrt(np.dot(np.cross(up, w), np.cross(up, w)))
    v = np.cross(w, u)

    target += xoffset * -u * 0.0025 * fov

def quarter_view(pos):
    global target, gFov, upV, eye, gLastX, gLastY, gCamHeight, gCamAng
    gFov = 30
    gCamHeight = 50
    gCamAng = 0

    xoffset = pos[0] - gLastX
    yoffset = pos[1] - gLastY
    gLastX = pos[0]
    gLastY = pos[1]

    eye = [ target[0] + (gFov*np.cos(np.radians(gCamHeight))*np.cos(np.radians(gCamAng))),
            target[1] + (gFov*np.sin(np.radians(gCamHeight))),
            target[2] + (gFov*np.cos(np.radians(gCamHeight))*np.sin(np.radians(gCamAng))) ]
    at = np.array(target)
    up = np.array(upV)

    w = (eye - at) / np.sqrt(np.dot(eye - at, eye - at))
    u = np.cross(up, w) / np.sqrt(np.dot(np.cross(up, w), np.cross(up, w)))
    v = np.cross(w, u)

    target += xoffset * -u * 0.0025 * gFov
    target += yoffset *  v * 0.0025 * gFov

def render():
    global gZkey, gQkey, gFov, eye, target, upV, gVertexArrayIndexed, gIndexArray, gNormal, size
    global cube, cylinder, sphere, cubeAng, cyAng, spAng
    global cubepos, cylinderpos, spherepos, cubeFov, cyFov, spFov

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # change method for lighting
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 10000)
    
    gFov = 30.
    if gQkey==1:
        if gZkey==0:
            quarter_view(cubepos)
        elif gZkey==1:
            quarter_view(cylinderpos)
        elif gZkey==2:
            quarter_view(spherepos)
    
    elif gQkey==-1:
        if gZkey==0:
            quarter_view(cubepos)
            first_person_view(cubepos, cubeAng, cubeFov)
            gFov = cubeFov
        elif gZkey==1:
            quarter_view(cylinderpos)
            first_person_view(cylinderpos, cyAng, cyFov)
            gFov = cyFov
        elif gZkey==2:
            quarter_view(spherepos)
            first_person_view(spherepos, spAng, spFov)
            gFov = spFov
 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    eye = [ target[0] + (gFov*np.cos(np.radians(gCamHeight))*np.cos(np.radians(gCamAng))),
            target[1] + (gFov*np.sin(np.radians(gCamHeight))),
            target[2] + (gFov*np.cos(np.radians(gCamHeight))*np.sin(np.radians(gCamAng))) ]
    gluLookAt(eye[0],eye[1],eye[2], target[0],target[1],target[2], upV[0],upV[1],upV[2])
    
    # grid plane
    drawPlaneXZ()

    glPushMatrix()
#    glTranslatef(0, 0, 0)
    lighting(0)

    glPushMatrix()
    transformations(cube, cubepos, 0)
    gVertexArrayIndexed, gIndexArray, gNormal = createVertexAndIndexArrayIndexed('cube.obj')
    if gQkey==1 or gZkey != 0:
        drawObj_glDrawElements()
    glPopMatrix()

    glPushMatrix()
    lighting(1)
#    glTranslatef(0, 0, 5)
    
    glPushMatrix()
    glTranslatef(0, 0, 5)
    transformations(cylinder, cylinderpos, 60)
#    glTranslatef(0, 0, 5)
    gVertexArrayIndexed, gIndexArray, gNormal = createVertexAndIndexArrayIndexed('cylinder.obj')
    if gQkey==1 or gZkey != 1:
        drawObj_glDrawElements()
    glPopMatrix()

    glPushMatrix()
    lighting(2)
#    glTranslatef(0, 0, 5)

    glPushMatrix()
    glTranslatef(0, 0, 10)
    transformations(sphere, spherepos, 120)
#    glTranslatef(0, 0, 10)
    gVertexArrayIndexed, gIndexArray, gNormal = createVertexAndIndexArrayIndexed('sphere.obj')
    if gQkey==1 or gZkey != 2:
        drawObj_glDrawElements()
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()

#    colliding()

    glDisable(GL_LIGHTING)

def colliding():
    global gZkey, gQkey, cube, cylinder, sphere, cubepos, cylinderpos, spherepos

    mod = []
    mod2 = []
    mod3 = []
    pos = [0, 0]
    tmp = [0, 0]
    tmp2 = [0, 0]

    if gZkey==0:
        mod = cube
        pos = cubepos
        mod2 = cylinder
        mod3 = sphere
        tmp = cylinderpos
        tmp2 = spherepos
    elif gZkey==1:
        mod = cylinder
        pos = cylinderpos
        mod2 = cubepos
        mod3 = sphere
        tmp = cubepos
        tmp2 = spherepos
    elif gZkey==2:
        mod = sphere
        pos = spherepos
        mod2 = cube
        mod3 = cylinder
        tmp = cubepos
        tmp2 = cylinderpos

    prev = mod[-1]
    act = 0
    if pos[0]>=tmp[0]-40 and (pos[1]<=tmp[1]+40 and pos[1]>=tmp[1]-40):
        act = 1
    elif pos[0]>=tmp2[0]-40 and (pos[1]<=tmp2[1]+40 and pos[1]>=tmp2[1]-40):
        act = 2
    elif pos[0]<=tmp[0] and (pos[1]<=tmp[1]+40 and pos[1]>=tmp[1]-40):
        act = 1
    elif pos[0]<=tmp2[0] and (pos[1]<=tmp2[1]+40 and pos[1]>=tmp2[1]-40):
        act = 2
    '''
    if act==1:
        if prev==2 or prev==3:
            mod2.insert(0,4)
            tmp[0] += 1.3
            mod3.insert(0,5)
            tmp[0] -= 1.3
        elif prev==4 or prev==5:
            mod2.insert(0,2)
            tmp[1] -= 1.
            mod3.insert(0,3)
            tmp[1] += 1.
        elif prev==1:
            mod2.insert(0,4)
            tmp[0] += 1.3
            mod3.insert(0,5)
            tmp[0] -= 1.3
    '''
    res = []
    resp = [0, 0]
    if act != 0:
        if act==1:
            res = mod2
            resp = tmp
        elif act==2:
            res = mod3
            resp = tmp2

        if prev==2:
            res.insert(0,4)
            resp[0] += 1.3
        elif prev==3:
            res.insert(0,5)
            resp[0] -= 1.3
        elif prev==4:
            res.insert(0,2)
            resp[1] += 1.
        elif prev==5:
            res.insert(0,2)
            resp[1] += 1.
       
    '''
    global cubeAng, cyAng, spAng

    if (cubepos[0] >= cylinderpos[0]-20 and (cubepos[1]<=cylinderpos[1]+20 and cubepos[1]>=cylinderpos[1]-20)):
        del cube[-1]
        cubepos[0] -= 1.3
    if (cubepos[0]<=cylinderpos[0]+20 and (cubepos[1]<=cylinderpos[1]+20 and cubepos[1]>=cylinderpos[1]-20)):
        del cube[-1]
        cubepos[0] += 1.3
    elif (cubepos[1]<=spherepos[1]+20 and cubepos[1]>=spherepos[1]-20):
        if cubepos[0]>=spherepos[0]-20:
            cube.insert(0,9)
            cubepos[0] -= 13.
        elif cubepos[0]<=spherepos[0]-40:
            cube.insert(0,10)
            cubepos[0] += 13.
    elif (cylinderpos[1]<=spherepos[1]+20 and cylinderpos[1]>=spherepos[1]-20):
        if cylinderpos[0]>=spherepos[0]-20:
            cylinder.insert(0,9)
            cylinderpos[0] -= 13.
        elif cylinderpos[0]<=spherepos[0]-40:
            cylinder.insert(0,10)
            cylinderpos[0] += 13.
    '''
def lighting(i):
    # light
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    t = glfw.get_time()
    # light 0
    glPushMatrix()
    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()

    # light 1
    glPushMatrix()
    glRotatef(t*(180/np.pi),0,1,0)
    lightPos = (-3.,-4.,5.,1.)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
    glPopMatrix()

    if i==0:
        objectColor = (1., 1., 0., 1.)
    elif i==1:
        objectColor = (0., 1., 1., 1.)
    elif i==2:
        objectColor = (1., 0., 1., 1.)

    ambientLightColor = (.1,.0,.0,1.)
    diffuseLightColor = (.5,.0,.0,1.)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLightColor)

    ambientLightColor1 = (.0,.1,.0,1.)
    diffuseLightColor1 = (.0,.5,.0,1.)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, diffuseLightColor1)

    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

def transformations(model, pos, init):
    for i in model:
        if i==0: # '1'
            model.clear()
        elif i==1: # 'E'
            glRotatef(10, 0., 1., 0.)
        elif i==2: # 'W'
            glTranslatef(-0.1, 0., 0.)
        elif i==3: # 'S'
            glTranslatef(0.1, 0., 0.)
        elif i==4: # 'A'
            glTranslatef(0, 0, 0.1)
        elif i==5: # 'D'
            glTranslatef(0, 0, -0.1)
        elif i==6: # 'R'
            glScalef(1.5, 1.5, 1.5)
        elif i==7: # 'F'
            M = np.identity(4)
            M[0,1] = 1.5
            glMultMatrixf(M)
        elif i==8: # 'C'
            M = np.identity(4)
            M[1,1] = -1
            glMultMatrixf(M)

def key_callback(window, key, scancode, action, mods):
    global gZkey, gQkey, gFov
    global cube, cylinder, sphere, cubeAng, cyAng, spAng
    global cubepos, cylinderpos, spherepos

    if action==glfw.PRESS or action==glfw.REPEAT:
        # change main model
        if key==glfw.KEY_Z:
            gZkey += 1
            if gZkey == 3:
                gZkey = 0
        elif key==glfw.KEY_1:
            if gZkey==0:
                cube.insert(0,0)
            elif gZkey==1:
                cylinder.insert(0,0)
            elif gZkey==2:
                sphere.insert(0,0)
            colliding()
        # rotate main model
        elif key==glfw.KEY_E:
            if gZkey==0:
                cube.insert(0,1)
                cubeAng -= 10
                if cubeAng==360:
                    cubeAng = 0
                x = cubepos[0]
                y = cubepos[1]
                if gQkey==1:
                    cubepos[0] = x*np.cos(np.radians(-10))-y*np.sin(np.radians(-10))
                    cubepos[1] = x*np.sin(np.radians(-10))+y*np.cos(np.radians(-10))
            elif gZkey==1:
                cylinder.insert(0,1)
                cyAng -= 10
                if cyAng==360:
                    cyAng = 0
                '''
                x = cylinderpos[0]
                y = cylinderpos[1]
                if gQkey==1:
                    cylinderpos[0] = x*np.cos(np.radians(-10))-y*np.sin(np.radians(-10))
                    cylinderpos[1] = x*np.sin(np.radians(-10))+y*np.cos(np.radians(-10))
                '''
            elif gZkey==2:
                sphere.insert(0,1)
                spAng -= 10
                if spAng==360:
                    spAng = 0
                '''
                x = spherepos[0]
                y = spherepos[1]
                if gQkey==1:
                    spherepos[0] = x*np.cos(np.radians(-10))-y*np.sin(np.radians(-10))
                    spherepos[1] = x*np.sin(np.radians(-10))+y*np.cos(np.radians(-10))
                '''
            colliding()
        # translate main model
            
        elif key==glfw.KEY_W: # forward
            if gZkey==0:
                moveW(cube, cubepos, cubeAng)
            elif gZkey==1:
                moveW(cylinder, cylinderpos, cyAng)
            elif gZkey==2:
                moveW(sphere, spherepos, spAng)
            colliding()
        elif key==glfw.KEY_S: # back
            if gZkey==0:
                moveS(cube, cubepos, cubeAng)
            elif gZkey==1:
                moveS(cylinder, cylinderpos, cyAng)
            elif gZkey==2:
                moveS(sphere, spherepos, spAng)
            colliding() 
        elif key==glfw.KEY_A: # left
            if gZkey==0:
                moveA(cube, cubepos, cubeAng)
            elif gZkey==1:
                moveA(cylinder, cylinderpos, cyAng)
            elif gZkey==2:
                moveA(sphere, spherepos, spAng)
            colliding()
        elif key==glfw.KEY_D: # right
            if gZkey==0:
                moveD(cube, cubepos, cubeAng)
            elif gZkey==1:
                moveD(cylinder, cylinderpos, cyAng)
            elif gZkey==2:
                moveD(sphere, spherepos, spAng)
            colliding()
        elif key==glfw.KEY_R: # scale
            if gZkey==0:
                cube.insert(0,6)
            elif gZkey==1:
                cylinder.insert(0,6)
            elif gZkey==2:
                sphere.insert(0,6)
        elif key==glfw.KEY_F: # shear
            if gZkey==0:
                cube.insert(0,7)
            elif gZkey==1:
                cylinder.insert(0,7)
            elif gZkey==2:
                sphere.insert(0,7)
        elif key==glfw.KEY_C: # reflect
            if gZkey==0:
                cube.insert(0,8)
            elif gZkey==1:
                cylinder.insert(0,8)
            elif gZkey==2:
                sphere.insert(0,8)
        elif key==glfw.KEY_Q: # change camera mode
            gQkey *= -1

def moveW(model, pos, ang):
    global gQkey, gZkey

    if gQkey==1:
        model.insert(0,2)
    
    elif gQkey==-1:
        if ang==0:
            model.insert(0,2)
        elif ang==-90:
            model.insert(0,5)
        elif ang==-180:
            model.insert(0,3)
        elif ang==-270:
            model.insert(0,4)
    
    if gQkey==1 or ang%(-90):
        pos[1] += 1

def moveS(model, pos, ang):
    global gQkey, gZkey

    if gQkey==1:
        model.insert(0,3)
    
    elif gQkey==-1:
        if ang==0:
            model.insert(0,3)
        elif ang==-90:
            model.insert(0,4)
        elif ang==-180:
            model.insert(0,2)
        elif ang==-270:
            model.insert(0,5)
    
    if (gQkey==1 or ang%(-90)):
        pos[1] -= 1

def moveA(model, pos, ang):
    global gQkey, gZkey

    if gQkey==1:
        model.insert(0,4)
    elif gQkey==-1:
        if ang==0:
            model.insert(0,4)
        elif ang==-90:
            model.insert(0,3)
        elif ang==-180:
            model.insert(0,5)
        elif ang==-270:
            model.insert(0,2)
    if gQkey==1 or ang%(-90)==0:
        pos[0] += 1.3

def moveD(model, pos, ang):
    global gQkey, gZkey

    if gQkey==1:
        model.insert(0,5)
    elif gQkey==-1:
        if ang==0:
            model.insert(0,5)
        elif ang==-90:
            model.insert(0,2)
        elif ang==-180:
            model.insert(0,4)
        elif ang==-270:
            model.insert(0,3)
    if gQkey==1 or ang%(-90)==0:
        pos[0] -= 1.3
   
def drawObj_glDrawElements():
    global gVertexArrayIndexed, gIndexArray, gNormal
    
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    narr = gNormal
   
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_VERTEX_ARRAY)
    
    glNormalPointer(GL_FLOAT, 3*varr.itemsize, narr)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def createVertexAndIndexArrayIndexed(gPath): 
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
    for i in range(len(v_index)):
        for j in range(3):
            narr[v_index[i][j]] = n_coords[n_index[i][j]]
    
    varr = np.array(v_coords, 'float32')
    iarr = np.array(v_index)
    narr = np.array(narr)
    
    return varr, iarr, narr

def main():
    if not glfw.init():
        return

    window = glfw.create_window(640, 640, '2018008177', None, None)
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
