import numpy as np
from enum import IntEnum
from math import atan2, pi, cos, sin, isnan
import pygame, sys, os
import pygame.gfxdraw as gfx
from pygame.locals import *

# Colors RGB
white = (255, 255, 255)
black = (0, 0, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)
purple= (200, 0, 200)
green = (0, 200, 0)

''' BodyType - Enumeration
	An enumeration for different types of bodies we have.
'''
class BodyType(IntEnum):
	TRIANGLE = 0
	SQUARE = 1
	RECTANGLE = 2
	DIAMOND = 3
	TRAPEZOID = 4
	PENTAGON = 5

''' BodyModel class
	A class that maps BodyTypes to a list of points used to draw the body.
	Points are listed in a counter-clockwise order.
'''
class BodyModel():
	# List different lists of vertecies for shapes.
	# Keep values between -1 and 1, so they can later be scaled up.
	body_list = {
		BodyType.TRIANGLE: [
			np.array([0,1]),
			np.array([-.5,-1]),
			np.array([.5,-1])
		],
		BodyType.SQUARE: [
			np.array([-1,1]),
			np.array([-1,-1]),
			np.array([1,-1]),
			np.array([1,1])
		],
		BodyType.RECTANGLE: [
			np.array([-.5,1]),
			np.array([-.5,-1]),
			np.array([.5,-1]),
			np.array([.5,1])
		],
		BodyType.DIAMOND: [
			np.array([0,1]),
			np.array([-.5,0]),
			np.array([0,-1]),
			np.array([.5,0])
		],
		BodyType.TRAPEZOID: [
			np.array([-0.5,1]),
			np.array([0.5,1]),
			np.array([1,-1]),
			np.array([-1,-1])
		],
		BodyType.PENTAGON: [
			np.array([0,1]),
			np.array([-1,0]),
			np.array([-2/3,-1]),
			np.array([2/3,-1]),
			np.array([1,0])
		]
	}

	''' Return the specific model based on the type of body. '''
	@staticmethod
	def get(type):
		return BodyModel.body_list.get(type, "Invalid body type")



''' Body class
	Handles the drawing of the body on the screen.
'''
class Body():
	''' Takes in a BodyType to determine what shape to draw. '''
	def __init__(self, *args, **kwargs):
		if len(args) == 1:
			self.type: BodyType = args[0]
			self.color: tuple = black
			self.border: tuple = black
		elif len(args) == 2:
			self.type: BodyType = args[0]
			self.color: tuple = args[1]
			border = []
			for channel in self.color:
				c = channel - 40
				if c < 0:
					c = 0
				border.append(c)
			self.border = tuple(border)
		else:
			self.type: BodyType = kwargs.get("type", "None")
			self.color: tuple = black
			self.border: tuple = black
		# 90 degree rotation matrix #
		self.rot_90 = np.array([[0,-1],[1,0]])

	''' 
	Draws the creature model scaled by size, at position, rotated to face the same direction as heading 
	'''
	def draw(self, screen, size, position, heading, fill):
		norm = np.linalg.norm(heading)
		if norm == 0 or isnan(norm):
			norm_heading = np.array([1,0])
		else:
			norm_heading = heading / norm			

		orth_heading = norm_heading.dot(self.rot_90)
		rot_matrix = np.array([orth_heading, norm_heading])

		transformed_model = []
		for v in BodyModel.get(self.type):
			p = v * size          # Scale #
			p = p.dot(rot_matrix) # Rotate #
			p += position         # Translate #
			transformed_model.append(tuple(p))

		if(fill):
			gfx.filled_polygon(screen, transformed_model, self.color)	
		gfx.aapolygon(screen, transformed_model, self.border)
		


''' 
Main function to test the drawing of the shape.
This test works off of the position of the mouse to test rotation of shape while staying in 1 position.
'''
if __name__ == "__main__":
	b = Body(BodyType.PENTAGON, blue) # Set shape to display
	pygame.init()
	screenDimensions = (400, 540)
	window = pygame.display.set_mode(screenDimensions)
	pygame.display.set_caption('Body Drawing Test')
	screen = pygame.display.get_surface()
	done = False
	
	size = 50 # Scale the shape
	position = np.array((250, 100)) # Position the shape
	heading = np.array((0, 0)) # Initial point to look at

	timing_draw = []
	import time
	timer = time.time()
	#Game loop
	while not done:
		if len(timing_draw) >= 999999:
			done = True
			print("One million frames timed, quitting...")
		#Handle events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					done = True
			elif event.type == MOUSEMOTION:
				if 0 < event.pos[0] < 400 and 0 < event.pos[1] < 400:
					mouse = np.array(event.pos)
					heading = mouse - position # The direction from position to the mouse


		screen.fill(white)
		timer = time.time()
		b.draw(screen, size, position, heading)
		timing_draw.append(time.time() - timer)
		pygame.display.flip()

	ave_draw = 0
	for t in timing_draw:
		ave_draw += t
		ave_draw /= len(timing_draw)
	print(f"Average draw time: {ave_draw}")
	pygame.quit()
	quit()
