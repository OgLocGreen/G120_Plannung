"""
Room View Mode (🗺️ Room View Tab)
"""
import streamlit as st
from typing import Dict, Any
from modules.utils import get_desk_status

def show_raumansicht_modus(config: Dict, tische: Dict):
    """Show the room view with all desks"""
    st.header("🗺️ Room View")
    st.markdown("### G120 Room - Overview of All Desks")
    
    # CSS for room view
    st.markdown("""
    <style>
    .raum-container {
        border: 3px solid #333;
        padding: 40px;
        background-color: #f0f0f0;
        border-radius: 10px;
        position: relative;
        min-height: 600px;
    }
    .tisch-box {
        background-color: #4CAF50;
        border: 2px solid #333;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
        color: white;
    }
    .tisch-box:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .tisch-gebucht {
        background-color: #ff6b6b;
    }
    .tisch-teilweise {
        background-color: #ffa500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ Green = Free | Orange = Partially booked | Red = Fully booked | Blue = Project")
    
    # Demo layout: 2 rows with 5 desks each
    st.markdown("---")
    
    # First row (Desk 0-4)
    cols1 = st.columns(5)
    for idx, tisch_id in enumerate(["0", "1", "2", "3", "4"]):
        if tisch_id in tische:
            tisch_data = tische[tisch_id]
            status, info = get_desk_status(tisch_data)
            
            with cols1[idx]:
                st.markdown(f"### {status}")
                st.info(f"**Desk {tisch_id}**\n\n{info}")
                
                rechner = tisch_data.get("rechner", {})
                if rechner.get("vorhanden"):
                    rechner_typ = rechner.get("typ", "N/A")
                    st.caption(f"💻 {rechner_typ}")
                
                # Button to switch to desk planning
                if st.button(f"📋 Book Desk {tisch_id}", key=f"goto_tisch_{tisch_id}", use_container_width=True):
                    st.session_state.selected_modus = "📋 Desk Planning"
                    st.session_state.selected_tisch_from_room = tisch_id
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Second row (Desk 5-9)
    cols2 = st.columns(5)
    for idx, tisch_id in enumerate(["5", "6", "7", "8", "9"]):
        if tisch_id in tische:
            tisch_data = tische[tisch_id]
            status, info = get_desk_status(tisch_data)
            
            with cols2[idx]:
                st.markdown(f"### {status}")
                st.info(f"**Desk {tisch_id}**\n\n{info}")
                
                rechner = tisch_data.get("rechner", {})
                if rechner.get("vorhanden"):
                    rechner_typ = rechner.get("typ", "N/A")
                    st.caption(f"💻 {rechner_typ}")
                
                # Button to switch to desk planning
                if st.button(f"📋 Book Desk {tisch_id}", key=f"goto_tisch_{tisch_id}", use_container_width=True):
                    st.session_state.selected_modus = "📋 Desk Planning"
                    st.session_state.selected_tisch_from_room = tisch_id
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Desk 10 centered
    col_left, col_center, col_right = st.columns([2, 1, 2])
    with col_center:
        if "10" in tische:
            tisch_data = tische["10"]
            status, info = get_desk_status(tisch_data)
            
            st.markdown(f"### {status}")
            st.info(f"**Desk 10**\n\n{info}")
            
            rechner = tisch_data.get("rechner", {})
            if rechner.get("vorhanden"):
                rechner_typ = rechner.get("typ", "N/A")
                st.caption(f"💻 {rechner_typ}")
            
            # Button to switch to desk planning
            if st.button(f"📋 Book Desk 10", key=f"goto_tisch_10", use_container_width=True):
                st.session_state.selected_modus = "📋 Desk Planning"
                st.session_state.selected_tisch_from_room = "10"
                st.rerun()
    
    st.markdown("---")
    st.caption("💡 Tip: Click 'Book Desk X' to create bookings directly")
