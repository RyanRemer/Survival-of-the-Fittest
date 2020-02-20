import abc

import pygame.gfxdraw as gfx

from UIcomponent import Button


class BasicButton(Button):

    def __init__(self, color, rect):
        super().__init__(color, rect)

        darkness = 50
        self.dark_color = (color[0] - darkness, color[1] - darkness, color[2] - darkness)
        self.clicked = 0

    def draw(self, screen):
        if self.clicked > 0:
            gfx.box(screen, self.rect, self.dark_color)
        else:
            gfx.box(screen, self.rect, self.color)

    def update(self):
        if self.clicked > 0:
            self.clicked -= 1

    def mouse_clicked(self, event):
        self.clicked = 5
        self.handle_click(event)

    @abc.abstractmethod
    def handle_click(self, event):
        pass
