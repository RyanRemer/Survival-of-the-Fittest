import abc
from listener_interface import _MouseClickListener
from listener_interface import _MouseScrollListener

import pygame
 

class UIComponent(abc.ABC):
    @abc.abstractmethod
    def draw(self,screen):
        raise NotImplementedError
    @abc.abstractmethod
    def update(self):
        raise NotImplementedError

class Button(UIComponent,_MouseClickListener):
    @abc.abstractmethod
    def __init__(self,color,rect):
        self.color=color
        self.rect=rect
    @abc.abstractmethod
    def draw(self,screen):
        raise NotImplementedError
        
    def update(self):
        raise NotImplementedError
    @abc.abstractmethod
    def mouse_clicked(self,event):
       raise NotImplementedError
    def handle(self,event):
        assert event.type==pygame.MOUSEBUTTONUP
        if self.rect.collidepoint(event.pos):
            self.mouse_clicked(event)


class ScrollMenu(UIComponent,_MouseScrollListener):
    @abc.abstractmethod
    def mouse_scrolled_up(self,event):
        raise NotImplementedError
    @abc.abstractmethod
    def mouse_scrolled_down(self,event):
        raise NotImplementedError
    def handle(self, event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==5:
                self.mouse_scrolled_down(event)
            if event.button==4:
                self.mouse_scrolled_up(event)
    @abc.abstractmethod
    def update(self):
        raise NotImplementedError
    @abc.abstractmethod
    def draw(self,screen):
        raise NotImplementedError




