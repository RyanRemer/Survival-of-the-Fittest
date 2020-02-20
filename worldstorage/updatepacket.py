# Made by Brian Robinson


class UpdatePacket:
        def __init__(self, land_features, same_creatures, other_creatures, resources, world):
                self.land_features = land_features
                self.same_creatures = same_creatures
                self.other_creatures = other_creatures
                self.resources = resources
                self.world = world
