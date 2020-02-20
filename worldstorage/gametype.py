class GameType:

    SURVIVAL = 0
    TIMED = 1
    LAST_MAN = 2
    CIVILIZATION = 3
    EVOLUTION = 4
    SANDBOX = 5

    def __init__(self, **kwargs):
        self.world_type = kwargs.get("world_type", 1)  # DEFAULT WORLD_PLAINS
        self.ctr_types = kwargs.get("ctr_type", "")  # DEFAULT creature1
        self.weather_type = kwargs.get("weather_type", 0)  # DEFAULT MILD WEATHER
        self.win_condition = kwargs.get("win_condition", 0)  # DEFAULT SURVIVAL
