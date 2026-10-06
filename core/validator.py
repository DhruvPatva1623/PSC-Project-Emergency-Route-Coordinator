"""
core/validator.py
=================
Input Validation and Persistent File Logging module.
Demonstrates:
- Regular Expressions (re module)
- File Handling: Writing and Reading text logs
(Syllabus: UNIT-I File I/O & UNIT-II Regular Expressions)
"""

import re
import os
from datetime import datetime

STORAGE_PATH = os.path.join("data", "emergency_records.txt")


def check_phone_format(phone: str) -> bool:
    """
    [UNIT-II: Regular Expressions]
    Validates Indian standard 10-digit emergency contact numbers.
    Pattern: Starts with 6, 7, 8, or 9 followed by 9 digits.
    """
    regex_pattern = r"^[6-9]\d{9}$"
    return bool(re.match(regex_pattern, phone.strip()))


def check_emergency_tag(tag: str) -> bool:
    """
    [UNIT-II: Regular Expressions]
    Validates incident ticket tags (e.g., 'SOS-101', 'MED-402', 'FIRE-999').
    """
    regex_pattern = r"^[A-Z]{3,4}-\d{3,4}$"
    return bool(re.match(regex_pattern, tag.strip().upper()))


def append_record_to_file(alert_id: str, citizen: str, phone: str, 
                          hazard: str, priority: str, location: str) -> None:
    """
    [UNIT-I: File Handling - Write]
    Appends a formatted incident record line to plain text file storage.
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
    [UNIT-I: File Handling - Read]
    Reads stored incident records line by line from the text file.
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
