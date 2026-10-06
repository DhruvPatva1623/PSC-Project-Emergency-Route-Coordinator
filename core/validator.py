"""
core/validator.py
=================
TOPIC USED:
- Regular Expressions (re module): Pattern matching for 10-digit phone validation (^[6-9]\\d{9}$) and tag formats
- File Handling (I/O): Plain text append ('a') and read ('r') file operations with context managers (with open)

WHERE IT CONNECTS:
- Connected to 'gui.py' & 'run.py' to validate distress caller phone inputs before dispatch.
- Connected to 'gui.py' & 'run.py' for reading and displaying stored incident records from 'data/emergency_records.txt'.
"""

import re
import os
from datetime import datetime

STORAGE_PATH = os.path.join("data", "emergency_records.txt")


def check_phone_format(phone: str) -> bool:
    """
    TOPIC: Regular Expressions (Regex)
    Validates standard 10-digit mobile contact numbers (starts with 6-9).
    """
    regex_pattern = r"^[6-9]\d{9}$"
    return bool(re.match(regex_pattern, phone.strip()))


def check_emergency_tag(tag: str) -> bool:
    """
    TOPIC: Regular Expressions (Regex)
    Validates ticket tag formats (e.g., 'SOS-101', 'E-1').
    """
    regex_pattern = r"^[A-Z]{1,4}-\d{1,4}$"
    return bool(re.match(regex_pattern, tag.strip().upper()))


def append_record_to_file(alert_id: str, citizen: str, phone: str, 
                          hazard: str, priority: str, location: str) -> None:
    """
    TOPIC: File Handling (Write/Append Mode)
    Appends a new emergency record to the persistent log text file.
    """
    os.makedirs("data", exist_ok=True)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_line = (
        f"TAG: {alert_id} | DATE: {current_time} | CITIZEN: {citizen} | "
        f"PHONE: {phone} | HAZARD: {hazard} | PRIORITY: {priority} | LOCATION: {location}\n"
    )

    with open(STORAGE_PATH, mode="a", encoding="utf-8") as file_handle:
        file_handle.write(entry_line)


def fetch_all_records() -> list:
    """
    TOPIC: File Handling (Read Mode)
    Reads and returns all logged emergency records line by line.
    """
    if not os.path.exists(STORAGE_PATH):
        return []

    collected_records = []
    with open(STORAGE_PATH, mode="r", encoding="utf-8") as file_handle:
        for single_line in file_handle:
            clean_str = single_line.strip()
            if clean_str:
                collected_records.append(clean_str)
    return collected_records
