"""
gui.py
======
Desktop Tkinter GUI for Emergency Route and Help Coordinator.
Matches the exact classic UI layout from the course project:
1. Report Emergency
2. Find Emergency Route
3. View Available Help
4. Assign Help
5. View Emergency Records
6. Start Emergency Monitoring
7. Show Emergency Map (Turtle)
8. Exit
"""

import os
import random
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

from core.entity import MedicalCenter, RescueVehicle
from core.router import (
    UrbanCorridorGraph,
    filter_idle_fleet,
    locate_nearest_medical_center,
    extract_waypoint_positions,
    fetch_openstreetmap_route
)
from core.validator import check_phone_format, append_record_to_file, fetch_all_records
from core.visualizer import compute_fleet_statistics, render_trend_curve
from core.turtle_visualizer import draw_turtle_simulation
from run import build_ahmedabad_corridor_graph, initialize_environment


class EmergencyCoordinatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Route and Help Coordinator (Educational Simulation)")
        self.root.geometry("450x530")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        # Initialize Environment
        self.graph, self.medical_centers, self.fleet, self.durations = initialize_environment()
        self.emergency_counter = len(fetch_all_records()) + 1
        self.latest_emergency = None
        self.monitoring_active = False

        self._build_main_menu()

    def _build_main_menu(self):
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#f0f0f0")
        header_frame.pack(pady=20)

        title_lbl = tk.Label(
            header_frame,
            text="Emergency Route and Help Coordinator",
            font=("Arial", 14, "bold"),
            bg="#f0f0f0",
            fg="#000000"
        )
        title_lbl.pack()

        subtitle_lbl = tk.Label(
            header_frame,
            text="Educational simulation only -- not a real emergency service.",
            font=("Arial", 9, "italic"),
            bg="#f0f0f0",
            fg="#cc0000"
        )
        subtitle_lbl.pack(pady=(4, 0))

        # Menu Buttons Frame
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        buttons = [
            ("1. Report Emergency", self.open_report_emergency_window),
            ("2. Find Emergency Route", self.find_emergency_route),
            ("3. View Available Help", self.view_available_help),
            ("4. Assign Help", self.assign_help),
            ("5. View Emergency Records", self.view_emergency_records),
            ("6. Start Emergency Monitoring", self.start_emergency_monitoring),
            ("7. Show Emergency Map (Turtle)", self.show_turtle_map),
            ("8. Exit", self.root.destroy)
        ]

        for text, cmd in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                width=28,
                font=("Arial", 10),
                relief="raised",
                bd=2,
                cursor="hand2",
                command=cmd
            )
            btn.pack(pady=5)

    def open_report_emergency_window(self):
        """Opens 'Report Emergency' dialog matching the user screenshot."""
        report_win = tk.Toplevel(self.root)
        report_win.title("Report Emergency")
        report_win.geometry("400x380")
        report_win.resizable(False, False)
        report_win.configure(bg="#f0f0f0")
        report_win.grab_set()

        content_frame = tk.Frame(report_win, bg="#f0f0f0", padx=20, pady=15)
        content_frame.pack(fill="both", expand=True)

        # Name
        tk.Label(content_frame, text="Name", font=("Arial", 10), bg="#f0f0f0", anchor="w").pack(fill="x")
        name_entry = tk.Entry(content_frame, font=("Arial", 10), relief="groove", bd=2)
        name_entry.insert(0, "dhruv")
        name_entry.pack(fill="x", pady=(2, 10))

        # Phone Number
        tk.Label(content_frame, text="Phone Number (10 digits)", font=("Arial", 10), bg="#f0f0f0", anchor="w").pack(fill="x")
        phone_entry = tk.Entry(content_frame, font=("Arial", 10), relief="groove", bd=2)
        phone_entry.insert(0, "9685633462")
        phone_entry.pack(fill="x", pady=(2, 10))

        # Current Location
        tk.Label(content_frame, text="Current Location", font=("Arial", 10), bg="#f0f0f0", anchor="w").pack(fill="x")
        location_entry = tk.Entry(content_frame, font=("Arial", 10), relief="groove", bd=2)
        location_entry.insert(0, "ghodasar")
        location_entry.pack(fill="x", pady=(2, 10))

        # Destination / Hospital
        tk.Label(content_frame, text="Destination/Hospital", font=("Arial", 10), bg="#f0f0f0", anchor="w").pack(fill="x")
        dest_entry = tk.Entry(content_frame, font=("Arial", 10), relief="groove", bd=2)
        dest_entry.insert(0, "hospital")
        dest_entry.pack(fill="x", pady=(2, 10))

        # Emergency Type
        tk.Label(content_frame, text="Emergency Type", font=("Arial", 10), bg="#f0f0f0", anchor="w").pack(fill="x")
        type_var = tk.StringVar(value="Crime")
        type_combo = ttk.Combobox(
            content_frame,
            textvariable=type_var,
            values=["Crime", "Medical", "Fire", "Accident"],
            state="readonly",
            font=("Arial", 10)
        )
        type_combo.pack(fill="x", pady=(2, 18))

        def submit():
            name = name_entry.get().strip() or "Citizen"
            phone = phone_entry.get().strip()
            loc = location_entry.get().strip() or "Ahmedabad"
            dest = dest_entry.get().strip() or "Hospital"
            etype = type_var.get()

            # Validation
            if not check_phone_format(phone):
                messagebox.showerror(
                    "Validation Error",
                    "Contact number must be 10 digits starting with 6, 7, 8, or 9."
                )
                return

            tag_id = f"E-{self.emergency_counter}"
            self.emergency_counter += 1
            priority = "High" if etype in ["Crime", "Medical", "Fire"] else "Medium"

            # Save to text records
            append_record_to_file(tag_id, name, phone, etype, priority, loc)

            # Store in session
            node_keys = list(self.graph.vertices.keys())
            dest_node = random.choice(node_keys[1:4])
            self.latest_emergency = {
                "tag_id": tag_id,
                "name": name,
                "phone": phone,
                "type": etype,
                "priority": priority,
                "location": loc,
                "destination": dest,
                "node_key": dest_node
            }

            report_win.destroy()

            # Popup matching user screenshot
            messagebox.showinfo(
                "Emergency Reported",
                f"Emergency {tag_id} reported.\nPriority: {priority}"
            )

        submit_btn = tk.Button(
            content_frame,
            text="Submit Emergency",
            font=("Arial", 10),
            relief="raised",
            bd=2,
            cursor="hand2",
            padx=10,
            command=submit
        )
        submit_btn.pack(pady=5)

    def find_emergency_route(self):
        """Calculates optimal shortest path corridor using Dijkstra engine."""
        dest_node = self.latest_emergency["node_key"] if self.latest_emergency else "N2"
        start_node = "N1"

        eta, dist, path = self.graph.find_fastest_corridor(start_node, dest_node)
        path_str = " ➔ ".join(path)
        dest_name = self.graph.vertices[dest_node]["label"]

        info_msg = (
            f"📍 Route Plan for Emergency Incident:\n"
            f"-----------------------------------------\n"
            f"• Origin Hub    : {self.graph.vertices[start_node]['label']} ({start_node})\n"
            f"• Destination   : {dest_name} ({dest_node})\n"
            f"• Shortest Path : {path_str}\n"
            f"• Total Distance: {dist} km\n"
            f"• Estimated ETA : {eta} minutes\n"
            f"• Routing Alg.  : Dijkstra Shortest Path Engine"
        )
        messagebox.showinfo("Emergency Route Found", info_msg)

    def view_available_help(self):
        """Displays table of available rescue vehicles and hospital bed capacity."""
        help_win = tk.Toplevel(self.root)
        help_win.title("Available Emergency Help & Fleet")
        help_win.geometry("540x360")
        help_win.configure(bg="#ffffff")

        tk.Label(
            help_win, 
            text="🚑 Emergency Fleet & Medical Centers", 
            font=("Arial", 12, "bold"), 
            bg="#ffffff", 
            fg="#0f172a"
        ).pack(pady=10)

        text_box = tk.Text(help_win, font=("Consolas", 10), wrap="word", padx=10, pady=10, bg="#f8fafc", bd=1)
        text_box.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        lines = [
            "RESCUE VEHICLES FLEET:",
            "=" * 50
        ]
        for v in self.fleet:
            lines.append(f"• {v.vehicle_id:<10} | {v.vehicle_type:<14} | Station: {v.current_station:<4} | Status: {v.operational_status}")

        lines.extend([
            "",
            "HOSPITALS & MEDICAL CENTERS:",
            "=" * 50
        ])
        for h in self.medical_centers:
            lines.append(f"• {h.center_id:<5} | {h.title:<28} | Beds: {h.available_beds} left")

        text_box.insert("1.0", "\n".join(lines))
        text_box.configure(state="disabled")

    def assign_help(self):
        """Assigns nearest available vehicle and admits patient to hospital."""
        if not self.latest_emergency:
            dest_node = "N2"
            hazard = "Medical"
        else:
            dest_node = self.latest_emergency["node_key"]
            hazard = self.latest_emergency["type"]

        hazard_map = {"Medical": "Ambulance", "Fire": "Fire Engine", "Crime": "Police Patrol", "Accident": "Ambulance"}
        needed_type = hazard_map.get(hazard, "Ambulance")

        available_units = filter_idle_fleet(self.fleet, needed_type)
        if not available_units:
            available_units = filter_idle_fleet(self.fleet)
        if not available_units:
            for v in self.fleet:
                v.mark_available()
            available_units = [self.fleet[0]]

        assigned_unit = available_units[0]
        assigned_unit.deploy_to_site()

        dest_coords = self.graph.vertices[dest_node]["coords"]
        matched_hospital = locate_nearest_medical_center(dest_coords, self.medical_centers)
        if matched_hospital:
            matched_hospital.admit_emergency_case()

        msg = (
            f"✅ Help Assigned Successfully!\n\n"
            f"• Assigned Vehicle : {assigned_unit.vehicle_id} ({assigned_unit.vehicle_type})\n"
            f"• Vehicle Station  : {assigned_unit.current_station}\n"
            f"• Target Location  : {self.graph.vertices[dest_node]['label']}\n"
            f"• Hospital Match   : {matched_hospital.title} ({matched_hospital.available_beds} beds left)"
        )
        messagebox.showinfo("Help Assigned", msg)

    def view_emergency_records(self):
        """Displays stored emergency log records from text storage."""
        records = fetch_all_records()
        records_win = tk.Toplevel(self.root)
        records_win.title("Stored Emergency Records")
        records_win.geometry("620x350")
        records_win.configure(bg="#ffffff")

        tk.Label(
            records_win,
            text="📁 Persistent Emergency Distress Logs (data/emergency_records.txt)",
            font=("Arial", 11, "bold"),
            bg="#ffffff"
        ).pack(pady=10)

        text_area = tk.Text(records_win, font=("Consolas", 9), wrap="none", padx=10, pady=10, bg="#f8fafc", bd=1)
        text_area.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        if not records:
            text_area.insert("1.0", "No emergency records logged yet.")
        else:
            text_area.insert("1.0", "\n\n".join(f"[{i+1}] {rec}" for i, rec in enumerate(records)))

        text_area.configure(state="disabled")

    def start_emergency_monitoring(self):
        """Starts background monitoring simulation."""
        if self.monitoring_active:
            messagebox.showinfo("Monitoring", "Emergency monitoring is already running in background.")
            return

        self.monitoring_active = True

        def monitor_worker():
            for _ in range(3):
                time.sleep(1)
            self.monitoring_active = False

        threading.Thread(target=monitor_worker, daemon=True).start()
        messagebox.showinfo(
            "Emergency Monitoring",
            "🟢 Emergency Monitoring System Started!\n\n"
            "Active Threads: 1\n"
            "Corridor Sensors: 9 Active Nodes\n"
            "Fleet Status: Real-Time Auto-Tracking Active"
        )

    def show_turtle_map(self):
        """Launches Python Turtle Graphical Simulation."""
        dest_node = self.latest_emergency["node_key"] if self.latest_emergency else "N2"
        needed_type = "Ambulance"
        if self.latest_emergency and self.latest_emergency["type"] in ["Crime", "Police"]:
            needed_type = "Police Patrol"
        elif self.latest_emergency and self.latest_emergency["type"] == "Fire":
            needed_type = "Fire Engine"

        available = filter_idle_fleet(self.fleet, needed_type) or self.fleet
        assigned_unit = available[0]
        dest_coords = self.graph.vertices[dest_node]["coords"]
        matched_hospital = locate_nearest_medical_center(dest_coords, self.medical_centers)

        eta, dist, path_nodes = self.graph.find_fastest_corridor(assigned_unit.current_station, dest_node)

        draw_turtle_simulation(
            self.graph,
            assigned_unit.current_station,
            dest_node,
            path_nodes,
            assigned_unit,
            matched_hospital,
            eta,
            dist
        )


def launch_gui():
    root = tk.Tk()
    app = EmergencyCoordinatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
