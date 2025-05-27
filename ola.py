F=open("Esp_seg.txt", "r")
G=open("Esp_seg.txt", "w")
for line in F:
    parts = line.strip().split()
    if len(parts) == 3:
        id_, name, lat = parts
        G.write(f"{id_},{name},{lat}\n")