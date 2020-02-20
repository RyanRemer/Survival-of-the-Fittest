import pygame

from draw_thread import DrawThread
from main_menu_view import MainMenuView
from thread_block import ThreadBlock
from update_thread import UpdateThread
from game_lost_view import GameLostView
from attr_view import AttrView
from view import View


class MainApp:
    def __init__(self):

        self.view = MainMenuView(self)
        # the block variables indicate if a thread is currently running
        self.draw_block = False
        self.update_block = False
        self.set_view_block = False
        self.framerate = 30
        self.updaterate = 30
        self.is_done = False
        

    def init_pygame(self):
        print("initializing Pygame...")
        pygame.init()
        pygame.font.init()

    def init_update_thread(self):
        print("initializing Update Thread...")
        update_thread = UpdateThread(self)
        update_thread.start()
        print("Update Thread Running")

    def init_draw_thread(self):
        print("initializing Draw Thread on Main Thread")
        draw_thread = DrawThread(self)
        draw_thread.run()

    def init_input_manager(self):
        print("initializing Input Manager...")

    def set_view(self, new_view: View):
        self.view.before_exit()
        self.view = new_view
    def restart(self):
        self.set_view(AttrView(self))

    def get_view(self):
        return self.view

    def set_framerate(self, value):
        self.framerate = value

    def set_updaterate(self, value):
        self.updaterate = value

    def set_blocked(self, block: ThreadBlock, value: bool):
        if block == ThreadBlock.Draw:
            self.draw_block = value
        elif block == ThreadBlock.Update:
            self.update_block = value
        elif block == ThreadBlock.View:
            self.set_view_block = value
        else:
            raise ValueError('Not a known thread')

    def is_not_blocked(self):
        return (self.draw_block and self.update_block and self.set_view_block) == False

    def get_blocked(self, block: ThreadBlock):
        if block == ThreadBlock.Draw:
            return self.draw_block
        elif block == ThreadBlock.Update:
            return self.update_block
        elif block == ThreadBlock.View:
            return self.set_view_block
        else:
            raise ValueError('Not a known thread')

    def run(self):
        self.init_pygame()
        self.init_input_manager()
        try:
            self.init_update_thread()
            self.init_draw_thread()
        except Exception as e:
            print(e)
            self.is_done = True
            raise e

        pygame.quit()


def main():
    main_app = MainApp()
    main_app.run()


main()
