"""
Utility functions for G120 Desk Planning System
"""
import json
import os
import streamlit as st
from typing import Dict, Any
from modules.config import DATA_FILE

def load_config() -> Dict[str, Any]:
    """Load desk configuration from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error(f"Configuration file {DATA_FILE} not found!")
        return {"tische": {}}

def save_config(config: Dict[str, Any]):
    """Save desk configuration to JSON file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
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
