import tkinter as tk
from tkinter import filedialog, messagebox
from graph import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from airSpace import AirSpace, LoadAirspaceFromFiles
from navPoint import HaversineDistance
from node import Distance
import os
import platform
import subprocess
import time
import random


def obrir_google_earth(kml_path):
    try:
        if platform.system() == 'Windows':
            os.startfile(kml_path)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.call(['open', kml_path])
        elif platform.system() == 'Linux':
            subprocess.call(['xdg-open', kml_path])
    except Exception as e:
        print(f"Error obrint Google Earth: {e}")

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Explorer - Version 1")
        self.current_graph = None
        self.current_airspace = None

        self.restricted_nodes = set()  # Para nodos restringidos (por nombre o número)
        self.restricted_segments = set()  # Para segmentos restringidos (formato "origen-destino")

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

        tk.Button(self.control_frame, text="Generate KML for Airspace",
                  command=self.generate_airspace_kml).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Generate KML for Path",
                  command=self.generate_path_kml).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Add Restrictions",
                  command=self.add_restrictions_dialog).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Compare Algorithms",
                  command=self.compare_algorithms).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Open image", command=self.open_specific_image).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Party mode 🎉", command=self.modo_festa).pack(fill=tk.X, pady=2)
        tk.Button(self.control_frame, text="Snake Path 🐍", command=self.run_snake_path_animation).pack(fill=tk.X,
                                                                                                       pady=2)
        tk.Button(self.control_frame, text="Snake Path (Airspace) 🐍", command=self.run_airspace_snake_path).pack(
            fill=tk.X, pady=2)



        # Área para mostrar el gráfico
        self.figure, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Estado inicial
        self.clear_graph_display()

        self.add_version4_features()

        self.zoom_frame = None  # Contenidor per als botons de zoom

    def add_version4_features(self):
        # Menú superior
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exportar KML", command=self.export_to_kml)
        menubar.add_cascade(label="Herramientas", menu=file_menu)
        self.root.config(menu=menubar)

        # Panel de estado
        self.status_bar = tk.Label(self.root, text="Versión 4 - Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def export_to_kml(self):
        if not self.current_graph:
            messagebox.showerror("Error", "No hay grafo para exportar")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".kml")
        if filename:
            # Implementar lógica de exportación (ejemplo simplificado)
            with open(filename, 'w') as f:
                f.write(
                    '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n')
                for node in self.current_graph.nodes:
                    f.write(
                        f'<Placemark><name>{node.name}</name><Point><coordinates>{node.x},{node.y},0</coordinates></Point></Placemark>\n')
                f.write('</Document>\n</kml>')
            self.status_bar.config(text=f"KML exportado a {filename}")

    def load_catalunya_airspace(self):
        self.current_airspace = AirSpace()
        try:
            LoadAirspaceFromFiles(self.current_airspace, "Cat_nav.txt", "Cat_seg.txt", "Cat_aer.txt")
            self.plot_airspace("Catalunya Airspace (Barcelona FIR)")

            messagebox.showinfo("Success", "Catalunya airspace loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load airspace: {str(e)}")

    def load_europe_airspace(self):
        self.current_airspace = AirSpace()
        try:
            # Verificar que los archivos existen antes de intentar cargarlos
            required_files = ["Eur_nav.txt", "Eur_seg.txt", "Eur_aer.txt"]
            for file in required_files:
                if not os.path.exists(file):
                    raise FileNotFoundError(f"El archivo {file} no se encuentra en el directorio actual")

            LoadAirspaceFromFiles(self.current_airspace, "Eur_nav.txt", "Eur_seg.txt", "Eur_aer.txt")
            self.plot_airspace("European Airspace")

            messagebox.showinfo("Success", "Europe airspace loaded successfully")
        except FileNotFoundError as e:
            messagebox.showerror("Error",
                                 f"No se encontraron los archivos necesarios: {str(e)}\n\nAsegúrate de que los archivos Eur_nav.txt, Eur_seg.txt y Eur_aer.txt estén en el mismo directorio que el programa.")
        except IndexError as e:
            messagebox.showerror("Error",
                                 f"Error en el formato de los archivos: {str(e)}\n\nAlguna línea en los archivos no tiene el formato esperado.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load airspace: {str(e)}")

    def load_spain_airspace(self):
        self.current_airspace = AirSpace()
        try:
            # Verificar que los archivos existen antes de intentar cargarlos
            required_files = ["Esp_nav.txt", "Esp_seg.txt", "Esp_aer.txt"]
            for file in required_files:
                if not os.path.exists(file):
                    raise FileNotFoundError(f"El archivo {file} no se encuentra en el directorio actual")

            LoadAirspaceFromFiles(self.current_airspace, "Esp_nav.txt", "Esp_seg.txt", "Esp_aer.txt")
            self.plot_airspace("Spain Airspace (Madrid FIR)")

            messagebox.showinfo("Success", "Spain airspace loaded successfully")
        except FileNotFoundError as e:
            messagebox.showerror("Error",
                                 f"No se encontraron los archivos necesarios: {str(e)}\n\nAsegúrate de que los archivos Esp_nav.txt, Esp_seg.txt y Esp_aer.txt estén en el mismo directorio que el programa.")
        except IndexError as e:
            messagebox.showerror("Error",
                                 f"Error en el formato de los archivos: {str(e)}\n\nAlguna línea en los archivos no tiene el formato esperado.")
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

    def plot_airspace(self, title="Airspace"):
        if not self.current_airspace:
            return

        self.ax.clear()

        # Configuración del fondo y estilo
        self.ax.set_facecolor('#F0F8FF')  # Azul claro muy tenue
        self.figure.patch.set_facecolor('white')

        # Ajustar márgenes para mejor visualización
        self.figure.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)

        # Dibujar segmentos primero (en azul aeronáutico con transparencia)
        for seg in self.current_airspace.nav_segments:
            origin = self.current_airspace.find_navpoint_by_number(seg.origin_number)
            destination = self.current_airspace.find_navpoint_by_number(seg.destination_number)

            if origin and destination:
                self.ax.plot([origin.longitude, destination.longitude],
                             [origin.latitude, destination.latitude],
                             color='#1E90FF', linewidth=0.8, alpha=0.5)

        # Dibujar puntos de navegación (tamaño según importancia)
        for point in self.current_airspace.nav_points:
            # Determinar tamaño según si es punto importante (con muchos vecinos)
            size = 8 if len(point.neighbors) < 3 else 12 if len(point.neighbors) < 5 else 16

            self.ax.plot(point.longitude, point.latitude, 'o',
                         markersize=size,
                         markerfacecolor='#32CD32',
                         markeredgecolor='#006400',
                         markeredgewidth=0.5,
                         picker=5)  # Permite selección con ratón

            # Mostrar nombre solo de puntos importantes para evitar saturación
            if len(point.neighbors) > 0:
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

        # Dibujar aeropuertos (iconos especiales más grandes)
        airport_icon = dict(marker='*', markersize=15, color='#FF4500', linestyle='none')
        for airport in self.current_airspace.nav_airports:
            if airport.sids:
                first_sid = self.current_airspace.find_navpoint_by_number(airport.sids[0])
                if first_sid:
                    self.ax.plot(first_sid.longitude, first_sid.latitude,
                                 **airport_icon)
                    self.ax.text(first_sid.longitude,
                                 first_sid.latitude + 0.05,  # Offset vertical
                                 airport.name,
                                 fontsize=9,
                                 ha='center',
                                 color='#8B0000',
                                 fontweight='bold',
                                 bbox=dict(facecolor='white',
                                           edgecolor='#FF4500',
                                           alpha=0.8))

        # Ajustes finales
        self.ax.grid(True, linestyle=':', color='gray', alpha=0.4)
        self.ax.set_title(title, fontsize=12, pad=15, fontweight='bold')


        # Configurar eventos para zoom y selección
        self.setup_interaction()

        self.canvas.draw()

    def setup_interaction(self):
        # Conectar eventos
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('pick_event', self.on_pick)

        # Añadir botones de zoom
        zoom_frame = tk.Frame(self.control_frame)
        zoom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        tk.Button(zoom_frame, text="Zoom In", command=lambda: self.zoom(1.2)).pack(side=tk.LEFT, expand=True)
        tk.Button(zoom_frame, text="Zoom Out", command=lambda: self.zoom(0.8)).pack(side=tk.LEFT, expand=True)
        tk.Button(zoom_frame, text="Reset View", command=self.reset_view).pack(side=tk.LEFT, expand=True)

        # Guardar límites iniciales
        self.initial_xlim = self.ax.get_xlim()
        self.initial_ylim = self.ax.get_ylim()

    def zoom(self, factor):
        # Obtener límites actuales
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        # Calcular nuevos límites
        x_center = (xlim[0] + xlim[1]) / 2
        y_center = (ylim[0] + ylim[1]) / 2
        x_width = (xlim[1] - xlim[0]) * factor
        y_height = (ylim[1] - ylim[0]) * factor

        # Aplicar zoom manteniendo el centro
        self.ax.set_xlim(x_center - x_width / 2, x_center + x_width / 2)
        self.ax.set_ylim(y_center - y_height / 2, y_center + y_height / 2)

        self.canvas.draw()

    def reset_view(self):
        self.ax.set_xlim(self.initial_xlim)
        self.ax.set_ylim(self.initial_ylim)
        self.canvas.draw()

    def on_scroll(self, event):
        # Zoom con rueda del ratón
        if event.inaxes == self.ax:
            factor = 1.2 if event.button == 'up' else 0.8
            self.zoom(factor)

    def on_pick(self, event):
        # Selección de nodo con clic
        if isinstance(event.artist, plt.Line2D):
            point = event.artist
            x, y = point.get_xdata()[0], point.get_ydata()[0]

            # Buscar el punto de navegación correspondiente
            for nav_point in self.current_airspace.nav_points:
                if (abs(nav_point.longitude - x) < 0.01 and
                        abs(nav_point.latitude - y) < 0.01):

                    # Mostrar información en un tooltip
                    tooltip = f"NavPoint: {nav_point.name}\n"
                    tooltip += f"Coordinates: {nav_point.latitude:.4f}°, {nav_point.longitude:.4f}°\n"
                    tooltip += f"Neighbors: {len(nav_point.neighbors)}"

                    # Crear anotación
                    if hasattr(self, 'current_tooltip'):
                        self.current_tooltip.remove()

                    self.current_tooltip = self.ax.annotate(
                        tooltip,
                        xy=(x, y),
                        xytext=(10, 10),
                        textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.9),
                        arrowprops=dict(arrowstyle='->')
                    )

                    self.canvas.draw()
                    break

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
            if self.current_airspace:
                self.convert_airspace_to_graph()
            else:
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
        # Si no hi ha graf actual però sí espai aeri, el convertim
        if not self.current_graph:
            if self.current_airspace:
                self.convert_airspace_to_graph()
            else:
                messagebox.showwarning("Warning", "No nodes in graph")
                return

        if not self.current_graph.nodes:
            messagebox.showwarning("Warning", "No nodes in graph")
            return

        node_name = tk.simpledialog.askstring("Delete Node", "Enter node name to delete:")
        if not node_name:
            return

        # Buscar i eliminar el node
        node_to_delete = None
        for node in self.current_graph.nodes:
            if node.name == node_name:
                node_to_delete = node
                break

        if not node_to_delete:
            messagebox.showerror("Error", f"Node '{node_name}' not found")
            return

        # Eliminar segments relacionats
        self.current_graph.segments = [
            seg for seg in self.current_graph.segments
            if seg.origin != node_to_delete and seg.destination != node_to_delete
        ]

        # Eliminar el node
        self.current_graph.nodes.remove(node_to_delete)

        # Treure'l dels veïns
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

    def generate_airspace_kml(self):
        if not self.current_airspace:
            messagebox.showwarning("Warning", "No airspace loaded")
            return

        filename = filedialog.asksaveasfilename(
            title="Save KML File",
            defaultextension=".kml",
            filetypes=(("KML files", "*.kml"), ("All files", "*.*")))

        if filename:
            try:
                self.create_airspace_kml(filename)
                messagebox.showinfo("Success", f"KML file saved successfully: {filename}")
                obrir_google_earth(filename)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate KML: {str(e)}")

    def create_airspace_kml(self, filename):
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>Airspace Visualization</name>
        <description>Generated by Graph Explorer</description>
    """

        # Add airports
        for airport in self.current_airspace.nav_airports:
            if airport.sids:
                first_sid = self.current_airspace.find_navpoint_by_number(airport.sids[0])
                if first_sid:
                    kml_content += f"""
        <Placemark>
            <name>{airport.name}</name>
            <description>Airport</description>
            <styleUrl>#airportStyle</styleUrl>
            <Point>
                <coordinates>{first_sid.longitude},{first_sid.latitude},0</coordinates>
            </Point>
        </Placemark>
    """

        # Add navigation points
        for point in self.current_airspace.nav_points:
            is_restricted = point.name in self.restricted_nodes or point.number in self.restricted_nodes
            style = "restrictedStyle" if is_restricted else "navpointStyle"

            kml_content += f"""
        <Placemark>
            <name>{point.name}</name>
            <description>NavPoint: {point.name}</description>
            <styleUrl>#{style}</styleUrl>
            <Point>
                <coordinates>{point.longitude},{point.latitude},0</coordinates>
            </Point>
        </Placemark>
    """

        # Add segments
        for seg in self.current_airspace.nav_segments:
            origin = self.current_airspace.find_navpoint_by_number(seg.origin_number)
            destination = self.current_airspace.find_navpoint_by_number(seg.destination_number)

            if origin and destination:
                is_restricted = (f"{origin.name}-{destination.name}" in self.restricted_segments or
                                 f"{origin.number}-{destination.number}" in self.restricted_segments)
                style = "restrictedSegmentStyle" if is_restricted else "segmentStyle"

                kml_content += f"""
        <Placemark>
            <name>{origin.name} to {destination.name}</name>
            <description>Distance: {seg.distance:.2f} km</description>
            <styleUrl>#{style}</styleUrl>
            <LineString>
                <coordinates>
                    {origin.longitude},{origin.latitude},0
                    {destination.longitude},{destination.latitude},0
                </coordinates>
            </LineString>
        </Placemark>
    """

        # Add styles
        kml_content += """
        <Style id="airportStyle">
            <IconStyle>
                <color>ff00aaff</color>
                <scale>1.5</scale>
                <Icon>
                    <href>http://maps.google.com/mapfiles/kml/shapes/airports.png</href>
                </Icon>
            </IconStyle>
        </Style>
        <Style id="navpointStyle">
            <IconStyle>
                <color>ff00ff00</color>
                <scale>0.7</scale>
                <Icon>
                    <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
                </Icon>
            </IconStyle>
        </Style>
        <Style id="segmentStyle">
            <LineStyle>
                <color>ff0000ff</color>
                <width>2</width>
            </LineStyle>
        </Style>
        <Style id="restrictedStyle">
            <IconStyle>
                <color>ffff0000</color>
                <scale>1.0</scale>
                <Icon>
                    <href>http://maps.google.com/mapfiles/kml/shapes/forbidden.png</href>
                </Icon>
            </IconStyle>
        </Style>
        <Style id="restrictedSegmentStyle">
            <LineStyle>
                <color>ff0000ff</color>
                <width>2</width>
            </LineStyle>
            <PolyStyle>
                <color>7f0000ff</color>
            </PolyStyle>
        </Style>
    </Document>
    </kml>
    """

        with open(filename, 'w') as f:
            f.write(kml_content)

    def generate_path_kml(self):
        if not self.current_airspace:
            messagebox.showwarning("Warning", "No airspace loaded")
            return

        origin_name = tk.simpledialog.askstring("Path KML", "Enter origin node name:")
        if not origin_name:
            return

        destination_name = tk.simpledialog.askstring("Path KML", "Enter destination node name:")
        if not destination_name:
            return

        path = FindShortestPathInAirspace(self.current_airspace, origin_name, destination_name)
        if not path:
            messagebox.showinfo("Info", "No path exists between these nodes")
            return

        filename = filedialog.asksaveasfilename(
            title="Save Path KML File",
            defaultextension=".kml",
            filetypes=(("KML files", "*.kml"), ("All files", "*.*")))

        if filename:
            try:
                self.create_path_kml(filename, path)
                messagebox.showinfo("Success", f"Path KML file saved successfully: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate path KML: {str(e)}")

    def create_path_kml(self, filename, path):
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
        <name>Shortest Path</name>
        <description>Generated by Graph Explorer</description>
        <Style id="pathStyle">
            <LineStyle>
                <color>ff00ffff</color>
                <width>4</width>
            </LineStyle>
        </Style>
        <Style id="nodeStyle">
            <IconStyle>
                <color>ffffff00</color>
                <scale>1.0</scale>
                <Icon>
                    <href>http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png</href>
                </Icon>
            </IconStyle>
        </Style>
    """

        # Add path line
        kml_content += """
        <Placemark>
            <name>Shortest Path</name>
            <description>From {0} to {1}</description>
            <styleUrl>#pathStyle</styleUrl>
            <LineString>
                <coordinates>
    """.format(path.nodes[0].name, path.nodes[-1].name)

        for node in path.nodes:
            kml_content += f"                {node.longitude},{node.latitude},0\n"

        kml_content += """            </coordinates>
            </LineString>
        </Placemark>
    """

        # Add path nodes
        for i, node in enumerate(path.nodes):
            kml_content += f"""
        <Placemark>
            <name>{node.name}</name>
            <description>Node {i + 1} in path</description>
            <styleUrl>#nodeStyle</styleUrl>
            <Point>
                <coordinates>{node.longitude},{node.latitude},0</coordinates>
            </Point>
        </Placemark>
    """

        kml_content += """
    </Document>
    </kml>
    """

        with open(filename, 'w') as f:
            f.write(kml_content)

    def add_restrictions_dialog(self):
        if not self.current_airspace:
            messagebox.showwarning("Warning", "No airspace loaded")
            return

        restriction_type = tk.simpledialog.askstring("Add Restrictions",
                                                     "Add restriction for:\n1. Node by name\n2. Node by number\n3. Segment by names\n4. Segment by numbers\nEnter choice (1-4):")

        if not restriction_type:
            return

        if restriction_type == "1":
            node_name = tk.simpledialog.askstring("Add Restrictions", "Enter node name to restrict:")
            if node_name:
                self.restricted_nodes.add(node_name)
                messagebox.showinfo("Success", f"Node {node_name} restricted")
        elif restriction_type == "2":
            node_number = tk.simpledialog.askstring("Add Restrictions", "Enter node number to restrict:")
            if node_number:
                self.restricted_nodes.add(int(node_number))
                messagebox.showinfo("Success", f"Node {node_number} restricted")
        elif restriction_type == "3":
            segment_names = tk.simpledialog.askstring("Add Restrictions",
                                                      "Enter segment to restrict (format: origin-destination):")
            if segment_names:
                self.restricted_segments.add(segment_names)
                messagebox.showinfo("Success", f"Segment {segment_names} restricted")
        elif restriction_type == "4":
            segment_numbers = tk.simpledialog.askstring("Add Restrictions",
                                                        "Enter segment to restrict (format: originNumber-destinationNumber):")
            if segment_numbers:
                self.restricted_segments.add(segment_numbers)
                messagebox.showinfo("Success", f"Segment {segment_numbers} restricted")
        else:
            messagebox.showerror("Error", "Invalid choice")

    def compare_algorithms(self):
        if not self.current_airspace:
            messagebox.showwarning("Warning", "No airspace loaded")
            return

        origin_name = tk.simpledialog.askstring("Compare Algorithms", "Enter origin node name:")
        if not origin_name:
            return

        destination_name = tk.simpledialog.askstring("Compare Algorithms", "Enter destination node name:")
        if not destination_name:
            return

        # Time A* algorithm
        import time
        start_time = time.time()
        path_astar = FindShortestPathInAirspace(self.current_airspace, origin_name, destination_name)
        astar_time = time.time() - start_time

        # Time Dijkstra algorithm
        start_time = time.time()
        path_dijkstra = self.dijkstra_shortest_path(origin_name, destination_name)
        dijkstra_time = time.time() - start_time

        if path_astar and path_dijkstra:
            message = f"A* Algorithm:\n"
            message += f"  Time: {astar_time:.6f} seconds\n"
            message += f"  Path cost: {path_astar.cost:.2f} km\n"
            message += f"  Path: {' -> '.join([n.name for n in path_astar.nodes])}\n\n"

            message += f"Dijkstra Algorithm:\n"
            message += f"  Time: {dijkstra_time:.6f} seconds\n"
            message += f"  Path cost: {path_dijkstra.cost:.2f} km\n"
            message += f"  Path: {' -> '.join([n.name for n in path_dijkstra.nodes])}\n\n"

            if path_astar.cost == path_dijkstra.cost:
                message += "Both algorithms found the same optimal path."
            else:
                message += "Warning: Algorithms found different paths!"

            messagebox.showinfo("Algorithm Comparison", message)
        else:
            messagebox.showinfo("Algorithm Comparison", "No path exists between these nodes")

    def dijkstra_shortest_path(self, origin_name, destination_name):
        origin = self.current_airspace.find_navpoint_by_name(origin_name)
        destination = self.current_airspace.find_navpoint_by_name(destination_name)

        if not origin or not destination:
            return None

        import heapq

        # Priority queue: (total_cost, current_node, path)
        heap = []
        heapq.heappush(heap, (0, origin, [origin]))

        visited = set()

        while heap:
            current_cost, current_node, current_path = heapq.heappop(heap)

            if current_node == destination:
                return Path(current_path, current_cost)

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    # Find the segment between current_node and neighbor
                    segment = None
                    for seg in self.current_airspace.nav_segments:
                        if (seg.origin_number == current_node.number and
                                seg.destination_number == neighbor.number):
                            segment = seg
                            break

                    if segment:
                        new_cost = current_cost + segment.distance
                        new_path = current_path.copy()
                        new_path.append(neighbor)
                        heapq.heappush(heap, (new_cost, neighbor, new_path))

        return None
    def open_specific_image(self):
        image_path = os.path.join(os.path.dirname(__file__), "img", "foto.jpg")

        if os.path.exists(image_path):
            try:
                if platform.system() == 'Windows':
                    os.startfile(image_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.call(['open', image_path])
                elif platform.system() == 'Linux':
                    subprocess.call(['xdg-open', image_path])
            except Exception as e:
                messagebox.showerror("Error", f"No s'ha pogut obrir la imatge: {e}")
        else:
            messagebox.showerror("Error", f"No s'ha trobat la imatge: {image_path}")

    def modo_festa(self):
        if not self.current_graph:
            messagebox.showwarning("Avis", "No hi ha graf carregat")
            return

        colors = ['#FF69B4', '#00FFFF', '#ADFF2F', '#FFA500', '#9370DB', '#FF4500', '#00FF00']
        self.ax.clear()

        for seg in self.current_graph.segments:
            self.ax.plot([seg.origin.x, seg.destination.x],
                         [seg.origin.y, seg.destination.y],
                         color=random.choice(colors), linewidth=2)

        for node in self.current_graph.nodes:
            self.ax.plot(node.x, node.y, 'o', markersize=12, color=random.choice(colors))
            self.ax.text(node.x, node.y, node.name,
                         fontsize=10, ha='center', va='center', color='black', fontweight='bold')

        self.ax.set_title("PARTY MODE ON", fontsize=14, color=random.choice(colors))
        self.canvas.draw()

    def animate_shortest_path(self, path):
        if not path or len(path.nodes) < 2:
            messagebox.showinfo("Info", "No path to animate.")
            return

        self.ax.clear()

        # Draw the full graph in the background (gray)
        for seg in self.current_graph.segments:
            self.ax.plot([seg.origin.x, seg.destination.x],
                         [seg.origin.y, seg.destination.y],
                         'gray', linewidth=1, alpha=0.3)

        # Draw all nodes
        for node in self.current_graph.nodes:
            self.ax.plot(node.x, node.y, 'o', markersize=8, color='gray')
            self.ax.text(node.x, node.y, node.name,
                         fontsize=8, ha='center', va='center', color='black')

        self.canvas.draw()

        # Animate each segment of the path like a "snake"
        for i in range(len(path.nodes) - 1):
            origin = path.nodes[i]
            destination = path.nodes[i + 1]

            self.ax.plot([origin.x, destination.x],
                         [origin.y, destination.y],
                         'lime', linewidth=3)

            self.ax.plot(origin.x, origin.y, 'o', color='blue', markersize=10)
            self.ax.plot(destination.x, destination.y, 'o', color='red', markersize=10)

            self.canvas.draw()
            self.root.update()
            time.sleep(0.5)  # pause between steps

        self.ax.set_title("🐍 Snake Path Animation", fontsize=12)
        self.canvas.draw()

    def run_snake_path_animation(self):
        if not self.current_graph or len(self.current_graph.nodes) < 2:
            messagebox.showwarning("Warning", "No graph loaded or not enough nodes.")
            return

        origin = tk.simpledialog.askstring("Snake Path", "Enter origin node name:")
        if not origin:
            return
        destination = tk.simpledialog.askstring("Snake Path", "Enter destination node name:")
        if not destination:
            return

        path = FindShortestPath(self.current_graph, origin, destination)
        if path:
            self.animate_shortest_path(path)
        else:
            messagebox.showinfo("Path", "No path exists between the selected nodes.")

    def animate_airspace_path(self, path):
        if not path or len(path.nodes) < 2:
            messagebox.showinfo("Info", "No path to animate.")
            return

        self.ax.clear()

        # Draw all points and segments in gray
        for seg in self.current_airspace.nav_segments:
            origin = self.current_airspace.find_navpoint_by_number(seg.origin_number)
            destination = self.current_airspace.find_navpoint_by_number(seg.destination_number)
            if origin and destination:
                self.ax.plot([origin.longitude, destination.longitude],
                             [origin.latitude, destination.latitude],
                             'gray', linewidth=0.5, alpha=0.3)

        for point in self.current_airspace.nav_points:
            self.ax.plot(point.longitude, point.latitude, 'o', markersize=3, color='gray', alpha=0.5)

        self.canvas.draw()

        # Animate each segment
        for i in range(len(path.nodes) - 1):
            origin = path.nodes[i]
            destination = path.nodes[i + 1]

            self.ax.plot([origin.longitude, destination.longitude],
                         [origin.latitude, destination.latitude],
                         'lime', linewidth=2)

            self.ax.plot(origin.longitude, origin.latitude, 'o', color='blue', markersize=8)
            self.ax.plot(destination.longitude, destination.latitude, 'o', color='red', markersize=8)

            self.canvas.draw()
            self.root.update()
            time.sleep(0.4)

        self.ax.set_title("🐍 Snake Path Animation (Airspace)", fontsize=12)
        self.canvas.draw()

    def run_airspace_snake_path(self):
        if not self.current_airspace:
            messagebox.showwarning("Warning", "No airspace loaded.")
            return

        origin = tk.simpledialog.askstring("Snake Path", "Enter origin navpoint name:")
        if not origin:
            return
        destination = tk.simpledialog.askstring("Snake Path", "Enter destination navpoint name:")
        if not destination:
            return

        path = FindShortestPathInAirspace(self.current_airspace, origin, destination)
        if path:
            self.animate_airspace_path(path)
        else:
            messagebox.showinfo("Path", "No path found between the selected navpoints.")


    def add_restrictions_dialog(self):
        if not self.current_airspace:
            messagebox.showwarning("Warning", "No airspace loaded")
            return

        restriction_type = tk.simpledialog.askstring("Add Restrictions",
                                                     "Add restriction for:\n1. Node by name\n2. Node by number\n3. Segment by names\n4. Segment by numbers\nEnter choice (1-4):")

        if not restriction_type:
            return

        if restriction_type == "1":
            node_name = tk.simpledialog.askstring("Add Restrictions", "Enter node name to restrict:")
            if node_name:
                self.restricted_nodes.add(node_name)
                messagebox.showinfo("Success", f"Node {node_name} restricted")
        elif restriction_type == "2":
            node_number = tk.simpledialog.askstring("Add Restrictions", "Enter node number to restrict:")
            if node_number:
                try:
                    node_num = int(node_number)
                    self.restricted_nodes.add(node_num)
                    messagebox.showinfo("Success", f"Node {node_num} restricted")
                except ValueError:
                    messagebox.showerror("Error", "Node number must be an integer")
        elif restriction_type == "3":
            segment_names = tk.simpledialog.askstring("Add Restrictions",
                                                      "Enter segment to restrict (format: origin-destination):")
            if segment_names:
                # Validar formato
                if '-' in segment_names and len(segment_names.split('-')) == 2:
                    self.restricted_segments.add(segment_names)
                    messagebox.showinfo("Success", f"Segment {segment_names} restricted")
                else:
                    messagebox.showerror("Error", "Invalid format. Use 'origin-destination'")
        elif restriction_type == "4":
            segment_numbers = tk.simpledialog.askstring("Add Restrictions",
                                                        "Enter segment to restrict (format: originNumber-destinationNumber):")
            if segment_numbers:
                # Validar formato
                if '-' in segment_numbers and len(segment_numbers.split('-')) == 2:
                    try:
                        orig, dest = segment_numbers.split('-')
                        orig_num = int(orig.strip())
                        dest_num = int(dest.strip())
                        self.restricted_segments.add(f"{orig_num}-{dest_num}")
                        messagebox.showinfo("Success", f"Segment {orig_num}-{dest_num} restricted")
                    except ValueError:
                        messagebox.showerror("Error", "Segment numbers must be integers")
                else:
                    messagebox.showerror("Error", "Invalid format. Use 'originNumber-destinationNumber'")
        else:
            messagebox.showerror("Error", "Invalid choice. Enter a number between 1-4")

    def setup_interaction(self):
        # Conectar eventos
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.canvas.mpl_connect('pick_event', self.on_pick)

        # Eliminar zoom_frame antic si existeix
        if self.zoom_frame is not None:
            self.zoom_frame.destroy()

        # Crear nou zoom_frame
        self.zoom_frame = tk.Frame(self.control_frame)
        self.zoom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        tk.Button(self.zoom_frame, text="Zoom Out", command=lambda: self.zoom(1.2)).pack(side=tk.LEFT, expand=True)
        tk.Button(self.zoom_frame, text="Zoom In", command=lambda: self.zoom(0.8)).pack(side=tk.LEFT, expand=True)
        tk.Button(self.zoom_frame, text="Reset View", command=self.reset_view).pack(side=tk.LEFT, expand=True)

        # Guardar límits inicials
        self.initial_xlim = self.ax.get_xlim()
        self.initial_ylim = self.ax.get_ylim()

        def convert_airspace_to_graph(self):
            if not self.current_airspace:
                return

            g = Graph()
            name_to_node = {}

            for navpoint in self.current_airspace.nav_points:
                node = Node(navpoint.name, navpoint.longitude, navpoint.latitude)
                g.nodes.append(node)
                name_to_node[navpoint.number] = node

            for seg in self.current_airspace.nav_segments:
                origin_nav = self.current_airspace.find_navpoint_by_number(seg.origin_number)
                dest_nav = self.current_airspace.find_navpoint_by_number(seg.destination_number)

                origin = name_to_node.get(seg.origin_number)
                destination = name_to_node.get(seg.destination_number)

                if origin and destination:
                    g.segments.append(Segment(f"{origin.name}-{destination.name}", origin, destination, seg.distance))

            self.current_graph = g
            self.current_airspace = None
            self.plot_current_graph()

    def convert_airspace_to_graph(self):
        if not self.current_airspace:
            return

        g = Graph()
        name_to_node = {}

        for navpoint in self.current_airspace.nav_points:
            node = Node(navpoint.name, navpoint.longitude, navpoint.latitude)
            g.nodes.append(node)
            name_to_node[navpoint.number] = node

        for seg in self.current_airspace.nav_segments:
            origin_nav = self.current_airspace.find_navpoint_by_number(seg.origin_number)
            dest_nav = self.current_airspace.find_navpoint_by_number(seg.destination_number)

            origin = name_to_node.get(seg.origin_number)
            destination = name_to_node.get(seg.destination_number)

            if origin and destination:
                g.segments.append(Segment(f"{origin.name}-{destination.name}", origin, destination, seg.distance))

        self.current_graph = g
        self.current_airspace = None
        self.plot_current_graph()


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