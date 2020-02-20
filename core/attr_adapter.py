import sys

sys.path.insert(0, '../creature')
from ctrattr import CreatureAttributes


def convert(scale_value, attr_min, attr_max):
    scale_range = attr_max - attr_min
    return (scale_range * scale_value) / 100 + attr_min


def weighted_average(values: [], weights: []):
    total_value = 0.0
    total_weight = 0.0

    for i in range(0, len(values)):
        total_value += values[i] * weights[i]
        total_weight += weights[i]

    return total_value / total_weight


def reverse(scale_value):
    return 100 - scale_value


class AttrAdapter:
    def __init__(self, *args, **kwargs):
        # values must be on a scale from 0 - 100 with the total of all values being a max of 300
        self.scale_values = {
            "size": kwargs.get("size", 50),
            "hardiness": kwargs.get("hardiness", 50),
            "speed": kwargs.get("speed", 50),
            "aggression": kwargs.get("aggression", 50),
            "awareness": kwargs.get("awareness", 50),
            "lifespan": kwargs.get("lifespan", 50),
        }

    def get_ctr_attr(self):
        attr_dict = self.get_attr_dict()
        attr = CreatureAttributes(**attr_dict)
        attr.scale_values = [
            self.scale_values["size"],self.scale_values["hardiness"],
            self.scale_values["speed"],self.scale_values["aggression"],
            self.scale_values["awareness"],self.scale_values["lifespan"]]
        return attr

    def get_attr_dict(self):
        scale_size = self.scale_values["size"]
        scale_hardiness = self.scale_values["hardiness"]
        scale_speed = self.scale_values["speed"]
        scale_aggression = self.scale_values["aggression"]
        scale_awareness = self.scale_values["awareness"]
        scale_lifespan = self.scale_values["lifespan"]

        # gets the scales and converts them into a value between 0-100 for each creature attr
        unconverted_attr = {
            "size": weighted_average([scale_size], [1]),
            "health_cap": weighted_average([scale_size], [1]),
            "regen_rate": weighted_average([scale_hardiness], [1]),
            "armor": weighted_average([scale_size, scale_hardiness], [1, 2]),
            "base_damage": weighted_average([scale_size, scale_aggression], [2, 1]),
            "hunger_cap": weighted_average([scale_size], [1]),
            "hunger_loss": weighted_average([reverse(scale_size), reverse(scale_hardiness), reverse(scale_speed)], [2, 1, 1]),
            "thirst_cap": weighted_average([scale_size], [1]),
            "thirst_loss": weighted_average([reverse(scale_size), reverse(scale_hardiness), reverse(scale_speed)], [2, 1, 1]),
            "lifespan": weighted_average([scale_hardiness, scale_lifespan], [1, 3]),
            "maturity_age": weighted_average([scale_lifespan], [1]),
            "max_velocity": weighted_average([reverse(scale_size), scale_speed], [1,1]),
            "steering_force": weighted_average([reverse(scale_size), scale_speed], [1,1.5]),
            "agressiveness": weighted_average([scale_aggression], [1]),
            "sight_range": weighted_average([scale_awareness], [1]),
            "gestation": weighted_average([scale_lifespan], [1]),
            "pregnancy_cooldown": weighted_average([scale_lifespan], [1]),
        }

        for value in unconverted_attr.values():
            if value < 0 or value > 100:
                raise Exception("scaled value must be between 0-100 value was " + str(value))

        # converts each of the 0-100 values into the min and max values for each attr
        converted_values = {
            "size": convert(unconverted_attr["size"], 5, 30),
            "health_cap": convert(unconverted_attr["health_cap"], 50, 200),
            "regen_rate": convert(unconverted_attr["regen_rate"], 5, 10),
            "armor": convert(unconverted_attr["armor"], 5, 50),
            "base_damage": convert(unconverted_attr["base_damage"], 5, 50),
            "hunger_cap": convert(unconverted_attr["hunger_cap"], 75, 125),
            "hunger_loss": convert(unconverted_attr["hunger_loss"], 1, 2),
            "thirst_cap": convert(unconverted_attr["thirst_cap"], 75, 125),
            "thirst_loss": convert(unconverted_attr["thirst_loss"], 1,2),
            "lifespan": convert(unconverted_attr["lifespan"], 150, 400),
            "maturity_age": convert(unconverted_attr["maturity_age"], 25, 100),
            "steering_force": convert(unconverted_attr["steering_force"], 2, 6),
            "max_velocity": convert(unconverted_attr["max_velocity"], 2, 10),
            "agressiveness": convert(unconverted_attr["agressiveness"], 0.1, 1),
            "sight_range": convert(unconverted_attr["sight_range"], 75, 250),
            "gestation": convert(unconverted_attr["gestation"], 5, 10),
            "pregnancy_cooldown": convert(unconverted_attr["pregnancy_cooldown"], 5, 10),
        }
        return converted_values
