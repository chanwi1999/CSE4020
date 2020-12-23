import glfw
from OpenGL.GL import *
import numpy as np
import math

def render(key):

		x = np.linspace(0,1,12)
		y = np.linspace(0,1,12)
		
		for i in range(0,12,1):
			x[i] = np.cos(30*i*math.pi*(1/180))
			y[i] = np.sin(30*i*math.pi*(1/180))

		glClear(GL_COLOR_BUFFER_BIT)
		glLoadIdentity()
		glBegin(key)
		
		for i in range(0,12):
			glVertex2f(x[i],y[i])
		
		glEnd()

def key_callback(window, key, scancode, action, mods):

		if key==glfw.KEY_1:
			if action==glfw.PRESS:
				render(GL_POINTS)
		elif key==glfw.KEY_2:
			if action==glfw.PRESS:
				render(GL_LINES)
		elif key==glfw.KEY_3:
			if action==glfw.PRESS:
				render(GL_LINE_STRIP)
		elif key==glfw.KEY_4:
			if action==glfw.PRESS:
				render(GL_LINE_LOOP)
		elif key==glfw.KEY_5:
			if action==glfw.PRESS:
				render(GL_TRIANGLES)
		elif key==glfw.KEY_6:
			if action==glfw.PRESS:
				render(GL_TRIANGLE_STRIP)
		elif key==glfw.KEY_7:
			if action==glfw.PRESS:
				render(GL_TRIANGLE_FAN)
		elif key==glfw.KEY_8:
			if action==glfw.PRESS:
				render(GL_QUADS)
		elif key==glfw.KEY_9:
			if action==glfw.PRESS:
				render(GL_QUAD_STRIP)
		elif key==glfw.KEY_0:
			if action==glfw.PRESS:
				render(GL_POLYGON)

def main():
		
		if not glfw.init():
				return

		window = glfw.create_window(480,480, "2018008177", None, None)

		if not window:
				glfw.terminate()
				return

		glfw.set_key_callback(window, key_callback)
		glfw.make_context_current(window)

		render(GL_LINE_LOOP)

		while not glfw.window_should_close(window):
			glfw.poll_events()

			glfw.swap_buffers(window)

		glfw.terminate()

if __name__ == "__main__":
		main()

