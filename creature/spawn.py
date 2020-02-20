import random
import sys

from body import Body, BodyType
from ctr import Creature
from foodtype import FoodType
from spectemp import SpeciesTemplate
from color import random_color

sys.path.insert(0, '../core')
from attr_adapter import AttrAdapter

SPAWN_PLAYER = 4  # Num player creatures spawned
SPAWN_ENEMY = 4  # Num enemy creatures spawned per enemy species
SPAWN_SPECIES = 4  # Num enemy species
MUTATION_AMOUNT = 30 # Maximum amount that attributes randomly mutate

_picked_colors = []
def _get_random_color():
    color = random_color()
    while color == (0,0,0) or color in _picked_colors:
        color = random_color()
    _picked_colors.append(color)
    return color

def _jitter(array, min_value, max_value, jitter_amount):
    vals = [(random.uniform(0,1)-0.5)*jitter_amount for i in array]
    avg = sum(vals)/len(vals)
    vals = [array[i]+vals[i]-avg for i in range(len(array))]
    for i in range(len(vals)):
        if vals[i] < min_value:
            d = min_value - vals[i]
            vals[i] += d
            vals[vals.index(max(vals))] -= d
        elif vals[i] > max_value:
            d = max_value - vals[i]
            vals[i] -= d
            vals[vals.index(min(vals))] += d
    for i in range(len(vals)):
        if vals[i] > max_value:
            vals[i] = max_value
        elif vals[i] < min_value:
            vals[i] = min_value
    return vals

_attr_adapter = AttrAdapter()
def _get_attr(scale_values):
    _attr_adapter.scale_values = {
        "size":scale_values[0],
        "hardiness":scale_values[1],
        "speed":scale_values[2],
        "aggression":scale_values[3],
        "awareness":scale_values[4],
        "lifespan":scale_values[5]
    }
    return _attr_adapter.get_ctr_attr()

class RandomSpeciesGenerator:
    def create_species(self):
        rand_attributes = [50 for a in _attr_adapter.scale_values]
        rand_attributes = _jitter(rand_attributes, 0, 100, 50)
        attributes = _get_attr(rand_attributes)
        max_attr = rand_attributes.index(max(rand_attributes))
        body = [BodyType.SQUARE, BodyType.PENTAGON, BodyType.DIAMOND,
                BodyType.TRIANGLE, BodyType.TRAPEZOID, BodyType.RECTANGLE][max_attr]
        food = random.choice(list(FoodType))
        while food == FoodType.WATER:
            food = random.choice(list(FoodType))
        template = SpeciesTemplate(
            base_attributes=attributes,
            body_type=body,
            food_type=food
        )
        template.scale_values = rand_attributes
        return template

_species_colors = [(0, 0, 0)] + [_get_random_color() for i in range(SPAWN_SPECIES)]
class CreatureGenerator:
    def __init__(self):
        self.attr_adapter = AttrAdapter()
    def create_creature(self, species, position):
        scale_values = _jitter(species.base_attributes.scale_values, 0, 100, MUTATION_AMOUNT)
        new_attributes = _get_attr(scale_values)
        creature = Creature(attributes=new_attributes,
                            template=species,
                            position=position,
                            body=Body(species.body_type, _species_colors[species.id.id]))
        return creature

    def create_child_creature(self, mom, dad, species, position):
        scale_values = [(mom.attributes.scale_values[i] +
                        dad.attributes.scale_values[i])/2
                        for i in range(len(mom.attributes.scale_values))]
        scale_values = _jitter(scale_values, 0, 100, MUTATION_AMOUNT)
        new_attributes = _get_attr(scale_values)
        creature = Creature(attributes=new_attributes,
                            template=species,
                            position=position,
                            body=Body(species.body_type, _species_colors[species.id.id]))
        return creature

class SpawnManager:
    instance = None
    def __init__(self, world):
        self.world = world
        self.species = {}
        self.species_gen = RandomSpeciesGenerator()
        self.creature_gen = CreatureGenerator()
        SpawnManager.instance = self

    def initial_generation(self, player_template):
        for i in range(SPAWN_SPECIES):
            spec = self.new_random_species()
            self.species[spec.id.id] = spec
            for j in range(SPAWN_ENEMY):
                self.spawn_creature(spec, self.world.get_random_pos())
        if player_template == None:
            return
        for i in range(SPAWN_PLAYER):
            self.spawn_creature(player_template, self.world.get_random_pos())

    def new_random_species(self):
        return self.species_gen.create_species()

    def get_species(self, species_id):
        return self.species[species_id.id]

    def spawn_creature(self, species_template, position):
        self.world.add_creature(self.creature_gen.create_creature(species_template, position))

    def spawn_child_creature(self, mom, dad, position):
        self.world.add_creature(self.creature_gen.create_child_creature(mom, dad, mom.template, position))
