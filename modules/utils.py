"""
Utility functions for G120 Desk Planning System
"""
import json
import os
import streamlit as st
from typing import Dict, Any
from modules.config import DATA_FILE

# Mapping for German to English weekdays
WEEKDAY_MAPPING = {
    "Montag": "Monday",
    "Dienstag": "Tuesday",
    "Mittwoch": "Wednesday",
    "Donnerstag": "Thursday",
    "Freitag": "Friday",
    "Samstag": "Saturday",
    "Sonntag": "Sunday"
}

# Mapping for German to English computer modes
COMPUTER_MODE_MAPPING = {
    "Nur Bildschirme": "Screens Only",
    "Rechner aktiv (abschaltbar)": "Computer Active (Shutdownable)",
    "Trainings-Modus (nicht abschaltbar)": "Training Mode (Not Shutdownable)",
    "Kein Rechner": "No Computer"
}

# Mapping for German to English desk types
DESK_TYPE_MAPPING = {
    "stundenplan": "schedule",
    "vollbuchung": "fullbooking",
    "projekt": "projekt"
}

# Mapping for German to English computer types
COMPUTER_TYPE_MAPPING = {
    "Leer": "None",
    "GPU": "GPU",
    "CPU": "CPU",
    "None": "None"  # Already migrated
}

def load_config() -> Dict[str, Any]:
    """Load desk configuration from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Migrate German to English weekdays
        config = migrate_weekdays(config)
        
        return config
    else:
        st.error(f"Configuration file {DATA_FILE} not found!")
        return {"tische": {}}

def migrate_weekdays(config: Dict[str, Any]) -> Dict[str, Any]:
    """Migrate German names to English (weekdays, desk types, computer modes)"""
    tische = config.get("tische", {})
    
    for desk_id, desk_data in tische.items():
        # Migrate desk type
        if "typ" in desk_data and desk_data["typ"] in DESK_TYPE_MAPPING:
            desk_data["typ"] = DESK_TYPE_MAPPING[desk_data["typ"]]
        
        # Migrate computer type
        if "rechner" in desk_data:
            rechner = desk_data["rechner"]
            if "typ" in rechner and rechner["typ"] in COMPUTER_TYPE_MAPPING:
                rechner["typ"] = COMPUTER_TYPE_MAPPING[rechner["typ"]]
        
        # Migrate bookings (weekdays and computer modes)
        if "buchungen" in desk_data:
            buchungen = desk_data["buchungen"]
            for booking_id, booking in buchungen.items():
                # Migrate weekday
                if "tag" in booking and booking["tag"] in WEEKDAY_MAPPING:
                    booking["tag"] = WEEKDAY_MAPPING[booking["tag"]]
                
                # Migrate computer mode
                if "rechner_modus" in booking and booking["rechner_modus"] in COMPUTER_MODE_MAPPING:
                    booking["rechner_modus"] = COMPUTER_MODE_MAPPING[booking["rechner_modus"]]
    
    return config

def save_config(config: Dict[str, Any]):
    """Save desk configuration to JSON file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # Ensure all configs are saved with migration applied
    config = migrate_weekdays(config)
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_desk_status(tisch_data: Dict) -> tuple:
    """
    Determine desk status based on booking type
    Returns: (emoji, info_text)
    """
    buchungen = tisch_data.get("buchungen", {})
    gebucht_von = tisch_data.get("gebucht_von", "")
    projekt_name = tisch_data.get("projekt_name", "")
    tisch_typ = tisch_data.get("typ", "schedule")
    
    if tisch_typ == "projekt":
        if projekt_name:
            info = f"Project: {projekt_name}"
            if gebucht_von:
                info += f"\nContact: {gebucht_von}"
            return "🔵", info
        else:
            return "🔵", "Project (unassigned)"
    elif tisch_typ == "fullbooking" and gebucht_von:
        return "🔴", f"Booked: {gebucht_von}"
    elif len(buchungen) > 0:
        return "🟠", f"{len(buchungen)} Bookings"
    else:
        return "🟢", "Free"
