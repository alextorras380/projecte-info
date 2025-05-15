from navPoint import HaversineDistance

class NavSegment:
    def __init__(self, origin_number, destination_number, distance=None):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance

    def __repr__(self):
        return f"NavSegment({self.origin_number}->{self.destination_number}, {self.distance:.2f}km)"