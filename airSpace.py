from navPoint import NavPoint, AddNavNeighbor
from navSegment import NavSegment
from navAirport import NavAirport


class AirSpace:
    def __init__(self):
        self.nav_points = []
        self.nav_segments = []
        self.nav_airports = []

    def find_navpoint_by_number(self, number):
        for point in self.nav_points:
            if point.number == number:
                return point
        return None

    def find_navpoint_by_name(self, name):
        for point in self.nav_points:
            if point.name == name:
                return point
        return None

    def __repr__(self):
        return f"AirSpace({len(self.nav_points)} points, {len(self.nav_segments)} segments, {len(self.nav_airports)} airports)"




def LoadAirspaceFromFiles(airspace, nav_file, seg_file, aer_file):
    # Cargar puntos de navegación
    with open(nav_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            number = int(parts[0])
            name = parts[1]
            latitude = float(parts[2])
            longitude = float(parts[3])
            airspace.nav_points.append(NavPoint(number, name, latitude, longitude))

    # Cargar segmentos
    with open(seg_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            origin = int(parts[0])
            destination = int(parts[1])
            distance = float(parts[2])
            airspace.nav_segments.append(NavSegment(origin, destination, distance))

            # Añadir vecinos
            origin_node = airspace.find_navpoint_by_number(origin)
            dest_node = airspace.find_navpoint_by_number(destination)
            if origin_node and dest_node:
                AddNavNeighbor(origin_node, dest_node)

    # Cargar aeropuertos
    with open(aer_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            name = parts[0]
            sids = [int(sid) for sid in parts[1].split(';') if sid]
            stars = [int(star) for star in parts[2].split(';') if star]
            airspace.nav_airports.append(NavAirport(name, sids, stars))

    return airspace