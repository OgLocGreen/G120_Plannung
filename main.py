"""
G120 Desk Planning System - Main Application
"""
import streamlit as st
from modules.utils import load_config
from modules.desk_planning import show_tischplanung_modus
from modules.room_view import show_raumansicht_modus
from modules.desk_config import show_tischbearbeitung_modus

def initialize_session_state():
    """Initialize session state variables"""
    if 'selected_modus' not in st.session_state:
        st.session_state.selected_modus = "📋 Desk Planning"
    if 'selected_tisch_from_room' not in st.session_state:
        st.session_state.selected_tisch_from_room = None
    if 'selected_slots' not in st.session_state:
        st.session_state.selected_slots = set()

def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="G120 Desk Planning",
        page_icon="🪑",
        layout="wide"
    )
    
    st.title("🪑 G120 Desk Planning System")
    st.markdown("---")
    
    # Initialize session state
    initialize_session_state()
    
    # Load configuration
    config = load_config()
    tische = config.get("tische", {})
    
    # Sidebar - Mode selection
    st.sidebar.title("⚙️ Navigation")
    
    # Radio button with current mode from session state
    modus = st.sidebar.radio(
        "Select mode:",
        ["📋 Desk Planning", "🗺️ Room View", "🔧 Desk Configuration"],
        label_visibility="collapsed",
        index=["📋 Desk Planning", "🗺️ Room View", "🔧 Desk Configuration"].index(st.session_state.selected_modus)
    )
    
    # Update session state when manually switched
    if modus != st.session_state.selected_modus:
        st.session_state.selected_modus = modus
        st.session_state.selected_tisch_from_room = None  # Reset on manual switch
    
    st.sidebar.markdown("---")
    
    # Different view depending on mode
    if modus == "📋 Desk Planning":
        show_tischplanung_modus(config, tische)
    elif modus == "🗺️ Room View":
        show_raumansicht_modus(config, tische)
    elif modus == "🔧 Desk Configuration":
        show_tischbearbeitung_modus(config, tische)

if __name__ == "__main__":
    main()
