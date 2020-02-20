import threading
import time

from thread_block import ThreadBlock


class UpdateThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app

    def run(self):
        while not self.app.is_done:
            if self.app.is_not_blocked():
                self.app.set_blocked(ThreadBlock.Update, True)

                # update the current view
                self.app.view.update()

                self.app.set_blocked(ThreadBlock.Update, False)
            time.sleep(1 / self.app.updaterate)
