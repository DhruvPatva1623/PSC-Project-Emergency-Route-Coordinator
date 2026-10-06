# Emergency Route & Help Coordinator

A pure Python desktop project that coordinates emergency dispatches using **Tkinter Desktop GUI**, **Python Turtle Graphics Simulation**, **Dijkstra's Shortest Path Algorithm**, **Regex Validation**, **File I/O Logging**, and **NumPy/Matplotlib Analytics**.

---

## Project Structure

```text
psc_project_antigravity/
├── gui.py           # Tkinter Desktop GUI (8 Action Buttons + Distress Form)
├── run.py           # Primary Entry Point / Terminal Coordinator
├── core/
│  ├── entity.py        # OOP Classes (MedicalCenter, RescueVehicle, EmergencyAlert)
│  ├── router.py        # Dijkstra Algorithm, Graph Corridors & Higher-Order Functions
│  ├── turtle_visualizer.py  # Python Turtle Graphics Screen & Route Animation
│  ├── validator.py      # Phone Regex Validation & Persistent File Logging
│  └── visualizer.py      # NumPy Statistical Computing & Matplotlib Curves
│
├── data/
│  ├── emergency_records.txt  # Persistent distress incident logs
│  └── performance_curve.png  # Matplotlib response benchmark curve
│
└── README.md          # Documentation
```

---

## How to Run

### 1. Run Desktop Tkinter GUI (Recommended)
```bash
python gui.py
```
Opens the classic desktop window with:
- **1. Report Emergency**: Fill caller name, phone number, location, and emergency type (`Crime`, `Medical`, `Fire`, `Accident`).
- **2. Find Emergency Route**: Calculates shortest path corridor with distance & ETA.
- **3. View Available Help**: Lists all rescue vehicles and hospital bed counts.
- **4. Assign Help**: Dispatches the nearest available unit and admits case to hospital.
- **5. View Emergency Records**: Displays all saved records from `data/emergency_records.txt`.
- **6. Start Emergency Monitoring**: Starts background tracking simulation.
- **7. Show Emergency Map (Turtle)**: Opens Python Turtle to animate the vehicle on the road network.
- **8. Exit**: Closes application.

### 2. Run Main Terminal Coordinator
```bash
python run.py
```
Provides an interactive menu to launch the Tkinter GUI, run Turtle simulations directly, view incident records, or generate response curves.

---

## Pure Python Syllabus Mapping

| Module | Core Concepts Used |
| :--- | :--- |
| **`gui.py`** | Tkinter GUI, Event Handlers, Input Validation, Modals, Multithreading |
| **`core/turtle_visualizer.py`** | Python Turtle graphics, coordinate translation, screen animation |
| **`core/entity.py`** | Classes, Encapsulation, `@property` getters/setters, Structured Types (Tuples, Sets) |
| **`core/router.py`** | Dijkstra's Algorithm, Graph Adjacency, Higher-order functions (`filter`, `sorted`, `lambda`) |
| **`core/validator.py`** | Regular Expressions (`^[6-9]\d{9}$`), Persistent File I/O (`open()`, read/write) |
| **`core/visualizer.py`** | NumPy 1D/2D array stats (Mean, Median, $\sigma$, Matrix Efficiency), Matplotlib polynomial curve |
