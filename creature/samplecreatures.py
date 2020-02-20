import numpy as np
from ctr import Creature, CreatureAttributes, SpeciesTemplate
from body import BodyType, Body
from foodtype import FoodType

triangle_template = SpeciesTemplate(
	player_adjustments=CreatureAttributes(),
	recent_creatures=[],
	abilities=[],
	body_type=BodyType.TRIANGLE,
	food_type=FoodType.MEAT,
)

def make_triangle(position):
	attributes = CreatureAttributes(
		size=15,
		health_cap=100,
		regen_rate=5,
		armor=15,
		base_damage=50,
		hunger_cap=100,
		hunger_loss=1,
		thirst_cap=100,
		thirst_loss=1,
		lifespan=300,
		maturity_age=75,
		max_velocity=7.5,
		steering_force=5,
		agressiveness=0.8,
		sight_range=50
	)
	triangle = Creature(
		attributes=attributes,
		template=triangle_template,
		health=attributes.health_cap,
		hunger=attributes.hunger_cap,
		thirst=attributes.thirst_cap,
		position=position,
		body= Body(triangle_template.body_type)
	)

	triangle_template.recent_creatures.append(triangle)
	return triangle


diamond_template = SpeciesTemplate(
	player_adjustments=CreatureAttributes(),
	recent_creatures=[],
	abilities=[],
	body_type=BodyType.DIAMOND,
	food_type=FoodType.PLANTS,
)

def make_diamond(position):
	attributes = CreatureAttributes(
		size=7,
		health_cap=50,
		regen_rate=10,
		armor=5,
		base_damage=5,
		hunger_cap=100,
		hunger_loss=1,
		thirst_cap=100,
		thirst_loss=1,
		lifespan=180,
		maturity_age=40,
		max_velocity=7.5,
		steering_force=5,
		agressiveness=0.2,
		sight_range=50
	)
	diamond = Creature(
		attributes=attributes,
		template=diamond_template,
		health=attributes.health_cap,
		hunger=attributes.hunger_cap,
		thirst=attributes.thirst_cap,
		position=position,
		body= Body(diamond_template.body_type)
	)

	diamond_template.recent_creatures.append(diamond)
	return diamond

pentagon_template = SpeciesTemplate(
	player_adjustments=CreatureAttributes(),
	recent_creatures=[],
	abilities=[],
	body_type=BodyType.PENTAGON,
	food_type=FoodType.PLANTS,
)

def make_pentagon(position):
	attributes = CreatureAttributes(
		size=25,
		health_cap=200,
		regen_rate=10,
		armor=30,
		base_damage=50,
		hunger_cap=100,
		hunger_loss=1,
		thirst_cap=100,
		thirst_loss=1,
		lifespan=300,
		maturity_age=150,
		max_velocity=2.5,
		steering_force=2,
		agressiveness=0.5,
		sight_range=50
	)
	pentagon = Creature(
		attributes=attributes,
		template=pentagon_template,
		health=attributes.health_cap,
		hunger=attributes.hunger_cap,
		thirst=attributes.thirst_cap,
		position=position,
		body= Body(pentagon_template.body_type)
	)

	pentagon_template.recent_creatures.append(pentagon_template)
	return pentagon

rectangle_template = SpeciesTemplate(
	player_adjustments=CreatureAttributes(),
	recent_creatures=[],
	abilities=[],
	body_type=BodyType.RECTANGLE,
	food_type=FoodType.MEAT,
)

def make_rectangle(position):
	attributes = CreatureAttributes(
		size=20,
		health_cap=150,
		regen_rate=10,
		armor=20,
		base_damage=60,
		hunger_cap=100,
		hunger_loss=1,
		thirst_cap=100,
		thirst_loss=1,
		lifespan=300,
		maturity_age=150,
		max_velocity=2.5,
		steering_force=2,
		agressiveness=0.8,
		sight_range=50
	)
	rectangle = Creature(
		attributes=attributes,
		template=rectangle_template,
		health=attributes.health_cap,
		hunger=attributes.hunger_cap,
		thirst=attributes.thirst_cap,
		position=position,
		body= Body(rectangle_template.body_type)
	)

	rectangle_template.recent_creatures.append(rectangle)
	return rectangle

if __name__ == "__main__":
	triangle = make_triangle(np.array([0,0]))
	diamond = make_diamond(np.array([0,0]))
	pentagon = make_pentagon(np.array([0,0]))
	rectangle = make_rectangle(np.array([0,0]))

	print(f'TRIANGLE:\n{triangle}')
	print(f'DIAMOND:\n{diamond}')
	print(f'PENTAGON:\n{pentagon}')
	print(f'RECTANGLE:\n{rectangle}')