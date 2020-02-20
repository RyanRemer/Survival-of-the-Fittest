
#Made by Brian Robinson

import sys
import random as rand
from worldgenerator import WorldGenerator
sys.path.insert(0, '../worldstorage')
from resource import Resource
from landfeature import LandFeature
sys.path.insert(0, '../creature')
from foodtype import FoodType

class PlainsWorldGenerator(WorldGenerator):
        PLANT_GEN_AMOUNT = 18
        PLANT_SIZE_MIN = 100
        PLANT_SIZE_MAX = 500

        MEAT_GEN_AMOUNT = 8
        MEAT_SIZE_MIN = 20
        MEAT_SIZE_MAX = 150

        WATER_GEN_AMOUNT = 2
        WATER_CLUSTER_MIN = 3
        WATER_CLUSTER_MAX = 8
        WATER_SIZE_MIN = 200
        WATER_SIZE_MAX = 1000
        def create_world(self, chunk_dimensions, world_dimensions, seed):
                global gen_factor
                world = super().create_world(chunk_dimensions, world_dimensions, seed)
                for i in range(self.WATER_GEN_AMOUNT):
                        self._spawn_water_cluster(world, self.WATER_SIZE_MIN, self.WATER_SIZE_MAX, self.WATER_CLUSTER_MIN, self.WATER_CLUSTER_MAX)
                for i in range(self.MEAT_GEN_AMOUNT):
                        self._spawn_resource(world, Resource(rand.randint(self.MEAT_SIZE_MIN, self.MEAT_SIZE_MAX),0,FoodType.MEAT), seed)
                for i in range(self.PLANT_GEN_AMOUNT):
                        self._spawn_resource(world, Resource(rand.randint(self.PLANT_SIZE_MIN, self.PLANT_SIZE_MAX),0,FoodType.PLANTS), seed)
                
                return world
                        

                        
                                
