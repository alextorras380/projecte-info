from navPoint import NavPoint
from navSegment import NavSegment

# Crear puntos de navegación
n1 = NavPoint(1, "PuntoA", 41.3879, 2.16992)
n2 = NavPoint(2, "PuntoB", 40.4168, -3.7038)

# Crear segmento
seg = NavSegment(1, 2, 500.0)

print("=== Testing NavSegment ===")
print(seg)