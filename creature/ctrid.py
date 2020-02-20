''' The unique identifier for a Creature. '''

# TODO: Possible generation of random string for ID when created

class CreatureID():
    id = 0
    def __init__(self):
        self.id = CreatureID.id
        CreatureID.id += 1

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return self.id

    def equals(self, other):
        return self.__eq__(other)

    def __eq__(self, other):
        return self.id == other.id
