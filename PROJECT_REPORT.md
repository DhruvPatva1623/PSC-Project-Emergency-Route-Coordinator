# Emergency Route & Help Coordinator
## Comprehensive Project Report & Technical Overview

---

## 1. Abstract & Project Overview

The **Emergency Route and Help Coordinator** is a desktop software application designed to optimize emergency dispatch operations across a municipal road network. During distress events (medical emergencies, fire hazards, or law enforcement calls), rapid resource allocation and shortest-path routing are critical to saving lives.

This project simulates a city dispatch center by:
1. Receiving citizen distress calls via a **Tkinter Desktop GUI**.
2. Validating input data (such as 10-digit phone numbers) using **Regular Expressions**.
3. Filtering available emergency response units (Ambulances, Fire Engines, Police Patrols) using **Higher-Order Functions and Lambdas**.
4. Finding the fastest path across road corridors using **Dijkstra's Shortest Path Algorithm**.
5. Assigning the nearest medical trauma center with available bed capacity.
6. Recording all incident logs persistently in **Plain Text Storage**.
7. Rendering a 2D interactive road corridor simulation using standard **Python Turtle Graphics**.
8. Computing statistical dispatch performance metrics using **NumPy** and plotting polynomial response trends using **Matplotlib**.

---

## 2. Technology Stack & Prerequisites

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10+ | Core programming logic, data structures, and algorithms |
| **Desktop GUI** | Tkinter (`tkinter`, `ttk`, `messagebox`) | Main desktop interactive windows, distress entry forms, and modals |
| **Simulation** | Python Turtle (`turtle`) | 2D vector animation of road corridors, landmarks, and rescue vehicles |
| **Routing Algorithm**| Priority Queue Min-Heap (`heapq`) | Dijkstra's shortest path computation based on distance and corridor speed |
| **Data Validation** | Regular Expressions (`re`) | Phone number format and ticket tag pattern matching |
| **Persistence** | File Handling (`open()`, Context Managers) | Plain text logging (`data/emergency_records.txt`) |
| **Data Analytics** | NumPy (`numpy`) | Vectorized mean, median, standard deviation, and matrix efficiency scoring |
| **Data Visualization**| Matplotlib (`matplotlib.pyplot`) | Polynomial trend curve plotting (`data/performance_curve.png`) |

---

## 3. Core Python Syllabus Concepts & Code Mapping

```
+--------------------------------------------------------------------------------------------------+
|                                    SYLLABUS TOPIC MAPPING                                        |
+--------------------------+----------------------------------------+------------------------------+
| Concept / Topic          | Where It Is Implemented                | Functional Application       |
+--------------------------+----------------------------------------+------------------------------+
| Structured Types         | core/entity.py, core/router.py         | Tuples, Sets, Dictionaries   |
| Higher-Order Functions   | core/router.py                         | filter(), sorted(), map()    |
| Recursion                | core/router.py (_trace_route_recursive)| Shortest path reconstruction |
| File Handling (I/O)      | core/validator.py                      | Persistent log append/read   |
| OOP & Encapsulation      | core/entity.py                         | Classes, @property setters   |
| Regular Expressions      | core/validator.py                      | Regex phone & tag checks     |
| Array Computing (NumPy)  | core/visualizer.py                     | 1D/2D statistical matrices   |
| Curve Plotting (Matplot) | core/visualizer.py                     | Polynomial regression chart  |
| GUI & Graphics (Tkinter) | gui.py, core/turtle_visualizer.py      | Windows & Turtle animation   |
+--------------------------+----------------------------------------+------------------------------+
```

### Detailed Concept Breakdown:

1. **Structured Data Types (Unit-I)**:
   - **Tuples**: Used in `MedicalCenter.position = (lat, lng)` and `graph.vertices` to ensure coordinate immutability.
   - **Sets**: Used in `MedicalCenter.facilities = {"Emergency Ward", "ICU", ...}` and `graph.roadblocks` for fast lookups.
   - **Dictionaries**: Used for graph vertices and network adjacency lists.

2. **Higher-Order Functions & Lambda Expressions (Unit-I)**:
   - `filter_idle_fleet()` uses `filter(lambda v: v.operational_status == "AVAILABLE", vehicles)` to identify ready vehicles.
   - `locate_nearest_medical_center()` uses `sorted(centers, key=lambda c: euclidean_distance(c))` to match the closest hospital.
   - `extract_waypoint_positions()` uses `map(lambda k: graph.vertices[k]["coords"], path)` to extract GPS points.

3. **Recursion (Unit-I)**:
   - `_trace_route_recursive()` in `core/router.py` backtracks parent pointers from the destination node to the starting intersection recursively without standard while-loops.

4. **File Handling & Persistence (Unit-I)**:
   - `append_record_to_file()` in `core/validator.py` writes distress call records in append mode (`mode="a"`).
   - `fetch_all_records()` reads records line by line (`mode="r"`) using Python context managers (`with open`).

5. **Object-Oriented Programming & Encapsulation (Unit-II)**:
   - `MedicalCenter`, `RescueVehicle`, and `EmergencyAlert` classes encapsulate sensitive fields (`_available_beds`, `_operational_status`).
   - Bed counts and vehicle states are controlled using `@property` getters and setters with validation logic.

6. **Regular Expressions (Unit-II)**:
   - `check_phone_format()` enforces Indian 10-digit mobile numbers starting with 6, 7, 8, or 9: `^[6-9]\d{9}$`.
   - `check_emergency_tag()` verifies structured tags like `SOS-101` or `E-1`: `^[A-Z]{1,4}-\d{1,4}$`.

7. **NumPy Vector & Matrix Computing (Unit-III)**:
   - `compute_fleet_statistics()` converts response times to a `numpy.ndarray` to calculate mean, median, standard deviation (`np.std`), min, max, and a 2D matrix efficiency score.

8. **Matplotlib Response Curve Plotting (Unit-III)**:
   - `render_trend_curve()` uses `matplotlib.pyplot` to draw bar benchmarks against an 8-minute standard and applies 2nd-degree polynomial fitting (`np.polyfit`, `np.polyval`) to plot trend curves.

9. **Tkinter Desktop GUI & Python Turtle Simulation (Unit-III)**:
   - `gui.py` uses `tk.Tk`, `tk.Toplevel`, `ttk.Combobox`, and `messagebox` to deliver an 8-button menu.
   - `core/turtle_visualizer.py` sets up a 2D coordinate system, draws city roads, and moves the vehicle sprite along the route.

---

## 4. System Architecture & File Structure

```text
psc_project_antigravity/
│
├── gui.py                      # Desktop Tkinter GUI (Primary user application)
├── run.py                      # Main Python CLI coordinator & terminal menu
├── README.md                   # Setup guide and reference manual
│
├── core/                       # Core Python Backend Modules
│   ├── entity.py               # OOP Classes (MedicalCenter, RescueVehicle, EmergencyAlert)
│   ├── router.py               # Graph Network, Dijkstra Engine, Recursion, Lambdas
│   ├── turtle_visualizer.py    # Python Turtle Screen, Road Drawing & Animation
│   ├── validator.py            # Phone Regex Validation & Plain Text File I/O
│   └── visualizer.py           # NumPy Statistical Analytics & Matplotlib Curves
│
└── data/                       # Persistent Data Storage
    ├── emergency_records.txt   # Appended distress incident logs
    └── performance_curve.png   # Generated Matplotlib performance chart
```

---

## 5. System Workflow & Flowchart

```mermaid
flowchart TD
    Start([User Launches gui.py / run.py]) --> Menu[Main Selection Menu]
    
    Menu -->|Action 1| Report[1. Report Emergency]
    Menu -->|Action 2| Route[2. Find Emergency Route]
    Menu -->|Action 3| ViewHelp[3. View Available Help]
    Menu -->|Action 4| Assign[4. Assign Help]
    Menu -->|Action 5| Logs[5. View Emergency Records]
    Menu -->|Action 6| Monitor[6. Start Emergency Monitoring]
    Menu -->|Action 7| TurtleMap[7. Show Emergency Map - Turtle]
    Menu -->|Action 8| Exit([8. Exit Application])

    Report --> InputData[/Input Name, Phone, Location, Hazard Type/]
    InputData --> ValidatePhone{Regex Check: ^[6-9]\\d{9}$}
    ValidatePhone -->|Invalid| ErrorMsg[Show Validation Error Popup] --> InputData
    ValidatePhone -->|Valid| GenTag[Generate Ticket Tag e.g., E-1]
    GenTag --> SaveFile[(Append to data/emergency_records.txt)]
    SaveFile --> SuccessPopup[Show Confirmation Popup: Emergency Reported]
    SuccessPopup --> Menu

    Route --> Dijkstra[Run Dijkstra Algorithm on Graph Network]
    Dijkstra --> CalcTime[Compute Distance km and Travel Time min]
    CalcTime --> TraceRoute[Recursive Path Reconstruction _trace_route_recursive]
    TraceRoute --> DisplayRoute[Display Shortest Path Corridors]
    DisplayRoute --> Menu

    Assign --> FilterVehicles[Filter Idle Fleet using filter & lambda]
    FilterVehicles --> MatchHospital[Locate Nearest Bed using sorted & Euclidean gap]
    MatchHospital --> UpdateState[Set Vehicle to DISPATCHED & Bed Count - 1]
    UpdateState --> Menu

    TurtleMap --> InitScreen[Setup Turtle 2D Coordinate Screen]
    InitScreen --> DrawRoads[Draw Corridors & Landmark Nodes]
    DrawRoads --> MarkHospital[Draw Hospital & Incident Markers]
    MarkHospital --> Animate[Animate Vehicle Sprite along Shortest Path]
    Animate --> Menu
```

---

## 6. Detailed Module Breakdown

### 6.1 `core/entity.py` (Object-Oriented Programming)
- **`MedicalCenter`**: Models hospitals with protected `_available_beds`. Provides setter validation and `admit_emergency_case()` method.
- **`RescueVehicle`**: Models response fleet (Ambulances, Fire Engines, Patrol Cruisers) with protected `_operational_status` ("AVAILABLE" / "DISPATCHED").
- **`EmergencyAlert`**: Stores timestamped distress tickets with citizen details and assigned resources.

### 6.2 `core/router.py` (Dijkstra Routing & Algorithms)
- **`UrbanCorridorGraph`**: Graph with vertices (landmarks with latitude/longitude) and weighted edges (corridor distance & cruising speed).
- **`find_fastest_corridor(start, end)`**: Implements Dijkstra's algorithm with `heapq` priority queue to minimize travel time:
  $$\text{Corridor Time (min)} = \left(\frac{\text{Distance (km)}}{\text{Speed (km/h)}}\right) \times 60$$
- **`_trace_route_recursive(parent_map, target)`**: Reconstructs the complete route path using pure recursion.
- **Higher-Order Functions**: `filter_idle_fleet()`, `locate_nearest_medical_center()`, `extract_waypoint_positions()`.

### 6.3 `core/validator.py` (Regex & File I/O)
- **`check_phone_format(phone)`**: Validates phone numbers using `re.match(r"^[6-9]\d{9}$", phone)`.
- **`append_record_to_file(...)`**: Logs each incident to `data/emergency_records.txt` in append mode (`"a"`).
- **`fetch_all_records()`**: Reads all logged records in read mode (`"r"`).

### 6.4 `core/visualizer.py` (NumPy & Matplotlib)
- **`compute_fleet_statistics(durations)`**: Calculates Mean, Median, $\sigma$, Min, Max, and a 2D Matrix Efficiency Score using NumPy.
- **`render_trend_curve(durations)`**: Plots a styled bar chart comparing actual response times against an 8-minute target and overlays a 2nd-degree polynomial curve (`np.polyfit`).

### 6.5 `core/turtle_visualizer.py` (Turtle Animation)
- **`gps_to_screen(lat, lng)`**: Converts real GPS coordinates into screen pixel coordinates $(x, y)$.
- **`draw_turtle_simulation(...)`**: Draws the city network in dark theme, marks incident and hospital spots, and animates a vehicle moving node-by-node along the computed path.

### 6.6 `gui.py` (Desktop Tkinter GUI)
- Implements an 8-button dashboard window matching desktop application standards:
  1. *Report Emergency*
  2. *Find Emergency Route*
  3. *View Available Help*
  4. *Assign Help*
  5. *View Emergency Records*
  6. *Start Emergency Monitoring*
  7. *Show Emergency Map (Turtle)*
  8. *Exit*

---

## 7. Execution Instructions

### Running the Desktop GUI:
```bash
python gui.py
```

### Running the Terminal Coordinator:
```bash
python run.py
```

---

## 8. GitHub Repository Link
- **Repository URL**: [https://github.com/DhruvPatva1623/PSC-Project-Emergency-Route-Coordinator](https://github.com/DhruvPatva1623/PSC-Project-Emergency-Route-Coordinator)
