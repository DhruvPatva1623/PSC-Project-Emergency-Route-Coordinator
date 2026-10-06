"""
core/entity.py
==============
TOPIC USED:
- Object-Oriented Programming (OOP): Classes, Object Instantiation
- Encapsulation & Data Hiding: Private attributes (_available_beds, _operational_status) and @property getters/setters
- Structured Data Types: Tuples for geographic coordinates (lat, lng), Sets for facility tags

WHERE IT CONNECTS:
- Connected to 'gui.py' & 'run.py' for emergency alert tickets, fleet tracking, and hospital capacity management.
- Connected to 'core/router.py' for filtering idle vehicles and matching hospital locations.
"""

from datetime import datetime


class MedicalCenter:
    """
    TOPIC: OOP Encapsulation
    Represents a hospital / emergency medical center with bed capacity validation.
    """
    def __init__(self, center_id: str, title: str, latitude: float, longitude: float, available_beds: int):
        self.center_id = center_id
        self.title = title
        # Structured Type: Tuple for coordinate immutability
        self.position = (latitude, longitude)
        # Encapsulated attribute: Protected bed count
        self._available_beds = available_beds
        # Structured Type: Set for distinct medical facilities
        self.facilities = {"Emergency Ward", "ICU", "Burn Care", "Surgical Theater"}

    @property
    def available_beds(self) -> int:
        """Getter for protected bed count."""
        return self._available_beds

    @available_beds.setter
    def available_beds(self, count: int) -> None:
        """Setter with validation to prevent negative values."""
        if count >= 0:
            self._available_beds = count
        else:
            raise ValueError("Bed count cannot be negative.")

    def admit_emergency_case(self) -> bool:
        """Decrements bed count upon admitting a patient."""
        if self._available_beds > 0:
            self._available_beds -= 1
            return True
        return False


class RescueVehicle:
    """
    TOPIC: OOP Encapsulation & State Management
    Represents an emergency rescue unit (Ambulance, Fire Engine, Police Cruiser).
    """
    def __init__(self, vehicle_id: str, vehicle_type: str, current_station: str, 
                 latitude: float, longitude: float, cruising_speed_kmh: float = 60.0):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.current_station = current_station
        self.latitude = latitude
        self.longitude = longitude
        self.cruising_speed_kmh = cruising_speed_kmh
        # Encapsulated state: AVAILABLE or DISPATCHED
        self._operational_status = "AVAILABLE"

    @property
    def operational_status(self) -> str:
        return self._operational_status

    def deploy_to_site(self) -> None:
        self._operational_status = "DISPATCHED"

    def mark_available(self) -> None:
        self._operational_status = "AVAILABLE"


class EmergencyAlert:
    """
    TOPIC: OOP Structured Incident Model
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
