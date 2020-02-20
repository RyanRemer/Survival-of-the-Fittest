import numpy as np
import sys
sys.path.insert(0, '../worldstorage')
sys.path.insert(0, '../worldgeneration')
sys.path.insert(0, '../input')
sys.path.insert(0, '../creature')
import pygame
import pygame.gfxdraw as gfx
from gameworld import GameWorld
from gametype import GameType
from worldtypes import WorldTypes
from listener_interface import _MouseClickListener
from inputManager import InputManager
from game_won_view import GameWonView
from game_lost_view import GameLostView
from view import View


MENU_PANEL_WIDTH = 90
CREATURE_TYPES = ["creature1", "creature2", "creature3", "creature4"]



# You can set this View to the Default View in main_app.py for testing the game
class GameView(View):
    def __init__(self, app, player_ctr, win_condition):
        # setup game type
        game_type = GameType(
            world_type=WorldTypes.PLAINS, 
            ctr_types=CREATURE_TYPES[0],
            win_condition=win_condition
        )
        self.game_type = game_type

        self.app = app
        self.game_world = GameWorld(player_ctr, game_type, np.array([1024, 512]), None)

    def init(self):
        pass

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.game_world.draw(screen)

    def update(self):
        self.game_world.update()
        game_over=self.game_world.check_game_over()
        if game_over=="won":
            view=GameWonView(self.app)
            self.app.set_view(view)
        elif game_over=="lost":
            view=GameLostView(self.app)
            self.app.set_view(view)

    def add_component(self, comp):
        pass

    def remove_component(self, comp):
        pass

    def before_exit(self):
        pass
