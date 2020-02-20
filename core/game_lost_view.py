
import sys
import pygame 
from color import *
#from attr_view import AttrView
from view import View
sys.path.insert(0, '../input')
from listener_interface import _MouseClickListener
from inputManager import InputManager

class MainMenuOnClickListener(_MouseClickListener):
    def __init__(self, app):
        self.app = app

    def mouse_clicked(self, event):
        trait_view = AttrView(self.app)
        self.app.set_view(trait_view)

class GameLostView(View):
    def __init__(self,app):
        self.app=app
        self.col=white
        self.input_manager = InputManager().instance
        self.on_click_listener = MainMenuOnClickListener(self.app)
        self.input_manager.add_mouse_click_listener(self.on_click_listener)


    def draw(self,screen):
        screen.fill(white)
        screen_width=screen.get_width()
        screen_height=screen.get_height()

        message='You lost'
        title_font = pygame.font.Font('../assets/fonts/ARCADE_R.TTF', 30)
        title_text = title_font.render(message, False, black)
        title_text_box = title_text.get_rect(center=(screen_width / 2, screen_height / 2))
        
        subtitle_font = pygame.font.SysFont('arial', 18)
        subtitle_text = subtitle_font.render('Click to Play Again', False, black)
        subtitle_text_box = subtitle_text.get_rect(center=(screen_width / 2, screen_height / 2 + 50))

        screen.blits(blit_sequence=((title_text, title_text_box), (subtitle_text, subtitle_text_box)))
    def update(self):
        pass
    def add_component(self,comp):
        pass
    
    def remove_component(self, comp):
        pass

    def before_exit(self):
        self.input_manager.remove_listener(self.on_click_listener)


