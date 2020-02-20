#Made by Brian Robinson

import pygame
import random
import numpy as np
from worldchunk import WorldChunk
from updatepacket import UpdatePacket
from gameworld import GameWorld
import sys
sys.path.insert(0, '../creature')
from ctr import Creature
from spectemp import SpeciesTemplate
from resource import Resource
from landfeature import LandFeature
from foodtype import FoodType
sys.path.insert(0, '../worldgeneration')
from worldtypes import WorldTypes

def test_all(seed, num_trials):
        if seed != None:
                random.seed(seed)
        game_world = GameWorld(None, WorldTypes.PLAINS, np.array([200,200]), 0)
        test_add_creature(game_world, num_trials)
        game_world.print_creatures()
        test_move_creature(game_world, num_trials)
        game_world.print_creatures()
        test_remove_creature(game_world, num_trials)
        game_world.print_creatures()
        test_add_resource(game_world, num_trials)
        game_world.print_resources()
        test_move_resource(game_world, num_trials)
        game_world.print_resources()
        test_remove_resource(game_world, num_trials)
        game_world.print_resources()
        test_add_land_feature(game_world, num_trials)
        game_world.print_land_features()
        test_remove_land_feature(game_world, num_trials)
        game_world.print_land_features()
        game_world.update()

view_range = 200
def test_get_creature(game_world):
        global view_range
        point = np.array([random.randrange(game_world._world_dimensions[0]), random.randrange(game_world._world_dimensions[1])])
        test_creature = Creature(SpeciesTemplate(id="1"))
        test_creature.position = point
        world_creatures = game_world.get_update_info(test_creature,view_range).same_creatures
        correct_creatures = [c for c in game_world._creatures if np.linalg.norm(point-c.position)< view_range]
        return (len(world_creatures),len(correct_creatures))

num_creatures = 10
def test_add_creature(game_world, num_trials):
        global num_creatures
        creatures = [Creature(SpeciesTemplate(id="1")) for i in range(num_creatures)]
        for c in creatures:
                c.position = np.array([random.randrange(game_world._world_dimensions[0]), random.randrange(game_world._world_dimensions[1])])
                game_world.add_creature(c)
        if len(creatures) != len(game_world._creatures):
                print("Add Creature Initial Test Failed!")
                print("Expected " + str(len(creatures)) + " creatures, got " + str(len(game_world._creatures)))
                return
        for i in range(num_trials):
                actual,expected = test_get_creature(game_world)
                if actual != expected:
                        print("Add Creature Get Test " + str(i) + " Failed!")
                        print("Expected " + str(expected) + " creatures, got " + str(actual))
                        return
        print("Add Creature Tests Passed!")

def test_move_creature(game_world, num_trials):
        for i in range(num_trials):
                for c in game_world._creatures:
                        game_world.move_creature(c, c.position,
                                c.position + np.array([random.randrange(49)-24,random.randrange(49)-24]))
                actual, expected = test_get_creature(game_world)
                if actual != expected:
                        print("Move Creature Get Test " + str(i) + " Failed!")
                        print("Expected " + str(expected) + " creatures, got " + str(actual))
                        return
        print("Move Creature Tests Passed!")

def test_remove_creature(game_world, num_trials):
        creatures = game_world._creatures[:len(game_world._creatures)//2]
        remove = game_world._creatures[len(creatures):]
        for c in remove:
                game_world.remove_creature(c)
        if len(creatures) != len(game_world._creatures):
                print("Remove Creature Initial Test Failed!")
                print("Expected " + str(len(creatures)) + " creatures, got " + str(len(game_world._creatures)))
                return
        for i in range(num_trials):
                actual, expected = test_get_creature(game_world)
                if actual != expected:
                        print("Remove Creature Get Test " + str(i) + " Failed!")
                        print("Expected " + str(expected) + " creatures, got " + str(actual))
                        return
        print("Remove Creature Tests Passed!")


def test_get_resource(game_world):
        global view_range
        point = np.array([random.randrange(game_world._world_dimensions[0]), random.randrange(game_world._world_dimensions[1])])
        test_creature = Creature(SpeciesTemplate(id="1"))
        test_creature.position = point
        world_resources = game_world.get_update_info(test_creature,view_range).resources
        correct_resources = [c for c in game_world._resources if np.linalg.norm(point-c.position)< view_range]
        return (len(world_resources),len(correct_resources))

num_resources = 2
def test_add_resource(game_world, num_trials):
        global num_resources
        resources = [Resource(0, np.array([random.randrange(game_world._world_dimensions[0]), random.randrange(game_world._world_dimensions[1])]), FoodType.MEAT) for i in range(num_resources)]
        initial = len(game_world._resources)
        for c in resources:
                game_world.add_resource(c)
        if len(resources) + initial != len(game_world._resources):
                print("Add resource Initial Test Failed!")
                print("Expected " + str(len(resources)) + " resources, got " + str(len(game_world._resources)))
                return
        for i in range(num_trials):
                actual,expected = test_get_resource(game_world)
                if actual != expected:
                        print("Add resource Get Test " + str(i) + " Failed!")
                        print("Expected " + str(expected) + " resources, got " + str(actual))
                        return
        print("Add resource Tests Passed!")

def test_move_resource(game_world, num_trials):
        for i in range(num_trials):
                for c in game_world._resources:
                        game_world.move_resource(c, c.position,
                                c.position + np.array([random.randrange(49)-24,random.randrange(49)-24]))
                actual, expected = test_get_resource(game_world)
                if actual != expected:
                        print("Move resource Get Test " + str(i) + " Failed!")
                        print("Expected " + str(expected) + " resources, got " + str(actual))
                        return
        print("Move resource Tests Passed!")

def test_remove_resource(game_world, num_trials):
        resources = game_world._resources[:len(game_world._resources)//2]
        remove = game_world._resources[len(resources):]
        for c in remove:
                game_world.remove_resource(c)
        if len(resources) != len(game_world._resources):
                print("Remove resource Initial Test Failed!")
                print("Expected " + str(len(resources)) + " resources, got " + str(len(game_world._resources)))
                return
        for i in range(num_trials):
                actual, expected = test_get_resource(game_world)
                if actual != expected:
                        print("Remove resource Get Test " + str(i) + " Failed!")
                        print("Expected " + str(expected) + " resources, got " + str(actual))
                        return
        print("Remove resource Tests Passed!")

def test_get_land_feature(game_world):
        global view_range
        point = np.array([random.randrange(game_world._world_dimensions[0]), random.randrange(game_world._world_dimensions[1])])
        test_creature = Creature(SpeciesTemplate(id="1"))
        test_creature.position = point
        world_land_features = game_world.get_update_info(test_creature,view_range).land_features
        correct_land_features = [c for c in game_world._land_features if np.linalg.norm(point-c.position)< view_range]
        return (len(world_land_features),len(correct_land_features))

num_land_features = 200
def test_add_land_feature(game_world, num_trials):
        global num_land_features
        land_features = [LandFeature(np.array([random.randrange(game_world._world_dimensions[0]), random.randrange(game_world._world_dimensions[1])])) for i in range(num_land_features)]
        initial = len(game_world._land_features)
        for c in land_features:
                game_world.add_land_feature(c)
        if len(land_features) + initial != len(game_world._land_features):
                print("Add Land Feature Initial Test Failed!")
                print("Expected " + str(len(land_features)) + " land_features, got " + str(len(game_world._land_features)))
                return
        for i in range(num_trials):
                actual,expected = test_get_land_feature(game_world)
                if actual != expected:
                        print("Add Land Feature Get Test " + str(i) + " Failed!")
                        print("Expected " + str(expected) + " land_features, got " + str(actual))
                        return
        print("Add Land Feature Tests Passed!")

def test_remove_land_feature(game_world, num_trials):
        land_features = game_world._land_features[:len(game_world._land_features)//2]
        remove = game_world._land_features[len(land_features):]
        for c in remove:
                game_world.remove_land_feature(c)
        if len(land_features) != len(game_world._land_features):
                print("Remove Land Feature Initial Test Failed!")
                print("Expected " + str(len(land_features)) + " land_features, got " + str(len(game_world._land_features)))
                return
        for i in range(num_trials):
                actual, expected = test_get_land_feature(game_world)
                if actual != expected:
                        print("Remove Land Feature Get Test " + str(i) + " Failed!")
                        print("Expected " + str(expected) + " land_features, got " + str(actual))
                        return
        print("Remove Land Feature Tests Passed!")

test_all(None, 20)
