#Made by Brian Robinson

from plainsworldgenerator import PlainsWorldGenerator
from worldtypes import WorldTypes

class WorldGenFactory:
        def get_generator(self, game_type):
                if game_type.world_type == WorldTypes.PLAINS:
                        return PlainsWorldGenerator()