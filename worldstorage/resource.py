#Made by Brian Robinson
import sys
sys.path.insert(0, "..")
from creature.foodtype import FoodType
import core.color as color
from pygame import gfxdraw as gfx
import pygame

class Resource():
	def __init__(self, value, position, food_type):
		if value==0:
			value=200
		self.value = value
		self.max_value=value
		self.position = position
		self.food_type = food_type
		self.worldchunk=None
		self.radius_mod=15
		self.water_regen_rate=1
		self.plant_regen_rate=5
		self.regen_rate=3
		self.regen_counter=0

	def draw(self, screen):
		radius=int(self.value//self.radius_mod)
		if radius<1:
			radius=1
		x, y = int(self.position[0]), int(self.position[1])
		if(self.food_type == FoodType.WATER):
			gfx.filled_circle(screen, x, y, int(radius), color.light_blue)
		elif(self.food_type == FoodType.MEAT):
			gfx.filled_ellipse(screen, x, y, radius, int(radius*2/3), color.red)
		elif(self.food_type == FoodType.PLANTS):
			half_r = int(radius/2)
			gfx.filled_circle(screen, x, y+half_r, half_r, color.light_green)
			gfx.filled_circle(screen, x, y-half_r, half_r, color.light_green)
			gfx.filled_circle(screen, x+half_r, y, half_r, color.light_green)
			gfx.filled_circle(screen, x-half_r, y, half_r, color.light_green)

	def draw_top(self, screen):
		radius=int(self.value//self.radius_mod)
		if radius<1:
			radius=1
		x, y = int(self.position[0]), int(self.position[1])
		if(self.food_type == FoodType.WATER):
			gfx.filled_circle(screen, x, y, int(radius*2/3), color.blue)
		elif(self.food_type == FoodType.PLANTS):
			half_r = int(radius/2)
			gfx.filled_circle(screen, x, y, half_r, color.green)

	def consume(self, amount):
		self.value=self.value-amount        

	def register(self,worldchunk):
		self.worldchunk=worldchunk

	def remove(self):
		if self.worldchunk!=None:
			self.worldchunk.remove_resource(self)

	def update(self):
		if self.value<1 :
			self.remove()
		if self.regen_counter>self.regen_rate:
			self.regen_counter=0
			if self.food_type==FoodType.MEAT:
				self.consume(1)
			elif self.food_type==FoodType.WATER:
				if self.value<self.max_value:
					self.value+=self.water_regen_rate
			elif self.food_type==FoodType.PLANTS:
				if self.value<self.max_value:
					self.value+=self.plant_regen_rate
		else:
			self.regen_counter+=1


	def get_radius(self):
		return 1+self.value//self.radius_mod
		

class FoodColor():
	# List different lists of vertecies for shapes.
	# Keep values between -1 and 1, so they can later be scaled up.
	
	@staticmethod
	def get(kind):
		if kind==FoodType.WATER:
			return color.light_blue
		elif kind==FoodType.MEAT:
			return color.red
		elif kind==FoodType.PLANTS:
			return color.light_green
		else:
			return "invalid food type"
