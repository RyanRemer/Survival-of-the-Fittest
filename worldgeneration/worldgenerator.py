
#Made by Brian Robinson
import numpy as np
import sys, math, random
sys.path.insert(0, '../worldstorage')
from worldchunk import WorldChunk
from resource import Resource
sys.path.insert(0, '../creature')
from foodtype import FoodType

class WorldGenerator:
        def create_world(self, chunk_dimensions, world_dimensions, seed):
                self._chunk_dimensions = chunk_dimensions
                self._world_dimensions = world_dimensions
                chunks = np.divide(world_dimensions, chunk_dimensions)
                world = [[WorldChunk() for y in range(math.ceil(chunks[1]))] for x in range(math.ceil(chunks[0]))]
                random.seed(seed)
                return world
        def _get_chunk(self, pos):
                chunk = np.divide(pos, self._chunk_dimensions)
                return (math.floor(chunk[0]), math.floor(chunk[1]))
        def _spawn_resource(self, world, resource, seed):
                position = np.array([random.randrange(self._world_dimensions[0]), random.randrange(self._world_dimensions[1])])
                chunk = self._get_chunk(position)
                resource.position = position
                world[chunk[0]][chunk[1]].add_resource(resource)
        def _spawn_water_cluster(self, world, min_size, max_size, min_amount, max_amount):
                min_radius = int(min_size//15)
                max_radius = int(max_size//15)
                cluster_center = np.array([
                        random.randrange(max_radius, stop=self._world_dimensions[0]-max_radius),
                        random.randrange(max_radius, stop=self._world_dimensions[1]-max_radius)
                        ])
                for i in range(random.randint(min_amount, max_amount)):
                        off_range = max_radius - min_radius
                        offset = np.array([random.randint(-off_range, off_range)])
                        position = cluster_center + offset
                        value = random.randint(min_size, max_size)
                        resource = Resource(value, position, FoodType.WATER)
                        chunk = self._get_chunk(position)
                        world[chunk[0]][chunk[1]].add_resource(resource)
        def _spawn_land_feature(self, world, land_feature, seed):
                position = np.array([random.randrange(self._world_dimensions[0]), random.randrange(self._world_dimensions[1])])
                chunk = self._get_chunk(position)
                land_feature.position = position
                world[chunk[0]][chunk[1]].add_land_feature(land_feature)
