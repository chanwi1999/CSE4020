import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gCamHeight = 5.
gPress = 0
gFov = 300.

eye = [0., 0., 0.]
target = [0., 0., 0.]
upV = [0., 1., 0.]

gLastX = 240.
gLastY = 240.

def drawPlaneXZ():
    glBegin(GL_LINES)
    glColor3ub(100, 100, 100)
    arr = np.arange(-1000.,1000.,50.)
    for i in range(0, len(arr)):
        glVertex3fv(np.array([arr[i],0.,1000.]))
        glVertex3fv(np.array([arr[i],0.,-1000.]))
        glVertex3fv(np.array([1000.,0.,arr[i]]))
        glVertex3fv(np.array([-1000.,0.,arr[i]]))
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
        if gFov+.5 >= 800:
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

# ClassAssignment3 #

gPath = ''
gCnt = 0

gModel = None
gFlag = -1

class Joint:
	def __init__(self):
		self.channels = []
		self.offset = []
		self.parent = None
		self.children = []
		self.frames = []
		self.index = [0, 0]
		self.R = np.identity(4)
		self.T = np.identity(4)
		self.oldT = np.identity(4)
		self.TT = np.identity(4)
		self.local = np.identity(4)
		self.world = np.array([0, 0, 0, 0])

	def update(self, frame):
		for index, channel in enumerate(self.channels):
			tmp = self.frames[frame][index]
			R = np.identity(4)			
			
			if channel == 'Xposition':
				self.T[0, 3] = tmp
			elif channel == 'Yposition':
				self.T[1, 3] = tmp
			elif channel == 'Zposition':
				self.T[2, 3] = tmp
			elif channel == 'Xrotation':
				R[1, 1] = np.cos(np.radians(tmp))
				R[1, 2] = -np.sin(np.radians(tmp))
				R[2, 1] = np.sin(np.radians(tmp))
				R[2, 2] = np.cos(np.radians(tmp))
				self.R = np.dot(self.R, R)
			elif channel == 'Yrotation':
				R[0, 0] = np.cos(np.radians(tmp))
				R[0, 2] = np.sin(np.radians(tmp))
				R[2, 0] = -np.sin(np.radians(tmp))
				R[2, 2] = np.cos(np.radians(tmp))
				self.R = np.dot(self.R, R)
			elif channel == 'Zrotation':
				R[0, 0] = np.cos(np.radians(tmp))
				R[0, 1] = -np.sin(np.radians(tmp))
				R[1, 0] = np.sin(np.radians(tmp))
				R[1, 1] = np.cos(np.radians(tmp))
				self.R = np.dot(self.R, R)
		
		if self.parent:
			self.local = np.dot(self.parent.TT, self.oldT)
		else:
			self.local = np.dot(self.oldT, self.T)

		self.world = np.array([self.local[0, 3],
					self.local[1, 3],
					self.local[2, 3],
					self.local[3, 3]])
		self.TT = np.dot(self.local, self.R)		

		for child in self.children:
			child.update(frame)

class BVH:
	global gPath

	def __init__(self, gPath):
		self.__root = None
		self.__stack = []
		self.frametime = 0.
		self.frames = 0
		self.channel_count = 0
		self.motions = []
		self.jointName = []
		self.loader(gPath)

	@property
	def root(self):
		return self.__root

	def loader(self, gPath):
		f = open(gPath)
		lines = f.readlines()
		
		parent = None
		now = None
		motion = 0

		for line in lines[1:len(lines)]:
			values = line.split()
			if len(values) == 0:
				continue
			
			if values[0] in ["ROOT", "JOINT", "End"]:
				if now:
					parent = now
				now = Joint()
				self.jointName.append(values[1])

				if len(self.__stack) == 0:
					self.__root = now
				self.__stack.append(now)

				now.parent = parent
				if now.parent:
					now.parent.children.append(now)
			
			elif "OFFSET" in values[0]:
				offset = []
				for i in range(1, len(values)):
					offset.append(float(values[i]))
				now.offset = offset
				for i in range(0, 2):
					now.oldT[i, 3] = offset[i]
			
			elif "CHANNELS" in values[0]:
				now.channels = values[2:len(values)]
				now.index[0] = self.channel_count
				now.index[1] = self.channel_count + len(now.channels)
				self.channel_count += len(now.channels)

			elif "{" in values[0]:
				pass

			elif "}" in values[0]:
				now = now.parent
				if now:
					parent = now.parent

			elif "MOTION" in values[0]:
				motion = 1
			
			elif "Frames:" in values[0]:
				self.frames = int(values[1])
			
			elif "Frame" in values[0]:
				self.frametime = float(values[2])
		
			elif motion == 1:
				tmp = [float(val) for val in values]
				self.channel_data(self.__root, tmp)
				vals = []
				for val in values:
					vals.append(float(val))
				self.motions.append(vals)

	def channel_data(self, joint, data):
		joint.frames.append(data[:len(joint.channels)])
		data = data[len(joint.channels):]

		for child in joint.children:
			data = self.channel_data(child, data)
		return data

def drawModel(joint, cnt, draw):
	global gFlag, gModel
	
	pos = [0, 0, 0]
	R = np.identity(4)
	offset = np.array([float(joint.offset[0]),
			float(joint.offset[1]),
			float(joint.offset[2])])

	if gFlag == 1:
		for i in range(0, len(joint.channels)):
			channel = joint.channels[i]
			tmp = gModel.motions[cnt][joint.index[0] + i]
			R2 = np.identity(4)

			if channel.lower() == "xposition":
				pos[0] = tmp
			elif channel.lower() == "yposition":
				pos[1] = tmp
			elif channel.lower() == "zposition":
				pos[2] = tmp

			if channel.lower() == "xrotation":
				R2[1, 1] = np.cos(np.radians(tmp))
				R2[1, 2] = -np.sin(np.radians(tmp))
				R2[2, 1] = np.sin(np.radians(tmp))
				R2[2, 2] = np.cos(np.radians(tmp))
				R = np.dot(R, R2)
			elif channel.lower() == "yrotation":
				R2[0, 0] = np.cos(np.radians(tmp))
				R2[0, 2] = np.sin(np.radians(tmp))
				R2[2, 0] = -np.sin(np.radians(tmp))
				R2[2, 2] = np.cos(np.radians(tmp))
				R = np.dot(R, R2)
			elif channel.lower() == "zrotation":
				R2[0, 0] = np.cos(np.radians(tmp))
				R2[0, 1] = -np.sin(np.radians(tmp))
				R2[1, 0] = np.sin(np.radians(tmp))
				R2[1, 1] = np.cos(np.radians(tmp))
				R = np.dot(R, R2)

	glPushMatrix()
	glTranslatef(pos[0], pos[1], pos[2])

	if draw == 1:
		drawCube(joint.offset)

	glTranslatef(joint.offset[0], joint.offset[1], joint.offset[2])
	glMultMatrixf(R.T)

	for child in joint.children:
		drawModel(child, cnt, 1)
	glPopMatrix()

def drawCube(offset):
	glBegin(GL_QUADS)

	origin = np.array([0, 0, 0])
	offset = np.array(offset)
	upY = np.array([0., 1, 0.])
	p = [[[0]] * 4, [0] * 4]
	
	v1 = origin - offset
	v1 = v1 / (np.sqrt(np.dot(v1, v1)))

	v2 = np.cross(v1, upY)
	v2 = v2 / (np.sqrt(np.dot(v2, v2)))
	v2 *= 1.
	
	v3 = np.cross(v1, v2)
	v3 = v3 / (np.sqrt(np.dot(v3, v3)))
	v3 *= 1.

	p[0][0] = origin + v2
	p[1][0] = offset + v2
	
	p[0][1] = origin + v3
	p[1][1] = offset + v3
	
	p[0][2] = origin - v2
	p[1][2] = offset - v2
	
	p[0][3] = origin - v3
	p[1][3] = offset - v3

	for i in range(0, 2):
		glNormal3f(v1[0], v1[0], v1[0])
		for pos in p[i]:
			glVertex3f(pos[0], pos[1], pos[2])

	n1 = v2 + v3
	n1 = n1 / (np.sqrt(np.dot(n1, n1)))

	n2 = v2 - v3
	n2 = n2 / (np.sqrt(np.dot(n2, n2)))

	for i in range(0, 4):
		j = i + 1
		
		if i == 0:
			glNormal3f(n1[0], n1[1], n1[2])
		elif i == 1:
			glNormal3f(n2[0], n2[1], n2[2])
		elif i == 2:
			glNormal3f(-n1[0], -n1[1], -n1[2])
		else:
			glNormal3f(-n2[0], -n2[1], -n2[2])
			j = 0

		glVertex3f(p[0][i][0], p[0][i][1], p[0][i][2])
		glVertex3f(p[1][i][0], p[1][i][1], p[1][i][2])
		glVertex3f(p[1][j][0], p[1][j][1], p[1][j][2])
		glVertex3f(p[0][j][0], p[0][j][1], p[0][j][2])

	glEnd()

def drop_callback(window, paths):
    global gPath, gCnt, gFlag, gModel

    gPath = ''.join(paths)
    gCnt = 0
    gFlag = -1
    gModel = BVH(gPath)
    print_inform()

def print_inform():
    global gPath, gModel

    print("1. File name: " + gPath)
    print("2. Number of frames: " + str(gModel.frames))
    print("3. FPS (which is 1/FrameTime): " + str(1/gModel.frametime))
    print("4. Number of joints (including root): " + str(len(gModel.jointName)))
    print("5. List of all joint names:")
    for name in gModel.jointName:
        print(name + " ")

def key_callback(window, key, scancode, action, mods):
    global gCnt, gFlag
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_SPACE:
            if gFlag == 1:
                gCnt = 0
            gFlag *= -1

def render(gCnt):
    global eye, target, upV, gModel, gFlag

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1, 100000)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    eye = [ target[0] + (gFov*np.cos(np.radians(gCamHeight))*np.cos(np.radians(gCamAng))),
            target[1] + (gFov*np.sin(np.radians(gCamHeight))),
            target[2] + (gFov*np.cos(np.radians(gCamHeight))*np.sin(np.radians(gCamAng))) ]
    gluLookAt(eye[0],eye[1],eye[2], target[0],target[1],target[2], upV[0],upV[1],upV[2])

    # grid plane
    drawPlaneXZ()

    # lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
	
    glEnable(GL_NORMALIZE)
    glPushMatrix()
    
    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glPopMatrix()
    
    LightColor = (1., 1., 1., 1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, LightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    
    ObjectColor = (1., 0., 0., 1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, ObjectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 50)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    if gModel:
        glPushMatrix()
        
        if gCnt == gModel.frames:
            gCnt = 0
        drawModel(gModel.root, gCnt % gModel.frames, 0)
        
        glPopMatrix()

    glDisable(GL_LIGHTING)

def main():
    global gFlag, gCnt
    
    if not glfw.init():
        return

    window = glfw.create_window(1000, 1000, '2018008177', None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_drop_callback(window, drop_callback)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        render(gCnt)
        glfw.swap_buffers(window)
        if gFlag == 1:
            gCnt += 1
    glfw.terminate()

if __name__ == "__main__":
    main()
