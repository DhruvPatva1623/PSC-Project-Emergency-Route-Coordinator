"""
core/router.py
==============
TOPIC USED:
- Graph Data Structure: Adjacency list representation using Dictionaries & Lists
- Shortest Path Algorithm: Dijkstra's Algorithm using Min-Heap Priority Queue (heapq)
- Recursion: Recursive path reconstruction (_trace_route_recursive) from destination to source
- Higher-Order Functions & Lambdas:
    * filter() with lambda -> filter available fleet by status & type
    * sorted() with lambda -> locate closest medical center using Euclidean distance
    * map() with lambda    -> extract coordinate waypoints from graph keys

WHERE IT CONNECTS:
- Connected to 'gui.py' & 'run.py' to find the shortest driving path, compute travel ETA, and match emergency units.
- Connected to 'core/turtle_visualizer.py' which draws the road graph and animates along the calculated Dijkstra path.
"""

import heapq
import math


class UrbanCorridorGraph:
    """
    TOPIC: Graph Data Structure & Algorithms
    Represents the road network of intersections and connecting corridors.
    """
    def __init__(self):
        # Dictionary storing vertex details: { node_id: {"label": str, "coords": (lat, lng)} }
        self.vertices = {}
        # Adjacency List: { node_id: [(neighbor_id, distance_km, speed_kmh)] }
        self.network = {}
        # Set for dynamic road hazards/blocks
        self.roadblocks = set()

    def register_intersection(self, node_key: str, label: str, latitude: float, longitude: float) -> None:
        """Registers a city intersection landmark."""
        self.vertices[node_key] = {
            "label": label,
            "coords": (latitude, longitude)
        }
        if node_key not in self.network:
            self.network[node_key] = []

    def connect_corridor(self, origin: str, destination: str, distance_km: float, speed_kmh: float = 50.0) -> None:
        """Adds a bidirectional road segment between two intersections."""
        if origin not in self.network:
            self.network[origin] = []
        if destination not in self.network:
            self.network[destination] = []

        self.network[origin].append((destination, distance_km, speed_kmh))
        self.network[destination].append((origin, distance_km, speed_kmh))

    def set_roadblock(self, u: str, v: str, is_blocked: bool = True) -> None:
        """Dynamically toggles roadblocks on specific corridors."""
        edge = tuple(sorted([u, v]))
        if is_blocked:
            self.roadblocks.add(edge)
        else:
            self.roadblocks.discard(edge)

    def find_fastest_corridor(self, start_node: str, end_node: str):
        """
        TOPIC: Dijkstra's Shortest Path Algorithm
        Uses a min-heap priority queue to find the route with the lowest travel time.
        Time Cost = (distance_km / speed_kmh) * 60.0 minutes.
        Returns: (travel_time_minutes, total_distance_km, path_sequence_list)
        """
        if start_node not in self.vertices or end_node not in self.vertices:
            return None, None, []

        # Priority Queue: (cumulative_time, current_node, cumulative_distance)
        priority_queue = [(0.0, start_node, 0.0)]
        shortest_times = {k: float("inf") for k in self.vertices}
        shortest_distances = {k: float("inf") for k in self.vertices}
        parent_map = {k: None for k in self.vertices}

        shortest_times[start_node] = 0.0
        shortest_distances[start_node] = 0.0

        while priority_queue:
            curr_time, curr_node, curr_dist = heapq.heappop(priority_queue)

            if curr_node == end_node:
                break

            if curr_time > shortest_times[curr_node]:
                continue

            for neighbor, edge_km, speed in self.network.get(curr_node, []):
                edge_pair = tuple(sorted([curr_node, neighbor]))
                if edge_pair in self.roadblocks:
                    continue

                corridor_time = (edge_km / speed) * 60.0
                new_time = curr_time + corridor_time
                new_dist = curr_dist + edge_km

                if new_time < shortest_times[neighbor]:
                    shortest_times[neighbor] = new_time
                    shortest_distances[neighbor] = new_dist
                    parent_map[neighbor] = curr_node
                    heapq.heappush(priority_queue, (new_time, neighbor, new_dist))

        if shortest_times[end_node] == float("inf"):
            return None, None, []

        # Reconstruct path using Recursion
        path = self._trace_route_recursive(parent_map, end_node)
        return round(shortest_times[end_node], 2), round(shortest_distances[end_node], 2), path

    def _trace_route_recursive(self, parent_map: dict, target_vertex: str) -> list:
        """
        TOPIC: Recursion
        Recursively backtracks parent pointers from destination to origin to build the path list.
        """
        if target_vertex is None:
            return []
        ancestor = parent_map[target_vertex]
        return self._trace_route_recursive(parent_map, ancestor) + [target_vertex]


# ====================================================================
# Higher-Order Functions & Lambda Implementations
# ====================================================================

def filter_idle_fleet(vehicles: list, target_type: str = None) -> list:
    """
    TOPIC: Higher-Order Function (filter) & Lambda Expression
    Filters available emergency vehicles from the fleet.
    """
    available_units = list(filter(lambda v: v.operational_status == "AVAILABLE", vehicles))
    if target_type:
        return list(filter(lambda v: v.vehicle_type.lower() == target_type.lower(), available_units))
    return available_units


def locate_nearest_medical_center(incident_pos: tuple, centers: list) -> object:
    """
    TOPIC: Higher-Order Function (sorted) & Lambda / Geometry
    Finds the hospital closest to the incident with available beds using Euclidean distance.
    """
    eligible = list(filter(lambda c: c.available_beds > 0, centers))
    if not eligible:
        eligible = centers

    def euclidean_gap(c):
        lat_diff = c.position[0] - incident_pos[0]
        lng_diff = c.position[1] - incident_pos[1]
        return math.sqrt(lat_diff**2 + lng_diff**2)

    ordered_centers = sorted(eligible, key=euclidean_gap)
    return ordered_centers[0] if ordered_centers else None


def extract_waypoint_positions(path_keys: list, graph: UrbanCorridorGraph) -> list:
    """
    TOPIC: Higher-Order Function (map) & Lambda Expression
    Maps node identifiers into coordinate tuples.
    """
    return list(map(lambda key: graph.vertices[key]["coords"], path_keys))
