''' The status of a Creature. '''

from ctrattr import CreatureAttributes

class CreatureStatus():
    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            self.modifiers: CreatureAttributes = args[0]
        else:
            self.modifiers: CreatureAttributes = kwargs.get("modifiers", CreatureAttributes())

    def __str__(self):
        return str(self.modifiers)

    def effect(self, creature):
        pass