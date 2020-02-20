#Made by Brian Robinson

import math
import pygame
import numpy as np
import random
import time
from worldchunk import WorldChunk
from updatepacket import UpdatePacket
import sys
sys.path.insert(0, '../worldgeneration')
from worldgenfactory import WorldGenFactory
sys.path.insert(0, '../creature')
from spawn import SpawnManager

chunks = 20
world_dimensions = np.array([2000,2000])

class GameWorld:
        def __init__(self, player_creature, game_type, world_dimensions, seed):
                #TODO: spawn player creatures using SpawnManager

                WORLD_DIMENSIONS = world_dimensions
                self._world_dimensions = WORLD_DIMENSIONS
                self._chunk_dimensions = np.divide(WORLD_DIMENSIONS, chunks)
                gen = WorldGenFactory().get_generator(game_type)
                self.player_creature_count=0
                self.other_creature_count=0
                self._world = gen.create_world(self._chunk_dimensions, self._world_dimensions, seed)
                self._creatures = []
                self._resources = []
                self._land_features = []
                self._toAdd = []
                for row in self._world:
                        for item in row:
                                self._creatures.extend(item.get_creatures())
                                self._resources.extend(item.get_resources())
                                self._land_features.extend(item.get_land_features())
                for res in self._resources:
                        res.register(self)
                spawn = SpawnManager(self)
                spawn.initial_generation(player_creature)
                for creature in self._creatures:
                        creature.register(self)

                self.start_time=time.time()
                self.wincondition=game_type.win_condition

                for resource in self._resources:
                        resource.register(self) 
        def update(self):
                for c in self._creatures:
                        c.update(self.get_update_info(c, c.attributes.sight_range))
                for r in self._resources:
                        r.update()


        def draw(self, screen):
                background_color = (245, 245, 245)
                screen.fill(background_color)
                for l in self._land_features:
                        l.draw(screen)
                for r in self._resources:
                        r.draw(screen)
                for r in self._resources:
                        r.draw_top(screen)
                for c in self._creatures:
                        c.draw(screen)
        def move_creature(self, creature, old_pos, new_pos):
                new_pos = np.array([new_pos[0] % self._world_dimensions[0],
                                    new_pos[1] % self._world_dimensions[1]])
                old = self._get_chunk(old_pos)
                new = self._get_chunk(new_pos)
                if old != new:
                        self._world[old[0]][old[1]].remove_creature(creature)
                        self._world[new[0]][new[1]].add_creature(creature)
                creature.position = new_pos
        def add_creature(self, creature):
                #if creature is creatureplayer:
                if creature.template.id.id==0:
                        self.player_creature_count+=1
                else:
                        self.other_creature_count+=1
                creature.register(self)
                chunk = self._get_chunk(creature.position)
                self._world[chunk[0]][chunk[1]].add_creature(creature)
                self._creatures.append(creature)
        def remove_creature(self, creature):
                chunk = self._get_chunk(creature.position)
                self._world[chunk[0]][chunk[1]].remove_creature(creature)
                self._creatures.remove(creature)
                if creature.template.id.id==0:
                        self.player_creature_count-=1
                else:
                        self.other_creature_count-=1
        def move_resource(self, resource, old_pos, new_pos):
                new_pos = np.array([new_pos[0] % self._world_dimensions[0],
                                    new_pos[1] % self._world_dimensions[1]])
                old = self._get_chunk(old_pos)
                new = self._get_chunk(new_pos)
                if old != new:
                        self._world[old[0]][old[1]].remove_resource(resource)
                        self._world[new[0]][new[1]].add_resource(resource)
                resource.position = new_pos
        def add_resource(self, resource):
                resource.register(self)
                chunk = self._get_chunk(resource.position)
                self._world[chunk[0]][chunk[1]].add_resource(resource)
                self._resources.append(resource)
        def remove_resource(self, resource):
                chunk = self._get_chunk(resource.position)
                self._world[chunk[0]][chunk[1]].remove_resource(resource)
                self._resources.remove(resource)
        def add_land_feature(self, feature):
                chunk = self._get_chunk(feature.position)
                self._world[chunk[0]][chunk[1]].add_land_feature(feature)
                self._land_features.append(feature)
        def remove_land_feature(self, feature):
                chunk = self._get_chunk(feature.position)
                self._world[chunk[0]][chunk[1]].remove_land_feature(feature)
                self._land_features.remove(feature)
        def get_update_info(self, creature, view_range):
                point = creature.position
                rangex = math.ceil(view_range / self._chunk_dimensions[0])
                rangey = math.ceil(view_range / self._chunk_dimensions[1])
                chunk = self._get_chunk(point)
                same_creatures = []
                other_creatures = []
                resources = []
                land_features = []
                for x in range(chunk[0] - rangex, chunk[0] + rangex + 1):
                        for y in range(chunk[1] - rangey, chunk[1] + rangey + 1):
                                if x < 0 or x >= len(self._world):
                                        continue
                                if y < 0 or y >= len(self._world[0]):
                                        continue
                                c = self._world[x][y]
                                all_creatures = self._get_in_range(c.get_creatures(), point, view_range)
                                for cr in all_creatures:
                                        if cr.id == creature.id:
                                                continue
                                        elif cr.template == creature.template:
                                                same_creatures.append(cr)
                                        else:
                                                other_creatures.append(cr)
                                resources.extend(self._get_in_range(c.get_resources(), point, view_range))
                                land_features.extend(self._get_in_range(c.get_land_features(), point, view_range))
                return UpdatePacket(land_features, same_creatures, other_creatures, resources, self)
        def print_creatures(self):
                print(len(self._creatures))
                for x in range(len(self._world)):
                        for y in range(len(self._world[0])):
                                print(len(self._world[x][y].get_creatures()), end="")
                        print()
        def print_resources(self):
                print(len(self._resources))
                for x in range(len(self._world)):
                        for y in range(len(self._world[0])):
                                print(len(self._world[x][y].get_resources()), end="")
                        print()
        def print_land_features(self):
                print(len(self._land_features))
                for x in range(len(self._world)):
                        for y in range(len(self._world[0])):
                                print(len(self._world[x][y].get_land_features()), end="")
                        print()
        def get_random_pos(self):
                return np.array([random.randrange(int(self._world_dimensions[0])), random.randrange(int(self._world_dimensions[1]))])

        def _get_chunk(self, pos):
                chunk = np.divide(pos, self._chunk_dimensions)
                return (math.floor(chunk[0]), math.floor(chunk[1]))
        def _get_in_range(self, items, point, view_range):
                return [i for i in items if np.linalg.norm(i.position-point) < view_range]

        def check_game_over(self):
                timed_game_length=180
                win_civilization_size=10
                
                #0 timed survive
                if self.wincondition==0 and time.time()>self.start_time+timed_game_length:
                        return "won"
                #last species staning =1      
                elif self.wincondition==1 and self.other_creature_count<1:
                        return "won"
                #civilization=2
                elif self.wincondition==2 and self.player_creature_count>win_civilization_size:
                        return "won"
                elif self.player_creature_count<1:
                        return "lost"
                else:
                        return "playing"

                
                