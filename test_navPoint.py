from navPoint import NavPoint, AddNavNeighbor, HaversineDistance

# Crear puntos de navegación de prueba
n1 = NavPoint(1, "PuntoA", 41.3879, 2.16992)  # Barcelona
n2 = NavPoint(2, "PuntoB", 40.4168, -3.7038)  # Madrid

print("=== Testing NavPoint class ===")
print(n1)
print(n2)

print("\n=== Testing AddNavNeighbor ===")
print(AddNavNeighbor(n1, n2))  # True
print(AddNavNeighbor(n1, n2))  # False (ya es vecino)

print("\n=== Testing HaversineDistance ===")
print(f"Distance: {HaversineDistance(n1, n2):.2f} km")