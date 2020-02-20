from inputManager import *
from listener_interface import _MouseMoveListener
from UIcomponent import *

class InputTest:
    class TestMouseMoveListener(_MouseMoveListener):
        def mouse_moved(self,event):
            assert event.type==pygame.MOUSEMOTION,"test move listener event type error"
            x,y=event.pos
            print("x: ",x," y: ",y)
    
    class TestButton(Button):
    
        def mouse_clicked(self,event):
            print(event.pos)
        def draw(self,screen):
            raise NotImplementedError

    def test_mouse_move(self):
        pygame.init()
        screen=pygame.display.set_mode((100,150))
        pygame.draw.rect(screen,(000,255,000),(25,25,0,0),0)
        pygame.display.update()

        running=True
        mml=self.TestMouseMoveListener()
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                if event.type==pygame.MOUSEMOTION:
                    mml.mouse_moved(event)

        x=self.TestMouseMoveListener()
        print(x.mouse_moved(4))

    #test1()
    def test_singleton(self):
        print("start test")
        x=InputManager()
        print("singleton ", x.instance)
        print("\nputing tacos in\n")
        x.instance.add_mouse_move_listener("tacos")
        print(x.instance.mouse_move_listeners)
        print("making new instance\n")
        y=InputManager().instance
        print(y.mouse_move_listeners)
        z=InputManager().instance
        assert z.mouse_move_listeners[0]=="tacos"

    def test_singleton2(self):
        z=InputManager().instance
        print("agian ",z.mouse_move_listeners)

    def test_remove_listener(self):
        print("\n\n test romove listener")
        x=InputManager().instance
        z=self.TestMouseMoveListener()
        print("\n",x.mouse_move_listeners)
        x.add_mouse_move_listener(z)
        print("\n",x.mouse_move_listeners)
        x.remove_listener(z)
        print("\n",x.mouse_move_listeners)
        x.remove_listener("tacos")

    def test_handle_evnets(self):
        pygame.init()
        screen=pygame.display.set_mode((500,850))
        pygame.draw.rect(screen,(000,255,000),(25,25,0,0),0)
        pygame.display.update()

        running=True
        y=InputManager().instance
        mml=self.TestMouseMoveListener()
        y.add_mouse_move_listener(mml)
        while running:
            y.handle_events(pygame.event.get())
        
    def test_button(self):
        pygame.init()
        screen=pygame.display.set_mode((500,850))
        pygame.display.update()

        running=True
        y=InputManager().instance
        botton_rect=pygame.Rect(25,25,5,5)
        tb=self.TestButton((000,255,000),botton_rect,0)
        tb.draw(screen)
        y.add_mouse_click_listener(tb)
        while running:
            event_list=pygame.event.get()
            for e in event_list:
                if e.type==pygame.QUIT:
                    running=False
            y.handle_events(event_list)

    def test(self):
        self.test_singleton()
        self.test_singleton2()
        self.test_remove_listener()
        #self.test_handle_evnets()
        self.test_button()

def main():
    print("\n bananas\n")
    tests=InputTest()
    tests.test()
main()
