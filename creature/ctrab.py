''' A creature ability. '''
import abc


class CreatureAbility(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def draw(self, screen, ctr):
        pass

    @abc.abstractmethod
    def update(self, ctr):
        pass

    @abc.abstractmethod
    def __str__(self):
        pass
