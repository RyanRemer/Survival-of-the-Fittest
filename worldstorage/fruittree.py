#Made by Brian Robinson

from pygame import gfxdraw as gfx
import sys
sys.path.insert(0, '..')
from landfeature import LandFeature

class FruitTree(LandFeature):
        def __init__(position, can_walk, can_swim,
                     can_climb, walk_speed_mod,
                     swim_speed_mod, climb_speed_mod,
                     damage):
                Resource.__init__(position, can_walk, can_swim,
                     can_climb, walk_speed_mod,
                     swim_speed_mod, climb_speed_mod,
                     damage)
        def draw(self):
                pass
        def update(self):
                pass
        
