import sys

import pygame

from view import View

sys.path.insert(0, '../input')
from basic_button import BasicButton
from text_box import TextBox
from inputManager import InputManager


class AttrSliderButton(BasicButton):
    def handle_click(self, event):
        self.value[0] = self.value[0] + self.increase

    def __init__(self, color, rect, value: [int], increase):
        super().__init__(color, rect)
        self.value = value
        self.increase = increase


class SingleAttrSlider(View):
    def __init__(self, title: str, value: [int], increase: int, coord: (int, int)):
        self.text = title
        self.value = value
        self.coord = coord
        self.components = []

        # define variables
        x, y = self.coord
        comp_width = 50
        grey = (189, 189, 189)
        black = (0, 0, 0)

        # add title text
        title_text_box_pos = (x,y + (comp_width * 0.5))
        title_text_box = TextBox(title, black, title_text_box_pos)
        title_text_box.set_font('../assets/fonts/ARCADE_R.TTF', 15)
        self.add_component(title_text_box)

        x += 200

        # add decrease button
        decrease_rect = pygame.Rect(x, y, comp_width, comp_width)
        self.decrease_button = AttrSliderButton(grey, decrease_rect, self.value, (-1 * increase))
        self.add_component(self.decrease_button)

        # add value text
        text_box_pos = (x + (comp_width * 2), y + (comp_width * 0.5))
        self.value_text_box = TextBox(str(self.value[0]), black, text_box_pos, center=True)
        self.value_text_box.set_font('../assets/fonts/ARCADE_R.TTF', 15)
        self.components.append(self.value_text_box)

        increase_rect = pygame.Rect((x + (comp_width * 3), y, comp_width, comp_width))
        self.increase_button = AttrSliderButton(grey, increase_rect, self.value, increase)
        self.add_component(self.increase_button)

    def add_listeners(self, input_manager: InputManager):
        input_manager.instance.add_mouse_click_listener(self.decrease_button)
        input_manager.instance.add_mouse_click_listener(self.increase_button)

    def remove_listeners(self, input_manager: InputManager):
        input_manager.instance.remove_listener(self.decrease_button)
        input_manager.instance.remove_listener(self.increase_button)

    def draw(self, screen):
        for comp in self.components:
            comp.draw(screen)

        number_font = pygame.font.Font('../assets/fonts/ARCADE_R.TTF', 30)
        black = (0, 0, 0)

    def update(self):
        # update text
        self.value_text_box.text = str(self.value[0])

        for comp in self.components:
            comp.update()

    def add_component(self, comp):
        self.components.append(comp)

    def remove_component(self, comp):
        self.components.remove(comp)

    def before_exit(self):
        pass
