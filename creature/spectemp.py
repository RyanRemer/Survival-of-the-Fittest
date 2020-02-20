''' The template for a Species. '''

from ctrattr import CreatureAttributes
from ctrab import CreatureAbility
from body import BodyType
from foodtype import FoodType

class SpeciesID():
    id = 0
    def __init__(self):
        self.id = SpeciesID.id
        SpeciesID.id += 1

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other.id

class SpeciesTemplate():
    def __init__(self, *args, **kwargs):
        self.id: SpeciesID = SpeciesID()
        self.base_attributes = kwargs.get("base_attributes", CreatureAttributes())
        self.player_adjustments: CreatureAttributes = kwargs.get("player_adjustments", CreatureAttributes())
        self.recent_creatures: list() = kwargs.get("recent_creatures", list())
        self.abilities: list() = kwargs.get("abilities", list())
        self.body_type: BodyType = kwargs.get("body_type", BodyType.TRIANGLE)
        self.food_type: FoodType = kwargs.get("food_type", FoodType.MEAT)

    def __str__(self):
        message = (
            f"Player adjustments: {self.player_adjustments}\n"
            f"Recent creatures: {self.recent_creatures}\n"
            f"abilities: {self.abilities}\n"
            f"body type: {self.body_type}\n"
            f"food type: {self.food_type}\n"
        )
        return message

    def __eq__(self, other):
        if other is None:
            return False

        return self.id == other.id
