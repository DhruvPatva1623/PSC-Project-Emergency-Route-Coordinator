"""
core/entity.py
==============
Object-Oriented Programming (OOP) module defining core emergency entities.
Demonstrates:
- Classes and Objects
- Encapsulation & Information Hiding (Protected fields & @property setters)
- Structured Objects (Tuples for coordinates, Sets for capabilities)
(Syllabus: UNIT-I Structured Objects & UNIT-II Object-Oriented Programming)
"""

from datetime import datetime


class MedicalCenter:
    """
    Represents a Hospital or Trauma Center.
    Demonstrates Encapsulation: bed capacity cannot be manipulated directly without validation.
    """
    def __init__(self, center_id: str, title: str, latitude: float, longitude: float, available_beds: int):
        self.center_id = center_id
        self.title = title
        # [UNIT-I: Tuple for geographic coordinates]
        self.position = (latitude, longitude)
        # [UNIT-II: Encapsulated attribute]
        self._available_beds = available_beds
        # [UNIT-I: Set for distinct medical facilities]
        self.facilities = {"Emergency Ward", "ICU", "Burn Care", "Surgical Theater"}

    @property
    def available_beds(self) -> int:
        """Getter for protected bed count."""
        return self._available_beds

    @available_beds.setter
    def available_beds(self, count: int) -> None:
        """Setter with validation logic."""
        if count >= 0:
            self._available_beds = count
        else:
            raise ValueError("Bed count cannot be negative.")

    def admit_emergency_case(self) -> bool:
        """Reduces one available bed upon patient admission."""
        if self._available_beds > 0:
            self._available_beds -= 1
            return True
        return False


class RescueVehicle:
    """
    Represents an emergency response vehicle (Ambulance, Fire Engine, Police Cruiser).
    """
    def __init__(self, vehicle_id: str, vehicle_type: str, current_station: str, 
                 latitude: float, longitude: float, cruising_speed_kmh: float = 60.0):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.current_station = current_station
        self.latitude = latitude
        self.longitude = longitude
        self.cruising_speed_kmh = cruising_speed_kmh
        # [UNIT-II: Encapsulated operational state]
        self._operational_status = "AVAILABLE"  # "AVAILABLE", "DISPATCHED"

    @property
    def operational_status(self) -> str:
        return self._operational_status

    def deploy_to_site(self) -> None:
        self._operational_status = "DISPATCHED"

    def mark_available(self) -> None:
        self._operational_status = "AVAILABLE"


class EmergencyAlert:
    """
    Represents an incoming emergency distress call ticket.
    """
    def __init__(self, alert_id: str, citizen_name: str, phone_number: str, 
                 hazard_type: str, urgency: str, landmark_node: str, 
                 lat: float, lng: float):
        self.alert_id = alert_id
        self.citizen_name = citizen_name
        self.phone_number = phone_number
        self.hazard_type = hazard_type
        self.urgency = urgency
        self.landmark_node = landmark_node
        self.coords = (lat, lng)
        self.timestamp = datetime.now()
        self.allocated_vehicle = None
        self.allocated_center = None
