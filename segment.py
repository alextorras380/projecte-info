from node import Distance


class Segment:
    def __init__(self, name, origin, destination, color='g-'):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = Distance(origin, destination)
        self.color = color