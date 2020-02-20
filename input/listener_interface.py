import abc
import pygame
import pygame.display



class _MouseMoveListener(abc.ABC):
    @abc.abstractmethod
    def mouse_moved(self,event):
        raise NotImplementedError
    def check_event_type(self,event):
        if event.type==pygame.MOUSEMOTION:
            return True
        else:
            return False
    def handle(self,event):
        self.mouse_moved(event)

class _MouseClickListener(abc.ABC):
    @abc.abstractmethod
    def mouse_clicked(self,event):
        raise NotImplementedError
    def check_event_type(self,event):
        if event.type==pygame.MOUSEBUTTONUP:
            if(event.button!=4 and event.button!=5):
                return True
            else:
                return False
        else:
            return False
    def handle(self,event):
        self.mouse_clicked(event)
    
class _MouseScrollListener(abc.ABC):
    @abc.abstractmethod
    def mouse_scrolled_up(self,event):
        raise NotImplementedError
    @abc.abstractmethod
    def mouse_scrolled_down(self,event):
        raise NotImplementedError
    def check_event_type(self,event):
        if event.type==pygame.MOUBUTTONDOWN and (event.button==4 or event.button==5):
            return True
        else:
            return False
    def handle(self, event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==5:
                self.mouse_scrolled_down(event)
            if event.button==4:
                self.mouse_scrolled_up(event)

class _KeyDownListener(abc.ABC):
    @abc.abstractmethod
    def key_down(self,event):
        raise NotImplementedError
    def check_event_type(self,event):
        if event.type==pygame.KEYDOWN:
            return True
        else:
            return False
    def handle(self,event):
        self.key_down(event)

class _KeyUpListener(abc.ABC):
    @abc.abstractmethod
    def key_up(self,event):
        raise NotImplementedError
    def check_event_type(self,event):
        if event.type==pygame.KEYUP:
            return True
        else:
            return False
    def handle(self,event):
        self.key_up(event)

class _QuitListener(abc.ABC):
    @abc.abstractmethod
    def quit(self,event):
        raise NotImplementedError

    def check_event_type(self,event):
        if event.type==pygame.QUIT:
            return True
        else:
            return False
    def handle(self,event):
        self.quit(event)

        

    
    