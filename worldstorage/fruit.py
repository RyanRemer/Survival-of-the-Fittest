
#Made by Brian Robinson

from pygame import gfxdraw as gfx
import sys
sys.path.insert(0, '..')
from resource import Resource

class Fruit(Resource):
        def __init__(self, value, position):
                Resource.__init__(self, value, position)
        def draw(self, screen):
                pass
        def consume(self, amount):
                pass
