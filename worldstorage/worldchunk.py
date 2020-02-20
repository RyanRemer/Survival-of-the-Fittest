#Made by Brian Robinson

import pygame
import numpy

class WorldChunk:
        def __init__(self):
                self._area_start = None
                self._area_end = None
                self._creatures = []
                self._resources = []
                self._land_features = []
        def add_creature(self, creature):
                self._creatures.append(creature)
        def remove_creature(self, creature):
                self._creatures.remove(creature)
        def get_creatures(self):
                return self._creatures
        def add_resource(self, resource):
                self._resources.append(resource)
        def remove_resource(self, resource):
                self._resources.remove(resource)
        def get_resources(self):
                return self._resources
        def add_land_feature(self, feature):
                self._land_features.append(feature)
        def remove_land_feature(self, feature):
                self._land_features.remove(feature)
        def get_land_features(self):
                return self._land_features
        
