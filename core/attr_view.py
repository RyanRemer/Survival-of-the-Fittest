import math
import sys

import pygame

from attr_adapter import AttrAdapter
from game_view import GameView
from single_attr_slider import SingleAttrSlider
from view import View

sys.path.insert(0, '../input')
from inputManager import InputManager
from text_box import TextBox
from basic_button import BasicButton

sys.path.insert(0, '../creature')
from body import Body, BodyType
from spectemp import SpeciesTemplate
from foodtype import FoodType

# constants
scale_avg = 50
scale_min = 0
scale_max = 100


# this button sends the user to the game
class GoToGameButton(BasicButton):
    def __init__(self, app, color, rect, attr_view):
        super().__init__(color, rect)
        self.app = app
        self.attr_view = attr_view

    def handle_click(self, event):
        ctr_attr = self.attr_view.ctr_attr
        body_type = self.attr_view.body.type
        food_type = self.attr_view.food_button.food_type
        win_condition = self.attr_view.win_condition_button.win_condition
        print("wincondition is ",win_condition)

        template = SpeciesTemplate(base_attributes=ctr_attr, body_type=body_type, food_type=food_type,
                                   abilities=[])

        game_view = GameView(
            self.app, 
            template,
            win_condition,
            
        )

        self.app.set_view(game_view)


# this button toggles the body type
class BodyTypeButton(BasicButton):
    def __init__(self, body_type: BodyType, color, rect):
        super().__init__(color, rect)
        self.body_type = body_type

    def handle_click(self, event):
        self.body_type += 1
        self.body_type = self.body_type % 6

class WinConditionButton(BasicButton):
    def __init__(self, win_condition,color,rect):
        super().__init__(color,rect)
        self.win_condition=win_condition
    
    def handle_click(self,event):
        self.win_condition+=1
        self.win_condition=self.win_condition % 3



# this button toggles the creatures food type
class FoodTypeButton(BasicButton):
    def __init__(self, food_type: FoodType, color, rect):
        super().__init__(color, rect)
        self.food_type = food_type

    def draw(self, screen):
        super().draw(screen)

        if self.food_type == FoodType.MEAT:
            self.color = (221, 44, 0)
        else:
            self.color = (0, 200, 83)

    def handle_click(self, event):
        if self.food_type == FoodType.MEAT:
            self.food_type = FoodType.PLANTS
        else:
            self.food_type = FoodType.MEAT


class ScaleData:
    def __init__(self, title, value, change_value):
        self.title = title
        self.value = value
        self.change_value = change_value


class AttrView(View):
    def __init__(self, app):
        self.components = []
        self.app = app

        # set up the values that the user will control
        increase_amount = 5
        init_values = 45
        self.scale_data = [
            ScaleData("Size", [init_values], increase_amount),
            ScaleData("Hardiness", [init_values], increase_amount),
            ScaleData("Speed", [init_values], increase_amount),
            ScaleData("Aggression", [init_values], increase_amount),
            ScaleData("Awareness", [init_values], increase_amount),
            ScaleData("Lifespan", [init_values], increase_amount),
        ]

        self.attr_sliders = {}

        # add title text
        title_text_box = TextBox("Create Your Creature", (0, 0, 0), (50, 50))
        title_text_box.set_font('../assets/fonts/ARCADE_R.TTF', 30)
        self.components.append(title_text_box)

        # build the user input form
        form_x = 50
        form_y = 100
        for data in self.scale_data:
            attr_slider = SingleAttrSlider(data.title, data.value, data.change_value, (form_x, form_y))
            self.attr_sliders[data] = attr_slider
            form_y += 55
            self.add_component(attr_slider)
            attr_slider.add_listeners(InputManager())

        grey = (189, 189, 189)
        button_size = 50

        # make the go to game button
        game_button_rect = pygame.Rect(900, form_y, button_size, button_size)
        self.game_button = GoToGameButton(self.app, grey, game_button_rect, self)
        InputManager().instance.add_mouse_click_listener(self.game_button)
        self.add_component(self.game_button)

        # set up the body
        self.update_ctr_attr()
        self.body = Body(BodyType.TRIANGLE)

        # make the body toggle button
        body_button_rect = pygame.Rect(900, 100, button_size, button_size)
        self.body_button = BodyTypeButton(self.body.type, grey, body_button_rect)
        InputManager().instance.add_mouse_click_listener(self.body_button)
        self.add_component(self.body_button)

        #make the win condition button

        win_condition_button_rect = pygame.Rect(790,100,button_size,button_size)
        self.win_condition_button=WinConditionButton(0,grey,win_condition_button_rect)
        InputManager().instance.add_mouse_click_listener(self.win_condition_button)
        self.add_component(self.win_condition_button)

        # make the food toggle button
        food_button_rect = pygame.Rect(845, 100, button_size, button_size)
        self.food_button = FoodTypeButton(FoodType.MEAT, grey, food_button_rect)
        InputManager().instance.add_mouse_click_listener(self.food_button)
        self.add_component(self.food_button)

        self.angle = 0

    def draw(self, screen):
        white = (255, 255, 255)
        screen.fill(white)

        # draw the rotating creature
        self.body = Body(self.body_button.body_type)
        self.angle += 1
        self.angle %= 360
        rad_angle = self.angle * math.pi / 180
        heading = [math.cos(rad_angle), math.sin(rad_angle)]
        self.body.draw(screen, self.ctr_attr.size, (screen.get_width() * (3 / 4), screen.get_height() / 2), heading, False)

        for component in self.components:
            component.draw(screen)

    def update(self):
        total_score = 0
        highest_scale_data = self.scale_data[0]

        # make sure that scale values are within the ranges
        for data in self.scale_data:
            if data.value[0] > highest_scale_data.value[0]:
                highest_scale_data = data

            if data.value[0] < scale_min:
                data.value[0] = scale_min
            elif data.value[0] > scale_max:
                data.value[0] = scale_max
            total_score += data.value[0]

        max_score = len(self.scale_data) * scale_avg

        if total_score > max_score:
            amount_over = total_score - max_score
            highest_scale_data.value[0] -= amount_over

        for component in self.components:
            component.update()

        self.update_ctr_attr()

    def update_ctr_attr(self):
        attr_adapter = AttrAdapter(size=self.scale_data[0].value[0],
                                   hardiness=self.scale_data[1].value[0],
                                   speed=self.scale_data[2].value[0],
                                   aggression=self.scale_data[3].value[0],
                                   awareness=self.scale_data[4].value[0],
                                   lifespan=self.scale_data[5].value[0])
                                   
        self.ctr_attr = attr_adapter.get_ctr_attr()

    def add_component(self, comp):
        self.components.append(comp)

    def remove_component(self, comp):
        self.components.append(comp)

    def before_exit(self):
        InputManager().instance.remove_listener(self.game_button)
        InputManager().instance.remove_listener(self.body_button)
        InputManager().instance.remove_listener(self.food_button)

        for trait in self.scale_data:
            trait_form = self.attr_sliders[trait]
            trait_form.remove_listeners(InputManager())
