from airSpace import AirSpace, LoadAirspaceFromFiles

print("=== Testing AirSpace ===")
airspace = AirSpace()

# Cargar datos de prueba (necesitarías archivos de prueba)
# airspace = LoadAirspaceFromFiles(airspace, "Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")

# Simular algunos datos para prueba
airspace.nav_points.append(NavPoint(6063, "IZA.D", 38.8725, 1.3733))
airspace.nav_points.append(NavPoint(6937, "LAMPA", 39.55, 2.7333))
airspace.nav_segments.append(NavSegment(6063, 6937, 48.55701))
airspace.nav_airports.append(NavAirport("LEIB", [6063], [6063]))

print("\nNavPoints:")
for point in airspace.nav_points:
    print(point)

print("\nNavSegments:")
for seg in airspace.nav_segments:
    print(seg)

print("\nNavAirports:")
for airport in airspace.nav_airports:
    print(airport)

# Probar funciones de búsqueda
print("\nFind by number (6063):", airspace.find_navpoint_by_number(6063))
print("Find by name ('LAMPA'):", airspace.find_navpoint_by_name("LAMPA"))
print("Find airport ('LEIB'):", airspace.find_airport_by_name("LEIB"))