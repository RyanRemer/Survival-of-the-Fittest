''' Interface for all Creatures. '''

import sys
import time

import numpy as np
import spawn

from body import BodyType, Body
from ctrattr import CreatureAttributes
from ctrid import CreatureID
from spectemp import SpeciesTemplate

sys.path.insert(0, '../ai')
from aistate import NeutralState

sys.path.insert(0, '../worldstorage')
from resource import Resource
from foodtype import FoodType

class Creature():

    def __init__(self, template, **kwargs):
        self.id: CreatureID = CreatureID()
        self.attributes: CreatureAttributes = kwargs.get("attributes", CreatureAttributes())
        self.template: SpeciesTemplate = template
        self.ai = NeutralState()
        self.health: float = kwargs.get("health", 100)
        self.time_born: float = time.time()
        self.age: float = 0
        self.last_pregnancy_start:float = 0;
        self.preggers: bool = False;
        self.mate:Creature = None;
        self.hunger: float = kwargs.get("hunger", 100)
        self.thirst: float = kwargs.get("thirst", 100)
        # self.status: CreatureStatus = kwargs.get("status", CreatureStatus())
        self.position: np.array = kwargs.get("position", np.array([0.0, 0.0]))
        self.velocity: np.array = kwargs.get("velocity", np.array([0.0, 0.0]))
        self.body: Body = kwargs.get("body", Body(BodyType.TRIANGLE))
        self.update_tick = 0
        self.world = None

        # *** DO NOT TOUCH *** #
        # creature constants 
        self.CRIT_HUNGER = 10
        # *** DO NOT TOUCH *** #

    def __str__(self):
        message = (
            f"ID: {self.id}\n"
            f"attributes: {self.attributes}\n"
            f"template: {self.template}\n"
            f"health: {self.health}\n"
            f"age: {self.age}\n"
            f"hunger: {self.hunger}\n"
            f"thirst: {self.thirst}\n"
            # f"status: {self.status}\n"
            f"position: {self.position}\n"
            f"velocity: {self.velocity}\n"
        )
        return message

    ''' Update the current creature stats.
        @param update_packet - stats about the world. For the AIState.
        magnitude of u-v must be <= steering force
    '''

    def update(self, packet):
        for ability in self.template.abilities:
            ability.update(self)

        if self.health < self.attributes.health_cap:  # Update health #
            if self.health + self.attributes.regen_rate > self.attributes.health_cap:
                self.health = self.attributes.health_cap
            else:
                self.health += self.attributes.regen_rate
        if self.thirst > 0 and self.update_tick == 0:  # Update thirst #
            if self.thirst - self.attributes.thirst_loss < 0:
                self.thirst = 0
            else:
                self.thirst -= self.attributes.thirst_loss
        if self.hunger > 0 and self.update_tick == 0:  # Update hunger #
            if self.hunger - self.attributes.hunger_loss < 0:
                self.hunger = 0
            else:
                self.hunger -= self.attributes.hunger_loss
        desired, next_state = self.ai.update(self, packet);
        desired *= self.attributes.max_velocity  # Go as fast as possible
        diff = desired - self.velocity  # Subtract desired velocity by current velocity
        if self.ai.mag(diff) > self.attributes.steering_force:  # Limit diff by steering force
            diff = self.ai.norm(diff) * self.attributes.steering_force
        np.add(self.velocity, diff, out=self.velocity, casting="unsafe")
        if self.ai.mag(self.velocity) > self.attributes.max_velocity:  # Limit velocity by max_velocity
            self.velocity = self.ai.norm(self.velocity) * self.attributes.max_velocity
        new_position = np.add(self.position, self.velocity)
        packet.world.move_creature(self, self.position, new_position)
        self.ai = next_state
        self.update_tick = (self.update_tick + 1) % 10
        if self.health < 1 or self.thirst < 1 or self.hunger < 1:
            self.die()
        self.age = int(time.time() - self.time_born)  # Update age #
        if self.age >= self.attributes.lifespan:
            self.die()
        if self.age >= self.attributes.gestation + self.last_pregnancy_start and self.preggers:
            spawn.SpawnManager.instance.spawn_child_creature(self, self.mate, self.position)
            self.mate = None
            self.preggers = False

    ''' Draw the creature by calling the body. '''

    def draw(self, screen):
        for ability in self.template.abilities:
            ability.draw(screen, self)

        self.body.draw(screen, self.attributes.size, self.position, self.velocity, not self.preggers)

    def register(self, world):
        self.world = world

    def die(self):
        self.world.remove_creature(self)
        self.world.add_resource(Resource(4 * self.attributes.size, self.position, FoodType.MEAT))
