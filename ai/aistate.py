import sys
sys.path.insert(0, '..')

from abc import ABCMeta, abstractmethod
from creature.foodtype import FoodType
import numpy as np
import random as r
import math
import inspect


class AIState:
    """
    The base class for determining a creature's behavior
    """
    def __init__(self):
        self.wander_angle = r.randint(-179,179)

    BASE_DAM_SIG_THRESH = .15  # if other_creature.base_damage deals >= 15% of this_creature.health -> minor threat
    SIZE_SIG_THRESH = .80  # if other_creature.size  >= 80% of this_creature.size -> minor threat
    LOW_HEALTH_SIG_THRESH = .10  # when this_creature.health <= 10% of this_creature.health_cap, they have low health

    #@abstractmethod
    def update(self, packet):
        raise NotImplementedError
    
    def mag(self, v: np.ndarray):
        """
        Returns the magnitude of a numpy ndarray
        (helper function)
        """
        return np.sqrt(v.dot(v))

    def magsq(self, v: np.ndarray):
        """
        Returns the magnitude squared of a numpy ndarray (faster than mag())
        (helper function)
        """
        return v.dot(v)

    def norm(self, v: np.ndarray):
        """
        Returns a vector that is the same direction as the one passed in, with length 1
        (helper function)
        """
        mag = self.mag(v)
        if mag == 0:
            return np.array([0.0,0.0])
        return v / mag

    def distsq(self, v1:np.ndarray, v2:np.ndarray):
        """
        Returns a scalar of the distance sqared between v1 and v2
        """
        return self.magsq(v1-v2)

    def wander(self, heading:np.ndarray, radius:float):
        """
        Returns a random, normalized acceleration vector within a small range of a heading direction
        """
        # Ensure a valid heading #
        if self.magsq(heading) == 0:
            x = r.randint(-100, 100)
            y = r.randint(-100, 100)
            heading = np.array([x,y])
        heading = self.norm(heading)

        # Project out and get a randomized acceleration #
        projection = heading * radius * 2
        self.wander_angle += r.randint(-5,5)
        r_rad = self.wander_angle/180.0 * math.pi
        x = math.cos(r_rad)
        y = math.sin(r_rad)
        r_circle_cord = np.array((x,y))
        
        # Final result is the projected position on the circle #
        return self.norm(projection + r_circle_cord)

    def seek(self, pos:np.ndarray, target:np.ndarray):
        """
        Returns a normalized vector from a given position to a target
        Note: Multiplying this by a negative number simulates constant fleeing
        """
        return self.norm(target - pos)

    def arrive(self, pos:np.ndarray, target:np.ndarray, radius:float):
        """
        If position is not within radius of target:
            Returns a normalized vector from a given position to a target
        Else
            Returns a scaled vector (magnitude between 0 and 1) based on the distance to the target/radius
        Note: Multiplying this by a negative number simulates proximity-based fleeing
        """
        desired_velocity = target - pos
        distance = self.mag(desired_velocity)
        desired_velocity = self.norm(desired_velocity)
        if distance <= radius:
            if distance > 0:
                desired_velocity /= distance/radius #Same as multiplying
            else:
                desired_velocity = np.array([0.0,0.0])
        return desired_velocity

    def separate(self, pos:np.ndarray, targets:list, radius:float):
        """
        Returns a normalized vector in a direction that takes it away from all targets within a certain distance
        Note targets is a list of position vectors
        """
        total = np.array([0.0,0.0])
        for target in targets:
            difference = pos - target
            distance = self.mag(difference)
            if distance <= radius:
                if distance == 0:
                    difference = np.array([100,100])
                else:
                    difference = self.norm(difference)
                    difference /= distance
                total += difference
        return self.norm(total)

    def group(self, pos:np.ndarray, targets:list, radius:float):
        """
        Returns a normalized vector in the direction of the center of all targets within a certain distance
        Note: targets is a list of position vectors
        """
        total = np.array([0.0,0.0])
        for target in targets:
            difference = target - pos
            distance = self.mag(difference)
            if distance <= radius:
                difference = self.norm(difference)
                total += difference
        return self.norm(total)

    def align(self, pos:np.ndarray, targets_vel:list, targets_pos:list, radius:float):
        """
        Returns a normalized vector that is the average direction of the targets within a certain distance
        Note: targets_vel is a list of velocity vectors and targets_pos is a list of position vectors
        ***ASSUMES targets_vel AND targets_pos ARE OF EQUAL LENGTH***
        """
        total = np.array([0.0,0.0])
        for i in range(len(targets_vel)):
            t_pos = targets_pos[i]
            t_vel = targets_vel[i]
            difference = t_pos - pos
            distance = self.mag(difference)
            if distance <= radius:
                total += t_vel
        return self.norm(total)

    def major_threats(self, this_creature, packet):
        """
        Get all nearby creatures that are major threats to 'this_creature'
        TODO: **Test**
        :type this_creature: Creature
        :type packet: UpdatePacket
        :param this_creature:
        :param packet:
        """
        # minor threat(s) exist? If none, there are no major threats
        minor_threats = self.minor_threats(this_creature, packet)
        if len(minor_threats) > 0:
            major_threats = []

            # if has low health, ALL minor threats are major threats
            if self.has_low_health(this_creature):
                return minor_threats

            # TODO: self.aggressiveness (**SPECIAL CASE**)
            # size difference, base damage diff
            for minor_threat in minor_threats:
                if (self.has_size_diff(this_creature, minor_threat)
                        or self.has_base_dam_diff(minor_threat, this_creature)):
                    major_threats += [minor_threat]
            return major_threats
        return []
    # ## END FEELS_MAJOR_THREAT_FROM() ## #

    def minor_threats(self, this_creature, other_creatures):
        """
        Get all nearby creatures that are -AT LEAST- a minor threat to 'this_creature'
        TODO: **Test**
        :type this_creature: Creature
        :type other_creatures: list
        :param this_creature:
        :param other_creatures:
        :return:
        """
        # other creature(s)' size is bigger than the threshold of being significantly smaller than you -OR-
        # other creature(s)' base_dam is higher than the threshold of being significantly lower than you
        minor_threats = []
        for other_creature in other_creatures:
            # size difference, base damage diff
            if (not self.has_size_diff(this_creature, other_creature)
                    or not self.has_base_dam_diff(this_creature, other_creature)):
                minor_threats += [other_creature]
        return minor_threats
    # ## END MINOR_THREAT_TO() ## #

    def get_threats(self, this_creature, other_creatures):
        """ Gets both major and minor threats within range """
        minor = self.minor_threats(this_creature, other_creatures)
        major = self.major_threats(this_creature, minor)
        return (minor, major)

    def has_low_health(self, this_creature):
        """
        Determine if this_creature has significantly low health
        TODO: **Test**
        :type this_creature: Creature
        :param this_creature:
        :return:
        """
        return this_creature.health <= this_creature.attributes.health_cap * self.LOW_HEALTH_SIG_THRESH
    # ## END HAS_LOW_HEALTH

    def has_size_diff(self, this_creature, other_creature, major=False):
        """
        This_creature has a significantly greater size than other_creature. **BASED ON this_creature PERCEPTION**
        If 'major' flag is set: detemine if this_creature.size << other_creature.size (major threat)
        else: this_creature.size >> other_creature.size (minor threat)
        TODO: **Test**
        :type this_creature: Creature
        :type other_creature: Creature
        :param this_creature:
        :param other_creature:
        :return:
        """
        if major:
            return this_creature.attributes.size < (1-this_creature.attributes.aggressiveness)*self.SIZE_SIG_THRESH*other_creature.attributes.size
        return this_creature.attributes.size > (1-this_creature.attributes.aggressiveness)*self.SIZE_SIG_THRESH*other_creature.attributes.size
    # ## END HAS_SIZE_DIFF() ## #

    def has_base_dam_diff(self, this_creature, other_creature, major=False):
        """
        this_creature has a significantly higher base_damage level than other_creature
        TODO: **Test**
        :type this_creature: Creature
        :type other_creature: Creature
        :param this_creature:
        :param other_creature:
        :return:
        """
        if major:
            return this_creature.attributes.base_damage < (1-this_creature.attributes.aggressiveness)*self.BASE_DAM_SIG_THRESH*other_creature.attributes.base_damage
        return this_creature.attributes.base_damage > (1-this_creature.attributes.aggressiveness)*self.BASE_DAM_SIG_THRESH*other_creature.attributes.base_damage
    # ## END HAS_BASE_DAM_DIFF() ## #



class NeutralState(AIState):
    def __init__(self):
        super().__init__()

    def update(self, this_creature, packet):
        my_attr = this_creature.attributes	
        # Is there something to run from?
            # TODO: check for threat and switch to wary state
            
        # Am I thirsty/hungry?
        hungry = this_creature.hunger <= my_attr.hunger_cap * 0.7
        thirsty = this_creature.thirst <= my_attr.thirst_cap * 0.7
        if hungry or thirsty:
            return (np.array([0.0,0.0]), FindResourceState())

        # Do I wanna have babies?
        is_mature = this_creature.age >= my_attr.maturity_age
        last_birth = this_creature.last_pregnancy_start + my_attr.gestation
        cooldown_over = this_creature.age >= last_birth + my_attr.gestation
        if(is_mature and cooldown_over):
            print(f"{this_creature.id} wants to have a baby")
            return(np.array([0.0,0.0]), FindMateState())

        # Otherwise wander with the herd
        friends = packet.same_creatures
        friend_pos = [friend.position for friend in friends]
        friend_vel = [friend.velocity for friend in friends]
        resource_pos = [res.position for res in packet.resources]
        wander = self.wander(this_creature.velocity, 20.0)
        avoid_resources = self.separate(this_creature.position, resource_pos, my_attr.size * 2)
        if len(friends) > 0:
            group = self.group(this_creature.position, friend_pos, my_attr.sight_range)
            align = self.align(this_creature.position, friend_vel, friend_pos, my_attr.sight_range)
            separate = self.separate(this_creature.position, friend_pos, my_attr.size * 2)
            return ((group + separate + align + wander + avoid_resources) / 5, self)
        return ((wander + avoid_resources * 0.5) / 2, self)



class FindResourceState(AIState):
    def __init__(self):
        super().__init__()

    def update(self, this_creature, packet):
        my_attr = this_creature.attributes
        my_species = this_creature.template

        major, minor = self.get_threats(this_creature, packet.other_creatures)
        if len(major) > 0:
            return (self.separate(this_creature.position, [c.position for c in major], my_attr.sight_range), self)

        if my_species.food_type == FoodType.MEAT:
            potential_prey = packet.other_creatures

            for creature in major:
                potential_prey.remove(creature)

            if len(potential_prey) > 0:
                return (self.seek(this_creature.position, potential_prey[0].position), AttackState())

        closest_food = None
        food_dist = float('inf')
        closest_water = None
        water_dist = float('inf')

        for resource in packet.resources:
            if resource.food_type == my_species.food_type:
                dist = self.distsq(this_creature.position, resource.position)
                if dist < food_dist:
                    closest_food = resource
                    food_dist = dist
            if resource.food_type == FoodType.WATER:
                dist = self.distsq(this_creature.position, resource.position)
                if dist < water_dist:
                    closest_water = resource
                    water_dist = dist

        # If we are close enough consume the resource
        if math.sqrt(food_dist) < my_attr.size:
            to_fill = my_attr.hunger_cap - this_creature.hunger
            amount = min(closest_food.value, to_fill, my_attr.hunger_loss * 2)
            resource.consume(amount)
            this_creature.hunger += amount
        if math.sqrt(water_dist) < my_attr.size:
            to_fill = my_attr.thirst_cap - this_creature.thirst
            amount = min(closest_water.value, to_fill, my_attr.thirst_loss * 2)
            resource.consume(amount)
            this_creature.thirst += amount

        full = this_creature.hunger > my_attr.hunger_cap * 0.95
        hydrated = this_creature.thirst > my_attr.thirst_cap * 0.95
        if full and hydrated:
            return (np.array([0.0,0.0]), NeutralState())

        # If we aren't full yet, keep looking for more resources
        desired = np.array([0.0,0.0])
        if not full and this_creature.hunger < this_creature.thirst and closest_food != None:
            desired = self.arrive(this_creature.position, closest_food.position, my_attr.max_velocity)
        elif not hydrated and closest_water != None:
            desired = self.arrive(this_creature.position, closest_water.position, my_attr.max_velocity)
        else:
            desired = self.wander(this_creature.velocity, my_attr.steering_force)
        
        return (desired, self)



class AttackState(AIState):

    PREDATOR_BOOST = 100

    def __init__(self):
        super().__init__()

    def update(self, this_creature, packet):
        # get minor threats
        minor_threats = self.minor_threats(this_creature, packet.other_creatures)

        # are there any creatures that I need to flee from? If so, FLEE.
        major_threats = self.major_threats(this_creature, minor_threats)
        if len(major_threats) > 0:
            return (self.separate(this_creature.position, [other.position for other in major_threats], (this_creature.attributes.size*this_creature.attributes.FEAR_FACTOR)), NeutralState())

        # extreme hunger or (sufficient health and aggression)
        if ((this_creature.hunger < this_creature.CRIT_HUNGER) 
                or (not self.has_low_health(this_creature) 
                and (this_creature.attributes.aggressiveness >= this_creature.attributes.AGGR_PREDATOR))):
            attack_target = None

            # attack the closest creature
            closest_ctr_pos = float("inf")
            for other_creature in packet.other_creatures:
                dist = self.distsq(this_creature.position, other_creature.position)
                if dist < closest_ctr_pos:
                    closest_ctr_pos = dist
                    attack_target = other_creature

            # Wander if no target
            if attack_target is None:
                return (self.wander(this_creature.velocity, 20), self)

            # if within attack range: attack creature ; else: keep moving towards creature
            # (TODO: STRETCH GOAL - ATTACK ANIMATION)
            if this_creature.attributes.size + attack_target.attributes.size <= closest_ctr_pos:
                if self.attack_ctr(this_creature, attack_target):
                    return (np.array([0.0,0.0]), NeutralState())
                return (this_creature.velocity, AttackState())
            else:
                return (self.arrive(this_creature.position, attack_target.position, attack_target.attributes.size), self)
        else:
            return (self.norm(this_creature.velocity), NeutralState())
    
    def attack_ctr(self, this_creature, attack_target):
        """
        <this_creature> attempts to deal damage to <attack_target> (creature).
        :param this_creature
        :param attack_target
        """
        attack_target.health -= (this_creature.attributes.base_damage*self.PREDATOR_BOOST - attack_target.attributes.armor)
        return attack_target.health <= 0



class FindMateState(AIState):

    def __init__(self):
        super().__init__()

    def update(self, this_creature, packet):
        my_attr = this_creature.attributes
        my_species = this_creature.template

        minor, major = self.get_threats(this_creature, packet.other_creatures)
        if len(major) > 0:
            return (self.separate(this_creature.position, [c.position for c in major], my_attr.sight_range), self)

        potential_mate = None;
        friend_distance = float('inf')
        friends = packet.same_creatures

        for friend in friends:
            # CONSENT PEOPLE!! #
            friend_state = friend.ai
            if not isinstance(friend_state, FindMateState):
                continue
            elif potential_mate != None and potential_mate.age < potential_mate.attributes.maturity_age:
                continue
            dist = self.distsq(this_creature.position, friend.position)
            if dist < friend_distance:
                potential_mate = friend
                friend_distance = dist

        if potential_mate != None and math.sqrt(friend_distance) <= 2 * my_attr.size:
            print(f"{this_creature.id} is trying to mate with {potential_mate.id}")
            this_creature.last_pregnancy_start = this_creature.age
            potential_mate.last_pregnancy_start = potential_mate.age
            potential_mate.state = NeutralState()
            this_creature.mate = potential_mate
            this_creature.preggers = True
            return (np.array([0.0,0.0]), NeutralState())

       # Otherwise wander with the herd
        friend_pos = [friend.position for friend in friends]
        friend_vel = [friend.velocity for friend in friends]
        resource_pos = [res.position for res in packet.resources]
        wander = self.wander(this_creature.velocity, 20.0)
        avoid_resources = self.separate(this_creature.position, resource_pos, my_attr.size * 2)
        if len(friends) > 0:
            group = self.group(this_creature.position, friend_pos, my_attr.sight_range)
            align = self.align(this_creature.position, friend_vel, friend_pos, my_attr.sight_range)
            separate = self.separate(this_creature.position, friend_pos, my_attr.size * 4)
            return ((group + separate + align + wander + avoid_resources) / 5, self)
        return ((wander + avoid_resources * 0.5) / 2, self) 