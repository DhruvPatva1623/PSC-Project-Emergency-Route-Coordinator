"""
core/turtle_visualizer.py
=========================
Simple, clean Turtle Graphics simulator for Emergency Route Coordination.
Demonstrates standard library GUI (Python Turtle) for easy college PSC viva demo.
"""

import turtle
import time


# Coordinate scaling for Turtle screen [-300, 300]
# Maps Ahmedabad GPS coordinates roughly to screen pixels
LAT_MIN, LAT_MAX = 23.025, 23.085
LNG_MIN, LNG_MAX = 23.025, 72.580  # approx bounding


def gps_to_screen(lat: float, lng: float, width: int = 700, height: int = 500) -> tuple:
    """Converts GPS (lat, lng) to Turtle screen (x, y) coordinates."""
    # Ahmedabad range: lat ~ [23.030, 23.080], lng ~ [72.480, 72.580]
    x = ((lng - 72.480) / (72.580 - 72.480) - 0.5) * (width - 120)
    y = ((lat - 23.030) / (23.080 - 23.030) - 0.5) * (height - 120)
    return round(x, 1), round(y, 1)


def draw_turtle_simulation(graph, origin_node: str, dest_node: str, 
                           path_nodes: list, vehicle_obj, hospital_obj, eta_mins: float, total_km: float):
    """
    Renders an animated Turtle GUI showing:
    1. City road network & landmarks
    2. Hospital and Incident locations
    3. Animated emergency vehicle moving along the calculated route
    """
    screen = turtle.Screen()
    screen.setup(width=850, height=650)
    screen.title("🚨 Indus Emergency Route Coordinator - Turtle Simulator")
    screen.bgcolor("#0f172a")  # Dark slate background
    screen.tracer(0)  # Turn off auto-animation for fast drawing

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)

    # 1. Draw Title & Status Header
    pen.penup()
    pen.goto(-380, 270)
    pen.color("#38bdf8")
    pen.write("🚨 EMERGENCY ROUTE COORDINATOR (Python Turtle Simulator)", font=("Arial", 14, "bold"))
    
    pen.goto(-380, 245)
    pen.color("#94a3b8")
    info_text = f"Unit: {vehicle_obj.vehicle_id} | Dest: {dest_node} | Hospital: {hospital_obj.title} | ETA: {eta_mins} mins ({total_km} km)"
    pen.write(info_text, font=("Arial", 10, "normal"))

    # 2. Draw Road Corridors (Edges)
    pen.color("#334155")
    pen.pensize(2)
    for u, neighbors in graph.adjacency.items():
        u_lat, u_lng = graph.vertices[u]["coords"]
        x1, y1 = gps_to_screen(u_lat, u_lng)
        for v, dist, speed in neighbors:
            v_lat, v_lng = graph.vertices[v]["coords"]
            x2, y2 = gps_to_screen(v_lat, v_lng)
            pen.penup()
            pen.goto(x1, y1)
            pen.pendown()
            pen.goto(x2, y2)

    # 3. Draw Landmarks (Nodes)
    for node_key, info in graph.vertices.items():
        lat, lng = info["coords"]
        x, y = gps_to_screen(lat, lng)

        # Draw Node Circle
        pen.penup()
        pen.goto(x, y - 6)
        pen.color("#38bdf8")
        pen.begin_fill()
        pen.circle(6)
        pen.end_fill()

        # Node Label
        pen.penup()
        pen.goto(x + 10, y - 5)
        pen.color("#cbd5e1")
        pen.write(f"{node_key}: {info['label']}", font=("Arial", 8, "normal"))

    # 4. Highlight Incident Spot (Red Marker)
    dest_info = graph.vertices[dest_node]
    dx, dy = gps_to_screen(dest_info["coords"][0], dest_info["coords"][1])
    pen.penup()
    pen.goto(dx, dy - 12)
    pen.color("#ef4444")
    pen.begin_fill()
    pen.circle(12)
    pen.end_fill()
    pen.goto(dx - 15, dy + 15)
    pen.color("#ef4444")
    pen.write("🚨 INCIDENT", font=("Arial", 9, "bold"))

    # 5. Highlight Hospital Spot (Blue Marker)
    hx, hy = gps_to_screen(hospital_obj.position[0], hospital_obj.position[1])
    pen.penup()
    pen.goto(hx, hy - 10)
    pen.color("#0284c7")
    pen.begin_fill()
    pen.circle(10)
    pen.end_fill()
    pen.goto(hx - 20, hy - 25)
    pen.color("#38bdf8")
    pen.write(f"🏥 {hospital_obj.title}", font=("Arial", 8, "bold"))

    # 6. Highlight Shortest Path Corridors (Green Line)
    pen.color("#10b981")
    pen.pensize(4)
    for i in range(len(path_nodes) - 1):
        u = path_nodes[i]
        v = path_nodes[i+1]
        x1, y1 = gps_to_screen(graph.vertices[u]["coords"][0], graph.vertices[u]["coords"][1])
        x2, y2 = gps_to_screen(graph.vertices[v]["coords"][0], graph.vertices[v]["coords"][1])
        pen.penup()
        pen.goto(x1, y1)
        pen.pendown()
        pen.goto(x2, y2)

    screen.update()

    # 7. Animated Rescue Vehicle Moving along Path
    vehicle = turtle.Turtle()
    vehicle.shape("triangle")
    vehicle.color("#fbbf24")
    vehicle.shapesize(1.2, 1.2)
    vehicle.speed(2)
    vehicle.penup()

    start_u = path_nodes[0]
    sx, sy = gps_to_screen(graph.vertices[start_u]["coords"][0], graph.vertices[start_u]["coords"][1])
    vehicle.goto(sx, sy)
    screen.tracer(1)  # Turn on smooth animation

    for next_node in path_nodes[1:]:
        nx, ny = gps_to_screen(graph.vertices[next_node]["coords"][0], graph.vertices[next_node]["coords"][1])
        vehicle.setheading(vehicle.towards(nx, ny))
        vehicle.goto(nx, ny)
        time.sleep(0.3)

    # Flash arrival message
    pen.penup()
    pen.goto(-120, -260)
    pen.color("#10b981")
    pen.write(f"✅ {vehicle_obj.vehicle_id} ARRIVED AT SITE IN {eta_mins} MINS!", font=("Arial", 11, "bold"))

    print("\n[TURTLE SIMULATOR] Simulation completed. Click on the Turtle window or close it to return to menu.")
    try:
        screen.mainloop()
    except Exception:
        pass
