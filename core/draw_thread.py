import sys

import pygame

sys.path.insert(0, '../input')
from inputManager import InputManager
from listener_interface import _QuitListener
from thread_block import ThreadBlock


def close_app(app):
    app.is_done = True


class QuitListener(_QuitListener):
    def __init__(self, main_app):
        self.main_app = main_app

    def quit(self, event):
        close_app(self.main_app)


class DrawThread:
    def __init__(self, app):
        self.app = app
        screen_size = [1024, 512]
        self.screen = pygame.display.set_mode(screen_size)
        self.input_manager = InputManager().instance
        self.input_manager.add_quit_listener(QuitListener(self.app))

    def run(self):
        clock = pygame.time.Clock()

        while not self.app.is_done:
            clock.tick(self.app.framerate)
            if self.app.is_not_blocked:
                self.app.set_blocked(ThreadBlock.Draw, True)

                self.app.view.draw(self.screen)
                pygame.display.flip()

                self.input_manager.handle_events(pygame.event.get())
                self.app.set_blocked(ThreadBlock.Draw, False)
