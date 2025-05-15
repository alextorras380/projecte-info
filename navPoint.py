class NavPoint:
    def __init__(self, number, name, latitude, longitude):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.neighbors = []

    def __repr__(self):
        return f"NavPoint({self.number}, '{self.name}', {self.latitude}, {self.longitude})"


def AddNavNeighbor(n1, n2):
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True



def HaversineDistance(n1, n2):
    from math import radians, sin, cos, sqrt, atan2
    # Radio de la Tierra en km
    R = 6371.0

    lat1 = radians(n1.latitude)
    lon1 = radians(n1.longitude)
    lat2 = radians(n2.latitude)
    lon2 = radians(n2.longitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c