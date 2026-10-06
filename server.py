"""
server.py
=========
Localhost Web Application and REST API Server for Emergency Route and Help Coordinator.
Serves static frontend from 'web/' and provides REST endpoints:
- GET  /              -> Serves web/index.html
- GET  /api/state     -> JSON live state (landmarks, hospitals, fleet, stats, logs)
- POST /api/dispatch  -> Dispatches rescue vehicle and computes fastest route
"""

import http.server
import json
import mimetypes
import os
import random
import socketserver
import sys
import urllib.parse

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from core.entity import MedicalCenter, RescueVehicle, EmergencyAlert
from core.router import (
    UrbanCorridorGraph,
    filter_idle_fleet,
    locate_nearest_medical_center,
    extract_waypoint_positions,
    fetch_openstreetmap_route
)
from core.validator import check_phone_format, append_record_to_file, fetch_all_records
from core.visualizer import compute_fleet_statistics, render_trend_curve, generate_interactive_map_html
from run import build_ahmedabad_corridor_graph, initialize_environment

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, 'web')

# Global System State
GRAPH, MEDICAL_CENTERS, FLEET, DURATIONS = initialize_environment()
render_trend_curve(DURATIONS)


class CoordinatorHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[HTTP] {self.command} {self.path} -> {args[0] if args else ''}")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 1. Main Web Dashboard
        if path in ["/", "/index.html"]:
            index_path = os.path.join(WEB_DIR, "index.html")
            if os.path.exists(index_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(index_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # 2. Live State JSON API
        if path == "/api/state":
            analytics = compute_fleet_statistics(DURATIONS)
            records = fetch_all_records()
            landmarks = {
                k: {"label": v["label"], "coords": v["coords"]}
                for k, v in GRAPH.vertices.items()
            }
            hospitals = [
                {
                    "hospital_id": h.center_id,
                    "title": h.title,
                    "available_beds": h.available_beds,
                    "latitude": h.position[0],
                    "longitude": h.position[1]
                }
                for h in MEDICAL_CENTERS
            ]
            fleet = [
                {
                    "vehicle_id": v.vehicle_id,
                    "vehicle_type": v.vehicle_type,
                    "current_station": v.current_station,
                    "status": v.operational_status,
                    "latitude": v.latitude,
                    "longitude": v.longitude
                }
                for v in FLEET
            ]

            payload = {
                "landmarks": landmarks,
                "hospitals": hospitals,
                "fleet": fleet,
                "analytics": analytics,
                "records": records
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
            return

        # 3. Serve Static Files (web/, data/, root)
        clean_path = path.lstrip("/")
        candidate_paths = [
            os.path.join(WEB_DIR, clean_path),
            os.path.join(BASE_DIR, clean_path),
            os.path.join(BASE_DIR, "data", clean_path)
        ]

        for file_path in candidate_paths:
            if os.path.isfile(file_path):
                mime_type, _ = mimetypes.guess_type(file_path)
                self.send_response(200)
                if mime_type:
                    self.send_header("Content-Type", mime_type)
                self.end_headers()
                with open(file_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        self.send_error(404, "File Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/dispatch":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body) if body else {}
            except Exception:
                data = {}

            caller_name = data.get("caller_name", "Rahul Sharma")
            phone = data.get("phone", "")
            hazard_type = data.get("hazard_type", "Medical")
            node_key = data.get("node_key", "N2")

            # Validate Phone
            if not check_phone_format(phone):
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Contact number must be 10 digits starting with 6-9."}).encode("utf-8"))
                return

            hazard_map = {"Medical": "Ambulance", "Fire": "Fire Engine", "Police": "Police Patrol"}
            vehicle_type = hazard_map.get(hazard_type, "Ambulance")

            dest_info = GRAPH.vertices.get(node_key)
            if not dest_info:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid destination landmark node."}).encode("utf-8"))
                return

            dest_coords = dest_info["coords"]

            # Filter Idle Vehicle
            available_units = filter_idle_fleet(FLEET, vehicle_type)
            if not available_units:
                available_units = filter_idle_fleet(FLEET)
            if not available_units:
                for v in FLEET:
                    v.mark_available()
                available_units = [FLEET[0]]

            assigned_unit = available_units[0]
            assigned_unit.deploy_to_site()

            # Hospital match
            matched_center = locate_nearest_medical_center(dest_coords, MEDICAL_CENTERS)
            if matched_center:
                matched_center.admit_emergency_case()

            # Routing via OSRM Live API or Dijkstra
            origin_coords = (assigned_unit.latitude, assigned_unit.longitude)
            osm_time, osm_dist, osm_coords = fetch_openstreetmap_route(origin_coords, dest_coords)

            if osm_time and osm_coords:
                eta_mins = osm_time
                total_km = osm_dist
                route_points = osm_coords
                routing_source = "OpenStreetMap OSRM Live API"
            else:
                eta_mins, total_km, path = GRAPH.find_fastest_corridor(assigned_unit.current_station, node_key)
                route_points = extract_waypoint_positions(path, GRAPH)
                routing_source = "Dijkstra Shortest Path Engine"

            DURATIONS.append(eta_mins)

            # Persistent Storage
            tag_id = f"SOS-{random.randint(100, 999)}"
            append_record_to_file(tag_id, caller_name, phone, hazard_type, "High", dest_info["label"])

            # Refresh Visuals
            generate_interactive_map_html(
                dest_info["label"], dest_coords, assigned_unit, matched_center,
                route_points, eta_mins, total_km
            )
            render_trend_curve(DURATIONS)

            response_data = {
                "tag_id": tag_id,
                "caller_name": caller_name,
                "phone": phone,
                "hazard_type": hazard_type,
                "destination": {
                    "key": node_key,
                    "label": dest_info["label"],
                    "coords": dest_coords
                },
                "assigned_unit": {
                    "vehicle_id": assigned_unit.vehicle_id,
                    "vehicle_type": assigned_unit.vehicle_type,
                    "current_station": assigned_unit.current_station,
                    "latitude": assigned_unit.latitude,
                    "longitude": assigned_unit.longitude
                },
                "matched_center": {
                    "hospital_id": matched_center.center_id if matched_center else "H1",
                    "title": matched_center.title if matched_center else "Emergency Hospital",
                    "available_beds": matched_center.available_beds if matched_center else 0,
                    "latitude": matched_center.position[0] if matched_center else dest_coords[0],
                    "longitude": matched_center.position[1] if matched_center else dest_coords[1]
                },
                "eta_mins": eta_mins,
                "total_km": total_km,
                "routing_source": routing_source,
                "route_points": route_points
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        self.send_error(404, "Endpoint Not Found")


def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CoordinatorHTTPRequestHandler) as httpd:
        print(f"==================================================================")
        print(f"  Emergency Route & Help Coordinator Localhost Server Active")
        print(f"  Local URL: http://localhost:{PORT}")
        print(f"==================================================================")
        httpd.serve_forever()


if __name__ == "__main__":
    start_server()
