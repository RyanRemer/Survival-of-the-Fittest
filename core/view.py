import abc

class View(abc.ABC):
    @abc.abstractmethod
    def draw(self, screen):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def add_component(self, comp):
        pass

    @abc.abstractmethod
    def remove_component(self, comp):
        pass

    @abc.abstractmethod
    def before_exit(self):
        pass
