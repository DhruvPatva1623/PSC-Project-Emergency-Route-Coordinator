# 🚨 Emergency Route & Help Coordinator

A modular Python project that calculates optimal emergency dispatch routes using **Live OpenStreetMap (OSRM) API Routing** & **Dijkstra's Algorithm**, validates input with **Regular Expressions**, records incident logs in a **Plain Text File**, computes statistical metrics with **NumPy & Matplotlib**, and launches an interactive **Leaflet Map** in your web browser.

---

## 📂 Modular File Structure

```
psc_project_antigravity/
├── run.py                 # Primary entry point with interactive CLI menu
├── core/
│   ├── entity.py          # OOP Classes (MedicalCenter, RescueVehicle, EmergencyAlert) with Encapsulation
│   ├── router.py          # Live OpenStreetMap OSRM API, Dijkstra Routing, Recursion & Higher-Order Functions
│   ├── validator.py       # Regular Expressions (phone/tag checks) & Text File Logging
│   └── visualizer.py      # NumPy Array Computing, Matplotlib Curves & Leaflet Map Generator
│
├── data/
│   ├── emergency_records.txt  # Persistent plain text incident logs
│   └── performance_curve.png  # Matplotlib generated response time curve
│
└── README.md              # Complete documentation & viva cheat sheet
```

---

## 📚 Complete Syllabus Concept Mapping

| Syllabus Unit | Concept | Implementation File & Details |
| :--- | :--- | :--- |
| **UNIT - I** | **Structured Objects (Lists, Tuples, Dictionaries, Sets)** | • `core/entity.py`: Tuples for GPS positions `(lat, lng)`, Sets for medical capabilities `{"ICU", "Burn Care"}`<br>• `core/router.py`: Dictionaries for vertex tables and network adjacency |
| **UNIT - I** | **Higher-Order Functions & Lambdas** | • `core/router.py`: `filter()` for idle vehicles, `sorted()` with Euclidean lambda for closest hospital, `map()` for coordinate conversion |
| **UNIT - I** | **Recursion** | • `core/router.py`: `_trace_route_recursive()` recursively backtracks parent pointers from destination to origin |
| **UNIT - I** | **File Handling (Plain Text I/O)** | • `core/validator.py`: `append_record_to_file()` using `open(..., "a")` and `fetch_all_records()` using `open(..., "r")` to `data/emergency_records.txt` |
| **UNIT - II** | **Object-Oriented Programming & Encapsulation** | • `core/entity.py`: Classes `MedicalCenter`, `RescueVehicle`, `EmergencyAlert` with protected attributes `_available_beds`, `_operational_status` and `@property` getters/setters |
| **UNIT - II** | **Algorithms & OpenStreetMap API** | • `core/router.py`: **Live OpenStreetMap (OSRM) Driving API** fetching real-time road driving paths + **Dijkstra's Algorithm** fallback with `heapq` |
| **UNIT - II** | **Regular Expressions (Regex)** | • `core/validator.py`: `check_phone_format(phone)` using `re.match(r"^[6-9]\d{9}$", phone)` |
| **UNIT - III** | **Array Computing & Matrices (NumPy)** | • `core/visualizer.py`: 1D arrays for vector Mean, Median, Std Dev, and 2D matrix speed/time efficiency scoring |
| **UNIT - III** | **Curve Plotting (Matplotlib)** | • `core/visualizer.py`: `render_trend_curve()` plots polynomial response curves (`np.polyfit`) saved to `data/performance_curve.png` |
| **UNIT - III** | **Interactive Leaflet Map Visuals** | • `core/visualizer.py`: `generate_interactive_map_html()` generates `emergency_map.html` and launches it in your browser showing the Ambulance 🚑, Incident 🚨, Hospital 🏥, and the route corridor |

---

## 🚀 How to Run in VS Code

Run the main script in your VS Code terminal:
```bash
python run.py
```

### 🎯 Interactive Menu Options:
1. **Option 1**: Report an emergency, fetch real driving routes from the **Live OpenStreetMap API**, save to `data/emergency_records.txt`, and automatically open the interactive **Leaflet Map** in your browser.
2. **Option 2**: View all saved logs in `data/emergency_records.txt`.
3. **Option 3**: View NumPy statistical calculations and generate the Matplotlib response time curve (`data/performance_curve.png`).
4. **Option 4**: Exit the application.
