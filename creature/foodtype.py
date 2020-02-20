''' Type of food. '''
from enum import IntEnum


class FoodType(IntEnum):
    WATER = 0
    MEAT = 1
    PLANTS = 2

    def __eq__(self, other):
        return self.value == other.value
