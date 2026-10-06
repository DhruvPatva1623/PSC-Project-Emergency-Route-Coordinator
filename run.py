"""
run.py
======
Main Execution Script for Emergency Route & Help Coordinator.
Pure Python Desktop Application:
- Desktop Tkinter GUI (`gui.py`)
- Python Turtle Graphical Corridor Animation (`core/turtle_visualizer.py`)
- Dijkstra Shortest Path Engine (`core/router.py`)
- Object-Oriented Entities (`core/entity.py`)
- Regex Phone Validator & Text File Storage (`core/validator.py`)
- NumPy Vector Statistics & Matplotlib Plotting (`core/visualizer.py`)
"""

import os
import random
import sys

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
    extract_waypoint_positions
)
from core.validator import check_phone_format, append_record_to_file, fetch_all_records
from core.visualizer import compute_fleet_statistics, render_trend_curve
from core.turtle_visualizer import draw_turtle_simulation


def build_ahmedabad_corridor_graph() -> UrbanCorridorGraph:
    """Initializes road corridors and intersections in the Ahmedabad/Indus area."""
    city_graph = UrbanCorridorGraph()

    landmarks = [
        ("N1", "Indus University Campus", 23.0560, 72.4860),
        ("N2", "Thaltej Cross Roads", 23.0504, 72.5168),
        ("N3", "Sola Civil Circle", 23.0786, 72.5290),
        ("N4", "SG Highway Flyover", 23.0360, 72.5100),
        ("N5", "Vastrapur Lake", 23.0350, 72.5293),
        ("N6", "IIM Ahmedabad Road", 23.0305, 72.5460),
        ("N7", "Navrangpura Hub", 23.0373, 72.5613),
        ("N8", "Ashram Road Corridor", 23.0440, 72.5714),
        ("N9", "Science City Circle", 23.0780, 72.4980)
    ]
    for key, name, lat, lng in landmarks:
        city_graph.register_intersection(key, name, lat, lng)

    corridors = [
        ("N1", "N9", 3.2, 60.0),
        ("N9", "N3", 4.0, 50.0),
        ("N1", "N2", 3.8, 55.0),
        ("N2", "N3", 3.5, 50.0),
        ("N2", "N4", 2.2, 60.0),
        ("N2", "N5", 2.5, 45.0),
        ("N4", "N5", 2.0, 50.0),
        ("N3", "N5", 5.1, 50.0),
        ("N5", "N6", 2.1, 40.0),
        ("N6", "N7", 2.0, 45.0),
        ("N7", "N8", 1.8, 40.0),
        ("N3", "N7", 5.8, 50.0)
    ]
    for u, v, dist, speed in corridors:
        city_graph.connect_corridor(u, v, dist, speed)

    return city_graph


def initialize_environment():
    """Sets up graph network, hospitals, and vehicles."""
    graph = build_ahmedabad_corridor_graph()

    medical_centers = [
        MedicalCenter("H1", "Sola Civil Super Specialty", 23.0786, 72.5290, available_beds=14),
        MedicalCenter("H2", "Zydus Multi-Speciality", 23.0504, 72.5168, available_beds=8),
        MedicalCenter("H3", "Sterling Emergency Care", 23.0440, 72.5714, available_beds=5)
    ]

    fleet = [
        RescueVehicle("AMB-101", "Ambulance", "N1", 23.0560, 72.4860, cruising_speed_kmh=65.0),
        RescueVehicle("AMB-102", "Ambulance", "N5", 23.0350, 72.5293, cruising_speed_kmh=70.0),
        RescueVehicle("FIRE-201", "Fire Engine", "N7", 23.0373, 72.5613, cruising_speed_kmh=50.0),
        RescueVehicle("POL-301", "Police Patrol", "N9", 23.0780, 72.4980, cruising_speed_kmh=60.0)
    ]

    historical_durations = [7.5, 8.2, 5.9, 11.0, 9.4, 6.7, 13.5]

    return graph, medical_centers, fleet, historical_durations


def print_banner():
    print(r"""
======================================================================
  🚨 EMERGENCY ROUTE & HELP COORDINATOR
  Educational Simulation System
======================================================================
    """)


def handle_new_incident(graph, medical_centers, fleet, durations):
    """Processes new emergency dispatch request and animates via Turtle."""
    print("\n--- 📝 Emergency Distress Registration ---")
    caller_name = input("Enter Citizen / Caller Name [e.g. Rahul]: ").strip() or "Rahul Sharma"
    phone_number = input("Enter 10-Digit Contact Phone [e.g. 9876543210]: ").strip() or "9876543210"

    # Regular Expression Validation
    if not check_phone_format(phone_number):
        print("❌ Validation Error: Contact number must be 10 digits starting with 6-9.\n")
        return

    print("\nAvailable Emergency Types: [1] Medical [2] Fire [3] Police")
    type_choice = input("Select Type (1/2/3) [Default 1]: ").strip() or "1"
    hazard_map = {"1": ("Medical", "Ambulance"), "2": ("Fire", "Fire Engine"), "3": ("Police", "Police Patrol")}
    hazard_type, vehicle_type = hazard_map.get(type_choice, ("Medical", "Ambulance"))

    print("\nSelect Emergency Destination Node:")
    node_keys = list(graph.vertices.keys())
    for idx, key in enumerate(node_keys, 1):
        print(f"  {idx}. {key} - {graph.vertices[key]['label']}")

    selected_idx = int(input("Choose Node (1-9) [Default 2]: ").strip() or "2") - 1
    destination_node = node_keys[selected_idx]
    dest_info = graph.vertices[destination_node]
    dest_coords = dest_info["coords"]

    # 1. Filter available units
    available_units = filter_idle_fleet(fleet, vehicle_type)
    if not available_units:
        available_units = filter_idle_fleet(fleet)

    if not available_units:
        print("❌ Warning: All emergency vehicles are currently dispatched!\n")
        return

    assigned_unit = available_units[0]
    assigned_unit.deploy_to_site()

    # 2. Locate closest hospital
    matched_center = locate_nearest_medical_center(dest_coords, medical_centers)
    if matched_center:
        matched_center.admit_emergency_case()

    # 3. Compute Dijkstra Shortest Route
    eta_mins, total_km, path_nodes = graph.find_fastest_corridor(assigned_unit.current_station, destination_node)
    durations.append(eta_mins)

    # 4. Save record to persistent storage
    tag_id = f"SOS-{random.randint(100, 999)}"
    append_record_to_file(tag_id, caller_name, phone_number, hazard_type, "High", dest_info["label"])

    # Summary Output
    print("\n" + "=" * 55)
    print(f"✅ EMERGENCY DISPATCH CONFIRMATION [{tag_id}]")
    print("=" * 55)
    print(f"📍 Location Spot  : {dest_info['label']} ({destination_node})")
    print(f"🚑 Assigned Unit  : {assigned_unit.vehicle_id} ({assigned_unit.vehicle_type})")
    print(f"🏥 Medical Center : {matched_center.title} ({matched_center.available_beds} beds left)")
    print(f"⏱️ Estimated ETA   : {eta_mins} minutes")
    print(f"🛣️ Driving Distance: {total_km} km")
    print(f"🌐 Route Corridors: {' ➔ '.join(path_nodes)}")
    print("=" * 55)

    # 5. Launch Turtle Simulator Animation
    print("\n🐢 Launching Python Turtle Graphical Simulator...")
    draw_turtle_simulation(
        graph, 
        assigned_unit.current_station, 
        destination_node, 
        path_nodes, 
        assigned_unit, 
        matched_center, 
        eta_mins, 
        total_km
    )


def display_analytics_summary(durations):
    """Displays NumPy statistical analytics and renders Matplotlib curve."""
    metrics = compute_fleet_statistics(durations)
    print("\n" + "=" * 50)
    print("📊 FLEET RESPONSE ANALYTICS (NumPy)")
    print("=" * 50)
    print(f"• Total Incident Dispatches : {metrics['count']}")
    print(f"• Mean Response Time        : {metrics['mean_min']} minutes")
    print(f"• Median Response Time      : {metrics['median_min']} minutes")
    print(f"• Standard Deviation (σ)    : ±{metrics['std_dev']} minutes")
    print(f"• Fastest / Slowest Case    : {metrics['min_min']}m / {metrics['max_min']}m")
    print(f"• 2D Matrix Efficiency Score: {metrics['efficiency']} points")
    print("=" * 50)

    chart_file = render_trend_curve(durations)
    print(f"✅ Generated Matplotlib performance curve at: {chart_file}\n")


def view_stored_logs():
    """Reads and displays stored records from plain text file."""
    records = fetch_all_records()
    print("\n" + "=" * 50)
    print("📁 STORED EMERGENCY RECORDS (data/emergency_records.txt)")
    print("=" * 50)
    if not records:
        print("No records logged yet.")
    else:
        for idx, item in enumerate(records, 1):
            print(f"{idx}. {item}")
    print("=" * 50 + "\n")


def main():
    graph, medical_centers, fleet, durations = initialize_environment()
    print_banner()

    while True:
        print("------------------------------------------------------")
        print("1. 🖥️ Launch Desktop Tkinter Window (Classic GUI)")
        print("2. 🚨 Report Emergency & Run Turtle Simulator")
        print("3. 📁 View Stored Incident Logs (Text File)")
        print("4. 📊 View NumPy Analytics & Matplotlib Trend Curve")
        print("5. ❌ Exit Coordinator")
        print("------------------------------------------------------")

        user_input = input("Enter your selection (1-5): ").strip()

        if user_input == "1":
            print("\n🖥️ Opening Desktop Tkinter Window...")
            from gui import launch_gui
            launch_gui()
        elif user_input == "2":
            handle_new_incident(graph, medical_centers, fleet, durations)
        elif user_input == "3":
            view_stored_logs()
        elif user_input == "4":
            display_analytics_summary(durations)
        elif user_input == "5":
            print("\nShutting down Emergency Coordinator. Have a safe day!\n")
            break
        else:
            print("❌ Invalid selection. Please enter 1 to 5.\n")


if __name__ == "__main__":
    main()
