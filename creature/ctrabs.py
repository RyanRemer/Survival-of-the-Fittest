from enum import IntEnum

from ctrab import CreatureAbility

frames_per_second = 30


class AbilityIds(IntEnum):
    SecondWind = 0,
    PoisonousFlesh = 1,
    EvenStronger = 2,
    RandomSprints = 3,


class SecondWind(CreatureAbility):

    def __init__(self):
        super().__init__()
        self.used_up = False
        self.cool_down_duration = 30
        self.cool_down_time = 0

    def draw(self, screen, ctr):
        pass

    def update(self, ctr):
        health = ctr.health

        if self.cool_down_time > 0:
            self.cool_down_time -= 1
        elif health < 25:
            ctr.health = 100
            self.cool_down_time = self.cool_down_duration * frames_per_second


    def __str__(self):
        return "Second Wind"


class PoisonousFlesh(CreatureAbility):

    def draw(self, screen, ctr):
        pass

    def update(self, ctr):
        health = ctr.health

        if health < 1:
            ctr.world.remove_creature(self)

    def __str__(self):
        return "Poisonous Flesh"


class EvenStronger(CreatureAbility):

    def draw(self, screen, ctr):
        pass

    def update(self, ctr):
        health = ctr.health
        health_cap = ctr.attributes.health_cap

        if health >= health_cap * 0.75:
            ctr.attributes.base_damage = 50

    def __str__(self):
        return "Even Stronger"


class RandomSprints(CreatureAbility):
    def draw(self, screen, ctr):
        pass

    def update(self, ctr):
        if self.cool_down_time > 0:
            # wait 60 seconds
            self.normal_velocity = ctr.attributes.max_velocity
            self.cool_down_time -= 1
        elif self.sprint_time > 0:
            # sprint for 2 seconds
            ctr.attributes.max_velocity = 10
            self.sprint_time -= 1
        else:
            # reset
            ctr.attributes.max_velocity = self.normal_velocity
            self.cool_down_time = self.cool_down_duration * frames_per_second
            self.sprint_time = self.sprint_duration * frames_per_second

    def __init__(self):
        super().__init__()
        self.cool_down_duration = 30
        self.sprint_duration = 3
        self.cool_down_time = self.cool_down_duration * frames_per_second
        self.sprint_time = self.sprint_duration * frames_per_second

    def __str__(self):
        pass
