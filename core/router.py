"""
core/router.py
==============
Routing, Graph Algorithms, Recursion, and OpenStreetMap (OSRM) Live API module.
Demonstrates:
- Live OpenStreetMap (OSRM) Driving Route API
- Graph Data Structure (Adjacency List)
- Dijkstra's Shortest Path Algorithm
- Recursive Path Traceback
- Higher-Order Functions: filter(), map(), sorted() with lambda
(Syllabus: UNIT-I Functions, Recursion, Higher-Order Functions & UNIT-II Algorithms/Data Structures)
"""

import heapq
import math
import json
import urllib.request
import urllib.parse


def fetch_openstreetmap_route(origin_coords: tuple, dest_coords: tuple):
    """
    [UNIT-II: Networking / External OpenStreetMap API]
    Fetches real-world driving route, road distance (km), and travel time (min)
    using the public OpenStreetMap OSRM routing engine.
    
    Coordinates format: (latitude, longitude)
    Returns: (duration_minutes, distance_km, list_of_coordinates)
    """
    # OSRM expects format: {lon1},{lat1};{lon2},{lat2}
    start_lat, start_lng = origin_coords
    end_lat, end_lng = dest_coords
    
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{start_lng},{start_lat};{end_lng},{end_lat}?overview=full&geometries=geojson"
    )
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'EmergencyHelpCoordinator/1.0'})
        with urllib.request.urlopen(req, timeout=4.0) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get("code") == "Ok" and len(data.get("routes", [])) > 0:
                best_route = data["routes"][0]
                distance_km = round(best_route["distance"] / 1000.0, 2)
                duration_mins = round(best_route["duration"] / 60.0, 1)
                
                # Geometry is [ [lng, lat], ... ] -> convert to [ [lat, lng], ... ] for Leaflet
                path_coords = [[pt[1], pt[0]] for pt in best_route["geometry"]["coordinates"]]
                return duration_mins, distance_km, path_coords
    except Exception as err:
        # Fallback gracefully if offline
        pass

    return None, None, []


class UrbanCorridorGraph:
    """
    Graph representation of road corridors and intersections.
    Adjacency List: { node_key: [(adjacent_key, distance_km, speed_kmh)] }
    """
    def __init__(self):
        self.vertices = {}
        self.network = {}
        self.roadblocks = set()

    def register_intersection(self, node_key: str, label: str, latitude: float, longitude: float) -> None:
        """Registers a city intersection vertex."""
        self.vertices[node_key] = {
            "label": label,
            "coords": (latitude, longitude)
        }
        if node_key not in self.network:
            self.network[node_key] = []

    def connect_corridor(self, origin: str, destination: str, distance_km: float, speed_kmh: float = 50.0) -> None:
        """Adds a two-way street connection between two intersections."""
        if origin not in self.network:
            self.network[origin] = []
        if destination not in self.network:
            self.network[destination] = []

        self.network[origin].append((destination, distance_km, speed_kmh))
        self.network[destination].append((origin, distance_km, speed_kmh))

    def set_roadblock(self, u: str, v: str, is_blocked: bool = True) -> None:
        """Dynamically blocks or clears an edge."""
        edge = tuple(sorted([u, v]))
        if is_blocked:
            self.roadblocks.add(edge)
        else:
            self.roadblocks.discard(edge)

    def find_fastest_corridor(self, start_node: str, end_node: str):
        """
        [UNIT-II: Dijkstra's Shortest Path Algorithm]
        Computes the quickest route using travel time cost: (distance / speed) * 60 minutes.
        Returns: (travel_time_minutes, total_distance_km, path_sequence_list)
        """
        if start_node not in self.vertices or end_node not in self.vertices:
            return None, None, []

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

        # [UNIT-I: Recursion] Trace shortest path from destination to origin
        path = self._trace_route_recursive(parent_map, end_node)
        return round(shortest_times[end_node], 2), round(shortest_distances[end_node], 2), path

    def _trace_route_recursive(self, parent_map: dict, target_vertex: str) -> list:
        """
        [UNIT-I: Recursive Function]
        Recursively backtracks parent pointers to build path sequence.
        """
        if target_vertex is None:
            return []
        ancestor = parent_map[target_vertex]
        return self._trace_route_recursive(parent_map, ancestor) + [target_vertex]


# ====================================================================
# [UNIT-I: Higher-Order Functions with Lambdas]
# ====================================================================

def filter_idle_fleet(vehicles: list, target_type: str = None) -> list:
    """Demonstrates filter() and lambda to retrieve available rescue vehicles."""
    available_units = list(filter(lambda v: v.operational_status == "AVAILABLE", vehicles))
    if target_type:
        return list(filter(lambda v: v.vehicle_type.lower() == target_type.lower(), available_units))
    return available_units


def locate_nearest_medical_center(incident_pos: tuple, centers: list) -> object:
    """Demonstrates sorted() with lambda to compute Euclidean proximity."""
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
    """Demonstrates map() and lambda to transform node labels into coordinate tuples."""
    return list(map(lambda key: graph.vertices[key]["coords"], path_keys))
