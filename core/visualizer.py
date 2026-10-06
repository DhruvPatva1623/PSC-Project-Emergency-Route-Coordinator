"""
core/visualizer.py
==================
Visualization, Array Computing, and Leaflet Map Generation module.
Demonstrates:
- NumPy 1D and 2D Array computing
- Matplotlib response time trend curve plotting
- Dynamic Leaflet HTML Interactive Map generation
(Syllabus: UNIT-III Array Computing, Curve Plotting & Visual Presentation)
"""

import os
import webbrowser
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def compute_fleet_statistics(response_intervals: list) -> dict:
    """
    [UNIT-III: NumPy Vector & Matrix Operations]
    Computes statistical evaluation using NumPy vectors and matrices.
    """
    if not response_intervals:
        response_intervals = [7.5, 9.2, 5.8, 12.1, 8.4, 6.6, 10.5]

    num_array = np.array(response_intervals, dtype=np.float64)

    mean_duration = float(np.mean(num_array))
    median_duration = float(np.median(num_array))
    std_deviation = float(np.std(num_array))
    fastest_time = float(np.min(num_array))
    longest_time = float(np.max(num_array))

    speed_vector = 60.0 / (num_array / 60.0 + 0.1)
    stats_matrix = np.column_stack((num_array, speed_vector))
    efficiency_index = float(np.mean(stats_matrix[:, 1]) / mean_duration)

    return {
        "count": len(response_intervals),
        "mean_min": round(mean_duration, 2),
        "median_min": round(median_duration, 2),
        "std_dev": round(std_deviation, 2),
        "min_min": round(fastest_time, 2),
        "max_min": round(longest_time, 2),
        "efficiency": round(efficiency_index, 2)
    }


def render_trend_curve(response_times: list, save_file: str = "data/performance_curve.png") -> str:
    """
    [UNIT-III: Matplotlib Curve Plotting]
    Plots polynomial trend curve of emergency response times.
    """
    os.makedirs(os.path.dirname(save_file), exist_ok=True)
    if not response_times or len(response_times) < 2:
        response_times = [7.2, 11.5, 5.8, 9.4, 14.1, 6.3, 10.2, 8.0]

    labels = [f"Case-{i+1}" for i in range(len(response_times))]
    actual_values = np.array(response_times)
    standard_target = np.full(len(response_times), 8.0)

    plt.figure(figsize=(8.5, 4.4), facecolor="#0f172a")
    ax = plt.subplot(1, 1, 1)
    ax.set_facecolor("#1e293b")

    x_indices = np.arange(len(labels))
    bar_width = 0.35

    ax.bar(x_indices - bar_width/2, actual_values, bar_width, label='Actual Time (min)', color='#38bdf8', alpha=0.9)
    ax.bar(x_indices + bar_width/2, standard_target, bar_width, label='Target Benchmark (8 min)', color='#f43f5e', alpha=0.7)

    smooth_x = np.linspace(0, len(labels)-1, 50)
    polynomial_weights = np.polyfit(x_indices, actual_values, 2)
    smooth_y = np.polyval(polynomial_weights, smooth_x)
    ax.plot(smooth_x, smooth_y, color='#fbbf24', linestyle='--', linewidth=2, label='Polynomial Response Curve')

    ax.set_title("Emergency Response Dispatch Curve (UNIT-III)", color="#f8fafc", fontsize=12, fontweight='bold', pad=10)
    ax.set_xlabel("Incident Sequence", color="#94a3b8", fontsize=10)
    ax.set_ylabel("Response Time (Minutes)", color="#94a3b8", fontsize=10)
    ax.set_xticks(x_indices)
    ax.set_xticklabels(labels, color="#cbd5e1", fontsize=9)
    ax.tick_params(colors="#cbd5e1")
    ax.grid(color="#334155", linestyle=":", alpha=0.6)

    legend = ax.legend(facecolor="#1e293b", edgecolor="#334155")
    for text_elem in legend.get_texts():
        text_elem.set_color("#f8fafc")

    plt.tight_layout()
    plt.savefig(save_file, dpi=120, bbox_inches='tight')
    plt.close()
    return save_file


def generate_interactive_map_html(incident_label: str, incident_coords: tuple, 
                                  vehicle_obj, medical_center, route_points: list, 
                                  eta_minutes: float, total_km: float, 
                                  output_file: str = "web/emergency_map.html") -> str:
    """
    [UNIT-III: Interactive Leaflet Map Visuals]
    Generates a full visual screen with map and interactive on-screen controls.
    """
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
    render_trend_curve([7.5, 8.2, 5.9, 11.0, 9.4, 6.7, eta_minutes])

    html_markup = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emergency Route & Help Coordinator</title>
    
    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }}
        body {{ background: #0b0f19; color: #f8fafc; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}
        
        /* Top Navigation Header */
        header {{
            background: #0f172a;
            padding: 10px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 1000;
        }}
        .brand {{ display: flex; align-items: center; gap: 10px; }}
        .brand-icon {{ font-size: 26px; background: rgba(239, 68, 68, 0.2); padding: 4px 8px; border-radius: 8px; border: 1px solid rgba(239, 68, 68, 0.4); }}
        .brand h1 {{ font-size: 1.15rem; font-weight: 700; }}
        .brand p {{ font-size: 0.75rem; color: #94a3b8; }}

        .nav-actions {{ display: flex; gap: 8px; }}
        .btn {{
            background: #1e293b;
            color: #f8fafc;
            border: 1px solid rgba(255,255,255,0.15);
            padding: 7px 14px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .btn:hover {{ background: #334155; border-color: #38bdf8; }}
        .btn-red {{ background: #dc2626; border-color: #ef4444; color: white; }}
        .btn-red:hover {{ background: #ef4444; }}

        /* Main Workspace */
        .workspace {{ display: grid; grid-template-columns: 360px 1fr; flex: 1; height: calc(100vh - 60px); }}
        
        /* Left Control Panel */
        .sidebar {{
            background: #131b2e;
            border-right: 1px solid rgba(255,255,255,0.1);
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            overflow-y: auto;
        }}
        .card {{
            background: #182238;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 10px;
            padding: 14px;
        }}
        .card h3 {{ font-size: 0.92rem; margin-bottom: 8px; color: #f8fafc; display: flex; justify-content: space-between; align-items: center; }}
        
        .stat-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }}
        .stat-box {{ background: #0f172a; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid rgba(255,255,255,0.05); }}
        .stat-box small {{ font-size: 0.7rem; color: #94a3b8; display: block; }}
        .stat-box strong {{ font-size: 1.15rem; color: #38bdf8; }}

        .form-group {{ margin-bottom: 8px; }}
        label {{ display: block; font-size: 0.74rem; color: #94a3b8; margin-bottom: 3px; font-weight: 600; }}
        select, input {{
            width: 100%;
            background: #0f172a;
            border: 1px solid rgba(255,255,255,0.15);
            color: #ffffff;
            padding: 8px 10px;
            border-radius: 6px;
            font-size: 0.82rem;
            outline: none;
        }}
        select:focus, input:focus {{ border-color: #38bdf8; }}

        /* Right Map View */
        #map {{ width: 100%; height: 100%; background: #1e293b; }}
        
        /* Map Legend */
        .map-legend {{
            position: absolute;
            bottom: 16px;
            right: 16px;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(8px);
            padding: 8px 14px;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            z-index: 1000;
            font-size: 0.75rem;
            display: flex;
            gap: 12px;
        }}
        .dot {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 4px; }}
        .dot-amb {{ background: #10b981; }}
        .dot-hosp {{ background: #0284c7; }}
        .dot-inc {{ background: #ef4444; }}

        /* Analytics Modal */
        #analytics-modal {{
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(6px);
            z-index: 2000;
            align-items: center;
            justify-content: center;
        }}
        .modal-body {{
            background: #0f172a;
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 12px;
            padding: 20px;
            max-width: 750px;
            width: 90%;
            text-align: center;
        }}
    </style>
</head>
<body>

    <!-- Top Header -->
    <header>
        <div class="brand">
            <div class="brand-icon">🚨</div>
            <div>
                <h1>Emergency Route & Help Coordinator</h1>
                <p>Indus University • Live OpenStreetMap (OSRM) & Dijkstra Routing</p>
            </div>
        </div>

        <div class="nav-actions">
            <button class="btn" onclick="presetDestination([23.0560, 72.4860], 'Indus University Campus')">🏫 Indus Univ</button>
            <button class="btn" onclick="presetDestination([23.0786, 72.5290], 'Sola Civil Hospital')">🏥 Sola Civil</button>
            <button class="btn" onclick="presetDestination([23.0504, 72.5168], 'Thaltej Cross Roads')">📍 Thaltej</button>
            <button class="btn" onclick="openAnalyticsModal()">📊 NumPy/Matplotlib Analytics</button>
        </div>
    </header>

    <!-- Workspace Layout -->
    <div class="workspace">
        
        <!-- Left Sidebar Controls -->
        <aside class="sidebar">
            <div class="card" style="border-color: rgba(56, 189, 248, 0.3);">
                <h3>📍 Live Corridor Status</h3>
                <div class="stat-grid">
                    <div class="stat-box">
                        <small>Travel ETA</small>
                        <strong id="stat-time">{eta_minutes} min</strong>
                    </div>
                    <div class="stat-box">
                        <small>Road Distance</small>
                        <strong id="stat-dist">{total_km} km</strong>
                    </div>
                </div>
                <div style="font-size:0.78rem; margin-top:10px; color:#cbd5e1; line-height:1.6;">
                    <p><strong>Emergency Spot:</strong> <span id="lbl-loc">{incident_label}</span></p>
                    <p><strong>Assigned Unit:</strong> {vehicle_obj.vehicle_id} ({vehicle_obj.vehicle_type})</p>
                    <p><strong>Target Hospital:</strong> {medical_center.title} ({medical_center.available_beds} beds)</p>
                </div>
            </div>

            <div class="card">
                <h3>⚡ Quick SOS Destination</h3>
                <div class="form-group">
                    <label>Choose Landmark Location</label>
                    <select id="select-place" onchange="onSelectChange()">
                        <option value="23.0504,72.5168">Thaltej Cross Roads</option>
                        <option value="23.0560,72.4860">Indus University Campus</option>
                        <option value="23.0786,72.5290">Sola Civil Hospital</option>
                        <option value="23.0350,72.5293">Vastrapur Lake</option>
                        <option value="23.0780,72.4980">Science City Circle</option>
                    </select>
                </div>
                <button class="btn btn-red" style="width:100%; margin-top:4px;" onclick="dispatchSelected()">
                    🚨 Dispatch Route (OSRM API)
                </button>
                <small style="display:block; text-align:center; color:#94a3b8; font-size:0.7rem; margin-top:6px;">
                    💡 Tip: Click anywhere on the map to set a custom emergency location!
                </small>
            </div>

            <div class="card">
                <h3>🏥 Available Hospitals</h3>
                <div style="font-size:0.78rem; line-height:1.7; color:#94a3b8;">
                    <div>🏥 <b>Sola Civil Hospital</b> (14 ICU Beds)</div>
                    <div>🏥 <b>Zydus Multi-Speciality</b> (8 ICU Beds)</div>
                    <div>🏥 <b>Sterling Emergency Care</b> (5 ICU Beds)</div>
                </div>
            </div>
        </aside>

        <!-- Right Leaflet Map -->
        <main style="position:relative; width:100%; height:100%;">
            <div id="map"></div>
            
            <div class="map-legend">
                <span><span class="dot dot-amb"></span> Ambulance AMB-101</span>
                <span><span class="dot dot-hosp"></span> Hospital</span>
                <span><span class="dot dot-inc"></span> Incident Spot</span>
            </div>
        </main>
    </div>

    <!-- Analytics Modal -->
    <div id="analytics-modal" onclick="closeAnalyticsModal()">
        <div class="modal-body" onclick="event.stopPropagation()">
            <h2 style="font-size:1.15rem; margin-bottom:8px;">📊 Matplotlib Response Time Curve (UNIT-III)</h2>
            <img src="data/performance_curve.png" alt="Response Curve" style="max-width:100%; border-radius:8px; margin:10px 0;">
            <button class="btn btn-red" onclick="closeAnalyticsModal()">✕ Close Window</button>
        </div>
    </div>

    <!-- Map Logic -->
    <script>
        // 1. Initialize Map
        const map = L.map('map').setView([{incident_coords[0]}, {incident_coords[1]}], 13);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap | Indus University Project'
        }}).addTo(map);

        const ambCoords = [{vehicle_obj.latitude}, {vehicle_obj.longitude}];

        // 2. Ambulance Marker
        const ambIcon = L.divIcon({{
            html: '<div style="background:#10b981; color:white; border-radius:50%; width:32px; height:32px; display:flex; align-items:center; justify-content:center; font-size:16px; border:2px solid white; box-shadow:0 0 10px #10b981;">🚑</div>',
            iconSize: [32, 32], iconAnchor: [16, 16]
        }});
        L.marker(ambCoords, {{ icon: ambIcon }}).addTo(map).bindPopup("<b>Unit: {vehicle_obj.vehicle_id}</b><br>Station: {vehicle_obj.current_station}");

        // 3. Hospital Markers
        const hospIcon = L.divIcon({{
            html: '<div style="background:#0284c7; color:white; border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; font-size:14px; border:2px solid white; box-shadow:0 0 8px #0284c7;">🏥</div>',
            iconSize: [28, 28], iconAnchor: [14, 14]
        }});
        L.marker([{medical_center.position[0]}, {medical_center.position[1]}], {{ icon: hospIcon }}).addTo(map).bindPopup("<b>{medical_center.title}</b><br>Available Beds: {medical_center.available_beds}");

        // 4. Initial Incident Marker & Route
        let incMarker = null;
        let routeLine = null;

        function setIncidentRoute(coords, labelName = "Emergency Spot") {{
            if (incMarker) map.removeLayer(incMarker);
            if (routeLine) map.removeLayer(routeLine);

            const incIcon = L.divIcon({{
                html: '<div style="background:#ef4444; color:white; border-radius:50%; width:30px; height:30px; display:flex; align-items:center; justify-content:center; font-size:15px; border:2px solid white; box-shadow:0 0 12px #ef4444;">🚨</div>',
                iconSize: [30, 30], iconAnchor: [15, 15]
            }});
            incMarker = L.marker(coords, {{ icon: incIcon }}).addTo(map).bindPopup("<b>" + labelName + "</b>").openPopup();

            // Fetch live OSRM route
            const osrmUrl = "https://router.project-osrm.org/route/v1/driving/" + ambCoords[1] + "," + ambCoords[0] + ";" + coords[1] + "," + coords[0] + "?overview=full&geometries=geojson";
            
            fetch(osrmUrl)
                .then(res => res.json())
                .then(data => {{
                    if (data.code === 'Ok' && data.routes.length > 0) {{
                        const r = data.routes[0];
                        const distKm = (r.distance / 1000).toFixed(2);
                        const timeMin = (r.duration / 60).toFixed(1);
                        const pts = r.geometry.coordinates.map(p => [p[1], p[0]]);

                        routeLine = L.polyline(pts, {{ color: '#ef4444', weight: 6, opacity: 0.9 }}).addTo(map);
                        map.fitBounds(routeLine.getBounds(), {{ padding: [50, 50] }});

                        document.getElementById('stat-time').innerText = timeMin + " min";
                        document.getElementById('stat-dist').innerText = distKm + " km";
                        document.getElementById('lbl-loc').innerText = labelName;
                    }}
                }})
                .catch(() => {{
                    // Direct line fallback
                    routeLine = L.polyline([ambCoords, coords], {{ color: '#ef4444', weight: 5, dashArray: '6, 6' }}).addTo(map);
                }});
        }}

        // Set initial route
        setIncidentRoute([{incident_coords[0]}, {incident_coords[1]}], "{incident_label}");

        // Map Click Event: Click anywhere to route ambulance
        map.on('click', function(e) {{
            setIncidentRoute([e.latlng.lat, e.latlng.lng], "Custom Emergency Coordinates");
        }});

        function presetDestination(coords, name) {{
            setIncidentRoute(coords, name);
        }}

        function dispatchSelected() {{
            const val = document.getElementById('select-place').value.split(',').map(Number);
            const selText = document.getElementById('select-place').selectedOptions[0].text;
            setIncidentRoute(val, selText);
        }}

        function onSelectChange() {{
            dispatchSelected();
        }}

        function openAnalyticsModal() {{
            document.getElementById('analytics-modal').style.display = 'flex';
        }}

        function closeAnalyticsModal() {{
            document.getElementById('analytics-modal').style.display = 'none';
        }}
    </script>
</body>
</html>"""

    with open(output_file, "w", encoding="utf-8") as file_out:
        file_out.write(html_markup)

    abs_path = os.path.abspath(output_file)
    webbrowser.open(f"file:///{abs_path}")
    return abs_path
