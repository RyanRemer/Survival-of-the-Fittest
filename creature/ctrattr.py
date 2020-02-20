''' Attributes of a Creature. '''


class CreatureAttributes:

    ''' Constructor. Looks for keyword in initialization. If not there, use default value. '''
    def __init__(self, *args, **kwargs):
        # if you add an attr, add it to attr_adapter in the core library!!!

        self.size: float = kwargs.get("size", 0)
        self.health_cap: float = kwargs.get("health_cap", 0)
        self.regen_rate: float = kwargs.get("regen_rate", 0)
        self.armor: float = kwargs.get("armor", 0)
        self.base_damage: float = kwargs.get("base_damage", 0)
        self.hunger_cap: float = kwargs.get("hunger_cap", 0)
        self.hunger_loss: float = kwargs.get("hunger_loss", 0)
        self.thirst_cap: float = kwargs.get("thirst_cap", 0)
        self.thirst_loss: float = kwargs.get("thirst_loss", 0)
        self.lifespan: float = kwargs.get("lifespan", 0)
        self.maturity_age: float = kwargs.get("maturity_age", 0)
        self.max_velocity: float = kwargs.get("max_velocity", 0)
        self.steering_force: float = kwargs.get("steering_force", 0)
        self.aggressiveness: float = kwargs.get("aggressiveness", 0)
        self.sight_range: float = kwargs.get("sight_range", 0)
        self.gestation: float = kwargs.get("gestation", 0)
        self.pregnancy_cooldown: float = kwargs.get("pregnancy_cooldown", 0)

        # *** DO NOT TOUCH *** #
        # creature constants 
        self.AGGR_PREDATOR = 0.8
        self.FEAR_FACTOR = 15
        # *** DO NOT TOUCH *** #


    ''' toString function. '''
    def __str__(self):
        message = (
            f"size: {self.size}\n"
            f"health_cap: {self.health_cap}\n"
            f"regen_rate: {self.regen_rate}\n"
            f"armor: {self.armor}\n"
            f"base_damage: {self.base_damage}\n"
            f"hunger_cap: {self.hunger_cap}\n"
            f"hunger_loss: {self.hunger_loss}\n"
            f"thirst_cap: {self.thirst_cap}\n"
            f"thirst_loss: {self.thirst_loss}\n"
            f"lifespan: {self.lifespan}\n"
            f"maturity_age: {self.maturity_age}\n"
            f"max_velocity: {self.max_velocity}\n"
            f"steering_force: {self.steering_force}\n"
            f"agressiveness: {self.agressiveness}\n"
            f"sight_range: {self.sight_range}\n"
            f"gestation: {self.sight_range}\n"
            f"pregnancy_cooldown: {self.sight_range}\n"
        )
        return message

    ''' Overload add (+) operator.
        @param other - Another CreatureAttributes() object.
        @result - A new CreatureAttributes() object whose attributes are the sum of other's and this' attributes. '''
    def __add__(self, other):
        return CreatureAttributes(
            size=self.size+other.size,
            health_cap=self.health_cap+other.health_cap,
            regen_rate=self.regen_rate+other.regen_rate,
            armor=self.armor+other.armor,
            base_damage=self.base_damage+other.base_damage,
            hunger_cap=self.hunger_cap+other.hunger_cap,
            hunger_loss=self.hunger_loss+other.hunger_loss,
            thirst_cap=self.thirst_cap+other.thirst_cap,
            thirst_loss=self.thirst_loss+other.thirst_loss,
            lifespan=self.lifespan+other.lifespan,
            maturity_age=self.maturity_age+other.maturity_age,
            max_velocity=self.max_velocity+other.max_velocity,
            steering_force=self.steering_force+other.steering_force,
            agressiveness=self.agressiveness+other.agressiveness,
            sight_range=self.sight_range+other.sight_range,
            gestation=self.gestation+other.gestation,
            pregnancy_cooldown=self.pregnancy_cooldown+other.pregnancy_cooldown
        )

    ''' Overload division (/) operator by a number.
        @param num - A number for all attributes to be divided by.
        @result - A new CreatureAttributes() object whose attributes are divided by num. '''
    def __truediv__(self, num):
        return CreatureAttributes(
            size=self.size/num,
            health_cap=self.health_cap/num,
            regen_rate=self.regen_rate/num,
            armor=self.armor/num,
            base_damage=self.base_damage/num,
            hunger_cap=self.hunger_cap/num,
            hunger_loss=self.hunger_loss/num,
            thirst_cap=self.thirst_cap/num,
            thirst_loss=self.thirst_loss/num,
            lifespan=self.lifespan/num,
            maturity_age=self.maturity_age/num,
            max_velocity=self.max_velocity/num,
            steering_force=self.steering_force/num,
            agressiveness=self.agressiveness/num,
            sight_range=self.sight_range/num,
            gestation=self.gestation/num,
            pregnancy_cooldown=self.pregnancy_cooldown/num
        )
        
