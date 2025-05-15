import tkinter as tk
from tkinter import filedialog, messagebox
from graph import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from airSpace import AirSpace, LoadAirspaceFromFiles
from navPoint import HaversineDistance

from project.node import Distance


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Explorer - Version 1")
        self.current_graph = None
        self.current_airspace = None

        # Frame principal
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para controles
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Frame para el gráfico
        self.graph_frame = tk.Frame(self.main_frame)
        self.graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Botones
        tk.Button(self.control_frame, text="Show Example Graph 1",
                  command=self.show_example_graph1).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Show Example Graph 2",
                  command=self.show_example_graph2).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Load Graph from File",
                  command=self.load_graph_from_file).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Show Node Neighbors",
                  command=self.show_node_neighbors).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Add Node",
                  command=self.add_node_dialog).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Add Segment",
                  command=self.add_segment_dialog).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Delete Node",
                  command=self.delete_node_dialog).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Create New Graph",
                  command=self.create_new_graph).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Save Graph to File",
                  command=self.save_graph_to_file).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Find Shortest Path",
                  command=self.show_shortest_path).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Load Catalunya Airspace",
                  command=self.load_catalunya_airspace).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Load Spain Airspace",
                  command=self.load_spain_airspace).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Load Europe Airspace",
                  command=self.load_europe_airspace).pack(fill=tk.X, pady=2)



        # Área para mostrar el gráfico
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Estado inicial
        self.clear_graph_display()

    def load_catalunya_airspace(self):
        self.current_airspace = AirSpace()
        try:
            LoadAirspaceFromFiles(self.current_airspace, "Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
            self.plot_airspace()
            messagebox.showinfo("Success", "Catalunya airspace loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load airspace: {str(e)}")

    def load_spain_airspace(self):
        self.current_airspace = AirSpace()
        try:
            LoadAirspaceFromFiles(self.current_airspace, "Esp_nav.txt", "Esp_seg.txt", "Esp_aer.txt")
            self.plot_airspace()
            messagebox.showinfo("Success", "Spain airspace loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load airspace: {str(e)}")

    def load_europe_airspace(self):
        self.current_airspace = AirSpace()
        try:
            LoadAirspaceFromFiles(self.current_airspace, "Eur_nav.txt", "Eur_seg.txt", "Eur_aer.txt")
            self.plot_airspace()
            messagebox.showinfo("Success", "Europe airspace loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load airspace: {str(e)}")

    def plot_airspace(self):
        if not self.current_airspace:
            return

        self.ax.clear()

        # Configuración del fondo y estilo
        self.ax.set_facecolor('#F0F8FF')  # Azul claro muy tenue
        self.figure.patch.set_facecolor('white')

        # Dibujar segmentos primero (en azul aeronáutico)
        for seg in self.current_airspace.nav_segments:
            origin = self.current_airspace.find_navpoint_by_number(seg.origin_number)
            destination = self.current_airspace.find_navpoint_by_number(seg.destination_number)

            if origin and destination:
                self.ax.plot([origin.longitude, destination.longitude],
                             [origin.latitude, destination.latitude],
                             color='#1E90FF', linewidth=0.8, alpha=0.7)

        # Dibujar puntos de navegación (en verde aeronáutico)
        for point in self.current_airspace.nav_points:
            self.ax.plot(point.longitude, point.latitude, 'o',
                         markersize=5,
                         markerfacecolor='#32CD32',
                         markeredgecolor='#006400',
                         markeredgewidth=0.5)

            # Mostrar nombre del punto (solo si hay espacio)
            text_offset = 0.02  # Ajuste para evitar solapamiento
            self.ax.text(point.longitude + text_offset,
                         point.latitude + text_offset,
                         point.name,
                         fontsize=7,
                         color='#006400',
                         bbox=dict(facecolor='white',
                                   edgecolor='none',
                                   alpha=0.7,
                                   boxstyle='round,pad=0.2'))

        # Dibujar aeropuertos (iconos especiales)
        airport_icon = dict(marker='*', markersize=10, color='#FF4500')
        for airport in self.current_airspace.nav_airports:
            if airport.sids:
                first_sid = self.current_airspace.find_navpoint_by_number(airport.sids[0])
                if first_sid:
                    self.ax.plot(first_sid.longitude, first_sid.latitude,
                                 **airport_icon)
                    self.ax.text(first_sid.longitude,
                                 first_sid.latitude + 0.05,  # Offset vertical
                                 airport.name,
                                 fontsize=8,
                                 ha='center',
                                 color='#8B0000',
                                 fontweight='bold',
                                 bbox=dict(facecolor='white',
                                           edgecolor='#FF4500',
                                           alpha=0.8))

        # Ajustes finales
        self.ax.grid(True, linestyle=':', color='gray', alpha=0.4)
        self.ax.set_title("Catalunya Airspace (Barcelona FIR)",
                          fontsize=12,
                          pad=15,
                          fontweight='bold')

        self.canvas.draw()

    def clear_graph_display(self):
        self.ax.clear()
        self.ax.set_title("No graph loaded")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def show_example_graph1(self):
        self.current_graph = CreateGraph_1()
        self.plot_current_graph()

    def show_example_graph2(self):
        self.current_graph = CreateGraph_2()
        self.plot_current_graph()

    def load_graph_from_file(self):
        filename = filedialog.askopenfilename(title="Select Graph File",
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            self.current_graph = LoadGraphFromFile(filename)
            if self.current_graph:
                self.plot_current_graph()
            else:
                messagebox.showerror("Error", "Failed to load graph from file")

    def show_node_neighbors(self):
        if not self.current_graph:
            messagebox.showwarning("Warning", "No graph loaded")
            return

        node_name = tk.simpledialog.askstring("Node Neighbors", "Enter node name:")
        if node_name:
            if not PlotNode(self.current_graph, node_name):
                messagebox.showerror("Error", f"Node '{node_name}' not found in graph")

    def show_shortest_path(self):
        if not self.current_graph or len(self.current_graph.nodes) < 2:
            messagebox.showwarning("Warning", "Not enough nodes in graph")
            return

        origin = tk.simpledialog.askstring("Shortest Path", "Enter origin node name:")
        if not origin:
            return

        destination = tk.simpledialog.askstring("Shortest Path", "Enter destination node name:")
        if not destination:
            return

        path = FindShortestPath(self.current_graph, origin, destination)
        if path:
            messagebox.showinfo("Shortest Path",
                                f"Path found with cost {path.cost:.1f}:\n{' -> '.join([node.name for node in path.nodes])}")
            self.plot_path(path)
        else:
            messagebox.showinfo("Shortest Path", "No path exists between these nodes")

    def plot_path(self, path):
        self.ax.clear()

        # Dibujar todos los segmentos en gris primero
        for seg in self.current_graph.segments:
            self.ax.plot([seg.origin.x, seg.destination.x],
                         [seg.origin.y, seg.destination.y],
                         'gray', linewidth=1, alpha=0.3)

        # Resaltar segmentos del camino más corto
        for i in range(len(path.nodes) - 1):
            origin = path.nodes[i]
            destination = path.nodes[i + 1]
            self.ax.plot([origin.x, destination.x],
                         [origin.y, destination.y],
                         'r-', linewidth=2)
            # Mostrar costo en rojo
            mid_x = (origin.x + destination.x) / 2
            mid_y = (origin.y + destination.y) / 2
            self.ax.text(mid_x, mid_y, f"{Distance(origin, destination):.1f}",
                         fontsize=8, ha='center', va='center', color='red',
                         bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        # Dibujar nodos
        for node in self.current_graph.nodes:
            if node in path.nodes:
                color = 'blue' if node == path.nodes[0] or node == path.nodes[-1] else 'green'
            else:
                color = 'gray'

            self.ax.plot(node.x, node.y, 'o', markersize=10, color=color)
            self.ax.text(node.x, node.y, node.name,
                         fontsize=12, ha='center', va='center', color='white')

        self.ax.grid(True)
        self.ax.set_title(f"Shortest Path from {path.nodes[0].name} to {path.nodes[-1].name}")
        self.canvas.draw()

    def plot_current_graph(self):
        if not self.current_graph:
            return

        self.ax.clear()

        # Configurar fondo y estilo general
        self.ax.set_facecolor('#F5F5F5')
        self.figure.patch.set_facecolor('white')

        # Dibujar segmentos
        for seg in self.current_graph.segments:
            self.ax.plot([seg.origin.x, seg.destination.x],
                         [seg.origin.y, seg.destination.y],
                         color='#4682B4', linewidth=1.5, alpha=0.7)

            # Mostrar costo
            mid_x = (seg.origin.x + seg.destination.x) / 2
            mid_y = (seg.origin.y + seg.destination.y) / 2
            self.ax.text(mid_x, mid_y, f"{seg.cost:.1f}",
                         fontsize=8, ha='center', va='center',
                         bbox=dict(facecolor='white', edgecolor='#4682B4', alpha=0.9))

        # Dibujar nodos
        for node in self.current_graph.nodes:
            self.ax.plot(node.x, node.y, 'o', markersize=12,
                         markerfacecolor='#FF6B6B', markeredgecolor='#333333', markeredgewidth=1)
            self.ax.text(node.x, node.y, node.name,
                         fontsize=10, ha='center', va='center', color='white', fontweight='bold')

        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.ax.set_title("Graph Visualization", fontsize=12, pad=15)
        self.canvas.draw()

    def add_node_dialog(self):
        if not self.current_graph:
            messagebox.showwarning("Warning", "No graph loaded. Creating new graph.")
            self.current_graph = Graph()

        name = tk.simpledialog.askstring("Add Node", "Enter node name:")
        if name:
            # Verificar si el nodo ya existe
            for node in self.current_graph.nodes:
                if node.name == name:
                    messagebox.showerror("Error", f"Node '{name}' already exists")
                    return

            x = tk.simpledialog.askfloat("Add Node", "Enter X coordinate:")
            y = tk.simpledialog.askfloat("Add Node", "Enter Y coordinate:")

            if x is not None and y is not None:
                AddNode(self.current_graph, Node(name, x, y))
                self.plot_current_graph()

    def add_segment_dialog(self):
        if not self.current_graph or len(self.current_graph.nodes) < 2:
            messagebox.showwarning("Warning", "Not enough nodes in graph")
            return

        origin = tk.simpledialog.askstring("Add Segment", "Enter origin node name:")
        if not origin:
            return

        destination = tk.simpledialog.askstring("Add Segment", "Enter destination node name:")
        if not destination:
            return

        # Verificar que los nodos existen
        origin_exists = any(node.name == origin for node in self.current_graph.nodes)
        destination_exists = any(node.name == destination for node in self.current_graph.nodes)

        if not origin_exists or not destination_exists:
            messagebox.showerror("Error", "One or both nodes not found in graph")
            return

        segment_name = f"{origin}{destination}"
        if AddSegment(self.current_graph, segment_name, origin, destination):
            self.plot_current_graph()
        else:
            messagebox.showerror("Error", "Failed to add segment")

    def delete_node_dialog(self):
        if not self.current_graph or not self.current_graph.nodes:
            messagebox.showwarning("Warning", "No nodes in graph")
            return

        node_name = tk.simpledialog.askstring("Delete Node", "Enter node name to delete:")
        if not node_name:
            return

        # Buscar y eliminar el nodo
        node_to_delete = None
        for node in self.current_graph.nodes:
            if node.name == node_name:
                node_to_delete = node
                break

        if not node_to_delete:
            messagebox.showerror("Error", f"Node '{node_name}' not found")
            return

        # Eliminar segmentos relacionados
        segments_to_keep = []
        for seg in self.current_graph.segments:
            if seg.origin != node_to_delete and seg.destination != node_to_delete:
                segments_to_keep.append(seg)

        self.current_graph.segments = segments_to_keep

        # Eliminar el nodo
        self.current_graph.nodes.remove(node_to_delete)

        # Actualizar listas de vecinos en otros nodos
        for node in self.current_graph.nodes:
            if node_to_delete in node.neighbors:
                node.neighbors.remove(node_to_delete)

        self.plot_current_graph()
        messagebox.showinfo("Success", f"Node '{node_name}' and related segments deleted")

    def create_new_graph(self):
        self.current_graph = Graph()
        self.plot_current_graph()
        messagebox.showinfo("Info", "New empty graph created")

    def save_graph_to_file(self):
        if not self.current_graph or not self.current_graph.nodes:
            messagebox.showwarning("Warning", "No graph to save")
            return

        filename = filedialog.asksaveasfilename(title="Save Graph",
                                                defaultextension=".txt",
                                                filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            if SaveGraphToFile(self.current_graph, filename):
                messagebox.showinfo("Success", "Graph saved successfully")
            else:
                messagebox.showerror("Error", "Failed to save graph")

    # En la clase GraphApp, modificar los siguientes métodos:

    def show_node_neighbors(self):
        if self.current_airspace:
            self.show_airspace_node_neighbors()
        elif self.current_graph:
            self.show_graph_node_neighbors()
        else:
            messagebox.showwarning("Warning", "No graph or airspace loaded")

    def show_graph_node_neighbors(self):
        node_name = tk.simpledialog.askstring("Node Neighbors", "Enter node name:")
        if node_name:
            if not PlotNode(self.current_graph, node_name):
                messagebox.showerror("Error", f"Node '{node_name}' not found in graph")

    def show_airspace_node_neighbors(self):
        node_name = tk.simpledialog.askstring("Node Neighbors", "Enter node name:")
        if node_name:
            node = self.current_airspace.find_navpoint_by_name(node_name)
            if node:
                self.plot_airspace_node_neighbors(node)
            else:
                messagebox.showerror("Error", f"Node '{node_name}' not found in airspace")

    def plot_airspace_node_neighbors(self, node):
        self.ax.clear()

        # Configuración del gráfico
        self.ax.set_facecolor('#F0F8FF')
        self.figure.patch.set_facecolor('white')

        # Dibujar todos los puntos y segmentos primero (en gris)
        for point in self.current_airspace.nav_points:
            self.ax.plot(point.longitude, point.latitude, 'o',
                         markersize=3, color='gray', alpha=0.5)

        for seg in self.current_airspace.nav_segments:
            origin = self.current_airspace.find_navpoint_by_number(seg.origin_number)
            destination = self.current_airspace.find_navpoint_by_number(seg.destination_number)
            if origin and destination:
                self.ax.plot([origin.longitude, destination.longitude],
                             [origin.latitude, destination.latitude],
                             'gray', linewidth=0.5, alpha=0.3)

        # Resaltar el nodo seleccionado y sus vecinos
        self.ax.plot(node.longitude, node.latitude, 'bo', markersize=8)
        self.ax.text(node.longitude, node.latitude, node.name,
                     fontsize=10, ha='center', va='center', color='white')

        # Dibujar vecinos
        for neighbor in node.neighbors:
            self.ax.plot(neighbor.longitude, neighbor.latitude, 'go', markersize=6)
            self.ax.text(neighbor.longitude, neighbor.latitude, neighbor.name,
                         fontsize=8, ha='center', va='center', color='black')

            # Dibujar conexión
            self.ax.plot([node.longitude, neighbor.longitude],
                         [node.latitude, neighbor.latitude],
                         'b-', linewidth=1)

            # Mostrar distancia
            seg = None
            for s in self.current_airspace.nav_segments:
                if (s.origin_number == node.number and
                        s.destination_number == neighbor.number):
                    seg = s
                    break

            if seg:
                mid_x = (node.longitude + neighbor.longitude) / 2
                mid_y = (node.latitude + neighbor.latitude) / 2
                self.ax.text(mid_x, mid_y, f"{seg.distance:.1f}",
                             fontsize=8, ha='center', va='center', color='red',
                             bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        self.ax.grid(True, linestyle=':', color='gray', alpha=0.4)
        self.ax.set_title(f"Neighbors of {node.name} in Catalunya Airspace",
                          fontsize=12, pad=15)
        self.canvas.draw()

    def show_shortest_path(self):
        if self.current_airspace:
            self.show_airspace_shortest_path()
        elif self.current_graph:
            self.show_graph_shortest_path()
        else:
            messagebox.showwarning("Warning", "No graph or airspace loaded")

    def show_airspace_shortest_path(self):
        origin_name = tk.simpledialog.askstring("Shortest Path", "Enter origin node name:")
        if not origin_name:
            return

        destination_name = tk.simpledialog.askstring("Shortest Path", "Enter destination node name:")
        if not destination_name:
            return

        path = FindShortestPathInAirspace(self.current_airspace, origin_name, destination_name)
        if path:
            messagebox.showinfo("Shortest Path",
                                f"Path found with cost {path.cost:.1f}:\n{' -> '.join([node.name for node in path.nodes])}")
            self.plot_airspace_path(path)
        else:
            messagebox.showinfo("Shortest Path", "No path exists between these nodes")

    def plot_airspace_path(self, path):
        self.ax.clear()

        # Configuración del gráfico
        self.ax.set_facecolor('#F0F8FF')
        self.figure.patch.set_facecolor('white')

        # Dibujar todos los puntos y segmentos primero (en gris)
        for point in self.current_airspace.nav_points:
            self.ax.plot(point.longitude, point.latitude, 'o',
                         markersize=3, color='gray', alpha=0.5)

        for seg in self.current_airspace.nav_segments:
            origin = self.current_airspace.find_navpoint_by_number(seg.origin_number)
            destination = self.current_airspace.find_navpoint_by_number(seg.destination_number)
            if origin and destination:
                self.ax.plot([origin.longitude, destination.longitude],
                             [origin.latitude, destination.latitude],
                             'gray', linewidth=0.5, alpha=0.3)

        # Dibujar el camino en rojo
        for i in range(len(path.nodes) - 1):
            origin = path.nodes[i]
            destination = path.nodes[i + 1]

            self.ax.plot([origin.longitude, destination.longitude],
                         [origin.latitude, destination.latitude],
                         'r-', linewidth=2)

            # Mostrar distancia
            seg = None
            for s in self.current_airspace.nav_segments:
                if (s.origin_number == origin.number and
                        s.destination_number == destination.number):
                    seg = s
                    break

            if seg:
                mid_x = (origin.longitude + destination.longitude) / 2
                mid_y = (origin.latitude + destination.latitude) / 2
                self.ax.text(mid_x, mid_y, f"{seg.distance:.1f}",
                             fontsize=8, ha='center', va='center', color='red',
                             bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

        # Dibujar nodos
        for node in self.current_airspace.nav_points:
            if node in path.nodes:
                color = 'blue' if node == path.nodes[0] or node == path.nodes[-1] else 'green'
                self.ax.plot(node.longitude, node.latitude, 'o',
                             markersize=8, color=color)
                self.ax.text(node.longitude, node.latitude, node.name,
                             fontsize=10, ha='center', va='center', color='white')
            else:
                self.ax.plot(node.longitude, node.latitude, 'o',
                             markersize=3, color='gray', alpha=0.5)

        self.ax.grid(True, linestyle=':', color='gray', alpha=0.4)
        self.ax.set_title(f"Shortest Path from {path.nodes[0].name} to {path.nodes[-1].name}",
                          fontsize=12, pad=15)
        self.canvas.draw()



def show_shortest_path(self):
    if not self.current_graph or len(self.current_graph.nodes) < 2:
        messagebox.showwarning("Warning", "Not enough nodes in graph")
        return

    origin = tk.simpledialog.askstring("Shortest Path", "Enter origin node name:")
    if not origin:
        return

    destination = tk.simpledialog.askstring("Shortest Path", "Enter destination node name:")
    if not destination:
        return

    path = FindShortestPath(self.current_graph, origin, destination)
    if path:
        messagebox.showinfo("Shortest Path", f"Path found with cost {path.cost:.1f}:\n{' -> '.join([node.name for node in path.nodes])}")
        self.plot_path(path)
    else:
        messagebox.showinfo("Shortest Path", "No path exists between these nodes")

def plot_path(self, path):
    self.ax.clear()

    # Dibujar todos los segmentos en gris primero
    for seg in self.current_graph.segments:
        self.ax.plot([seg.origin.x, seg.destination.x],
                     [seg.origin.y, seg.destination.y],
                     'gray', linewidth=1, alpha=0.3)

    # Resaltar segmentos del camino más corto
    for i in range(len(path.nodes)-1):
        origin = path.nodes[i]
        destination = path.nodes[i+1]
        self.ax.plot([origin.x, destination.x],
                     [origin.y, destination.y],
                     'r-', linewidth=2)
        # Mostrar costo en rojo
        mid_x = (origin.x + destination.x) / 2
        mid_y = (origin.y + destination.y) / 2
        self.ax.text(mid_x, mid_y, f"{Distance(origin, destination):.1f}",
                     fontsize=8, ha='center', va='center', color='green',
                     bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Dibujar nodos
    for node in self.current_graph.nodes:
        if node in path.nodes:
            color = 'blue' if node == path.nodes[0] or node == path.nodes[-1] else 'green'
        else:
            color = 'gray'

        self.ax.plot(node.x, node.y, 'o', markersize=10, color=color)
        self.ax.text(node.x, node.y, node.name,
                     fontsize=12, ha='center', va='center', color='white')

    self.ax.grid(True)
    self.ax.set_title(f"Shortest Path from {path.nodes[0].name} to {path.nodes[-1].name}")
    self.canvas.draw()

from path import *

def FindShortestPath(g, origin_name, destination_name):
    # Encontrar nodos de origen y destino
    origin = None
    destination = None
    for node in g.nodes:
        if node.name == origin_name:
            origin = node
        if node.name == destination_name:
            destination = node

    if origin is None or destination is None:
        return None

    # Implementación del algoritmo A*
    open_paths = [Path([origin], 0)]
    visited = set()

    while open_paths:
        # Encontrar el camino con el menor costo estimado
        current_path = min(open_paths, key=lambda p: p.cost + Distance(p.nodes[-1], destination))
        open_paths.remove(current_path)
        last_node = current_path.nodes[-1]

        # Si hemos llegado al destino
        if last_node == destination:
            return current_path

        # Marcar el nodo como visitado
        if last_node in visited:
            continue
        visited.add(last_node)

        # Expandir a los vecinos
        for neighbor in last_node.neighbors:
            if neighbor not in visited:
                # Encontrar el segmento correspondiente
                segment = None
                for seg in g.segments:
                    if seg.origin == last_node and seg.destination == neighbor:
                        segment = seg
                        break

                if segment:
                    new_path = AddNodeToPath(current_path, neighbor, segment.cost)
                    open_paths.append(new_path)

    return None  # No se encontró camino

def FindShortestPathInAirspace(airspace, origin_name, destination_name):
    # Encontrar nodos de origen y destino
    origin = airspace.find_navpoint_by_name(origin_name)
    destination = airspace.find_navpoint_by_name(destination_name)

    if origin is None or destination is None:
        return None

    # Implementación del algoritmo A*
    open_paths = [Path([origin], 0)]
    visited = set()

    while open_paths:
        # Encontrar el camino con el menor costo estimado
        current_path = min(open_paths, key=lambda p: p.cost + HaversineDistance(p.nodes[-1], destination))
        open_paths.remove(current_path)
        last_node = current_path.nodes[-1]

        # Si hemos llegado al destino
        if last_node == destination:
            return current_path

        # Marcar el nodo como visitado
        if last_node in visited:
            continue
        visited.add(last_node)

        # Expandir a los vecinos
        for neighbor in last_node.neighbors:
            if neighbor not in visited:
                # Encontrar el segmento correspondiente
                segment = None
                for seg in airspace.nav_segments:
                    if (seg.origin_number == last_node.number and
                        seg.destination_number == neighbor.number):
                        segment = seg
                        break

                if segment:
                    new_path = AddNodeToPath(current_path, neighbor, segment.distance)
                    open_paths.append(new_path)

    return None  # No se encontró camino



if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.geometry("900x600")
    root.mainloop()
