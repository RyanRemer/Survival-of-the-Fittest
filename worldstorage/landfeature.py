#Made by Brian Robinson

from pygame import gfxdraw as gfx

class LandFeature:
        def __init__(self, position, can_walk=True, can_swim=True,
                     can_climb=True, walk_speed_mod=1,
                     swim_speed_mod=1, climb_speed_mod=1,
                     damage=0):
                self.position = position
                self.can_walk = can_walk
                self.can_swim = can_swim
                self.can_climb = can_climb
                self.walk_speed_mod = walk_speed_mod
                self.swim_speed_mod = swim_speed_mod
                self.climb_speed_mod = climb_speed_mod
                self.damage = damage
        def draw(self, screen):
                pass
        def update(self):
                pass
        
