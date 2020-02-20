# made by Alan Ames
from listener_interface import *


class InputManager:
    class _InputManager:

        def __init__(self):
            self.event_list = []

            self.mouse_move_listeners = []
            self.mouse_click_listeners = []
            self.mouse_scroll_listeners = []
            self.mouse_drag_listeners = []
            self.key_down_listeners = []
            self.key_up_listeners = []
            self.quit_listeners = []

        def add_mouse_move_listener(self, listener):
            self.mouse_move_listeners.append(listener)

        def add_mouse_click_listener(self, listener):
            self.mouse_click_listeners.append(listener)

        def add_mouse_scroll_listener(self, listener):
            self.mouse_scroll_listeners.append(listener)

        def add_mouse_drag_listener(self, listener):
            self.mouse_drag_listeners.append(listener)

        def add_key_down_listener(self, listener):
            self.key_down_listeners.append(listener)

        def add_key_up_listener(self, listener):
            self.key_up_listeners.append(listener)

        def add_quit_listener(self, listener):
            self.quit_listeners.append(listener)

        def remove_listener(self, listener):
            temp_list = []
            for l in self.mouse_click_listeners:
                if l != listener:
                    temp_list.append(l)
            self.mouse_click_listeners = temp_list

            temp_list = []
            for l in self.mouse_move_listeners:
                if l != listener:
                    temp_list.append(l)
            self.mouse_move_listeners = temp_list

            temp_list = []
            for l in self.mouse_scroll_listeners:
                if l != listener:
                    temp_list.append(l)
            self.mouse_scroll_listeners = temp_list

            temp_list = []
            for l in self.mouse_drag_listeners:
                if l != listener:
                    temp_list.append(l)
            self.mouse_drag_listeners = temp_list

            temp_list = []
            for l in self.key_down_listeners:
                if l != listener:
                    temp_list.append(l)
            self.key_down_listeners = temp_list

            temp_list = []
            for l in self.key_up_listeners:
                if l != listener:
                    temp_list.append(l)
            self.key_up_listeners = temp_list

            temp_list = []
            for l in self.quit_listeners:
                if l != listener:
                    temp_list.append(l)
            self.quit_listeners = temp_list

        def handle_events(self, event_list):
            for event in event_list:
                switcher = {
                    pygame.KEYDOWN: self.key_down_listeners,
                    pygame.KEYUP: self.key_up_listeners,
                    pygame.MOUSEMOTION: self.mouse_move_listeners,
                    pygame.MOUSEBUTTONUP: self.mouse_click_listeners,
                    pygame.MOUSEBUTTONDOWN: self.mouse_scroll_listeners,
                    pygame.QUIT: self.quit_listeners
                }
                listeners = switcher.get(event.type, [])
                for listener in listeners:
                    listener.handle(event)

    instance: _InputManager = None

    def __init__(self):
        if InputManager.instance is None:
            InputManager.instance = InputManager._InputManager()
        self.__dict__['_InputGenerator_instance'] = InputManager.instance
