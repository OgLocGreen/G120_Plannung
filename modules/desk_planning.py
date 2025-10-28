"""
Desk Planning Mode (📋 Desk Planning Tab)
"""
import streamlit as st
from typing import Dict, Any
from datetime import datetime
from modules.config import WEEKDAYS, WEEKDAYS_ALL, TIMESLOTS_BOOKING, TIMESLOTS
from modules.utils import save_config

def show_tischplanung_modus(config: Dict, tische: Dict):
    """Show the Desk Planning mode (original functionality)"""
    st.header("📋 Desk Planning")
    
    # Sidebar for desk selection
    st.sidebar.subheader("Desk Selection")
    
    # Sort desks numerically
    tisch_nummern = sorted([int(t) for t in tische.keys()])
    tisch_optionen = [str(t) for t in tisch_nummern]
    
    # If switched from room view, use pre-selected desk
    default_index = 0
    if st.session_state.selected_tisch_from_room is not None:
        if st.session_state.selected_tisch_from_room in tisch_optionen:
            default_index = tisch_optionen.index(st.session_state.selected_tisch_from_room)
    
    selected_tisch = st.sidebar.selectbox(
        "Choose a desk:",
        tisch_optionen,
        format_func=lambda x: f"Desk {x}",
        index=default_index,
        key="tisch_selector"
    )
    
    # Reset pre-selection after first load
    if st.session_state.selected_tisch_from_room is not None:
        st.session_state.selected_tisch_from_room = None
    
    if selected_tisch not in tische:
        st.error(f"Desk {selected_tisch} not found in configuration!")
        return
    
    tisch_data = tische[selected_tisch]
    
    # Display desk information
    st.subheader(f"📍 {tisch_data['name']}")
    
    # Computer information
    col1, col2, col3, col4 = st.columns(4)
    
    rechner_info = tisch_data.get("rechner", {})
    
    with col1:
        if rechner_info.get("vorhanden", False):
            st.success("✅ Computer available")
        else:
            st.info("ℹ️ No computer")
    
    with col2:
        if rechner_info.get("vorhanden", False):
            if rechner_info.get("abschaltbar", False):
                st.success("🔌 Computer shutdownable")
            else:
                st.warning("⚠️ Training Mode (not shutdownable)")
    
    with col3:
        bildschirme = rechner_info.get("bildschirme", 0)
        if bildschirme > 0:
            st.info(f"🖥️ {bildschirme} Screen(s)")
        else:
            st.info("🖥️ No screens")
    
    with col4:
        tisch_typ = tisch_data.get("typ", "schedule")
        if tisch_typ == "fullbooking":
            st.warning("👤 Full booking possible")
        elif tisch_typ == "projekt":
            st.info("🔵 Project desk")
        else:
            st.info("📅 Schedule booking")
    
    st.markdown("---")
    
    # Different views based on booking type
    if tisch_data.get("typ") == "fullbooking":
        show_fullbooking_view(selected_tisch, tisch_data, config)
    elif tisch_data.get("typ") == "projekt":
        show_projekt_view(selected_tisch, tisch_data, config)
    else:
        show_schedule_view(selected_tisch, tisch_data, config)

def show_fullbooking_view(tisch_id: str, tisch_data: Dict, config: Dict):
    """Show the full booking view (person booking)"""
    st.subheader("👤 Full Booking")
    
    gebucht_von = tisch_data.get("gebucht_von", "")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        neuer_name = st.text_input(
            "Booked by:",
            value=gebucht_von,
            placeholder="Enter person name"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("💾 Save", type="primary"):
            config["tische"][tisch_id]["gebucht_von"] = neuer_name
            save_config(config)
            st.success("Booking saved!")
            st.rerun()
    
    if gebucht_von:
        st.success(f"✅ Desk is fully booked by: **{gebucht_von}**")
    else:
        st.info("ℹ️ Desk is currently not booked")

def show_projekt_view(tisch_id: str, tisch_data: Dict, config: Dict):
    """Show the project view"""
    st.subheader("🔵 Project Booking")
    
    projekt_name = tisch_data.get("projekt_name", "")
    ansprechpartner = tisch_data.get("gebucht_von", "")
    
    col1, col2 = st.columns(2)
    
    with col1:
        neuer_projekt_name = st.text_input(
            "🔷 Project Name:",
            value=projekt_name,
            placeholder="e.g. AI Research, Bachelor Thesis, etc."
        )
    
    with col2:
        neuer_ansprechpartner = st.text_input(
            "👤 Contact Person:",
            value=ansprechpartner,
            placeholder="Name of contact person"
        )
    
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
    with col_btn2:
        if st.button("💾 Save", type="primary", use_container_width=True):
            config["tische"][tisch_id]["projekt_name"] = neuer_projekt_name
            config["tische"][tisch_id]["gebucht_von"] = neuer_ansprechpartner
            save_config(config)
            st.success("Project booking saved!")
            st.rerun()
    
    st.markdown("---")
    
    if projekt_name and ansprechpartner:
        st.success(f"✅ **Project:** {projekt_name}")
        st.info(f"👤 **Contact:** {ansprechpartner}")
    elif projekt_name:
        st.warning(f"🔷 **Project:** {projekt_name}")
        st.warning("⚠️ No contact person entered")
    else:
        st.info("ℹ️ No project assigned yet")

def show_schedule_view(tisch_id: str, tisch_data: Dict, config: Dict):
    """Show the schedule view"""
    st.subheader("📅 Schedule Bookings")
    
    buchungen = tisch_data.get("buchungen", {})
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📊 Weekly Overview", "➕ New Booking", "📋 All Bookings"])
    
    with tab1:
        show_weekly_view(buchungen)
    
    with tab2:
        add_new_booking(tisch_id, buchungen, config)
    
    with tab3:
        show_all_bookings(tisch_id, buchungen, config)

def show_weekly_view(buchungen: Dict):
    """Show a visual weekly overview"""
    st.markdown("### 📅 Weekly Schedule")
    
    for tag in WEEKDAYS_ALL:
        st.markdown(f"**{tag}**")
        
        tag_buchungen = {slot: [] for slot in TIMESLOTS}
        
        # Collect all bookings for this day
        for buchung_key, buchung in buchungen.items():
            if buchung.get("tag") == tag:
                slot = buchung.get("zeitslot")
                if slot in tag_buchungen:
                    tag_buchungen[slot].append(buchung.get("person", "Unknown"))
        
        # Display bookings in grid view
        cols = st.columns(4)
        for idx, slot in enumerate(TIMESLOTS):
            col_idx = idx % 4
            with cols[col_idx]:
                personen = tag_buchungen[slot]
                if personen:
                    st.success(f"**{slot}**\n\n{', '.join(personen)}")
                else:
                    st.info(f"{slot}\n\nFree")
        
        st.markdown("---")

def add_new_booking(tisch_id: str, buchungen: Dict, config: Dict):
    """Add a new booking with visual time slot grid"""
    st.markdown("### ➕ Create New Booking")
    
    # Initialize session state for selected slots
    if 'selected_slots' not in st.session_state:
        st.session_state.selected_slots = set()
    
    # Name and computer mode input
    col1, col2 = st.columns(2)
    
    with col1:
        person = st.text_input("👤 Person Name:", placeholder="Max Mustermann", key="person_name")
    
    with col2:
        # Computer mode (only if computer available)
        tisch_data = config["tische"][tisch_id]
        rechner_vorhanden = tisch_data.get("rechner", {}).get("vorhanden", False)
        
        if rechner_vorhanden:
            rechner_modus = st.selectbox(
                "💻 Computer Usage:",
                ["Screens Only", "Computer Active (Shutdownable)", "Training Mode (Not Shutdownable)"]
            )
        else:
            rechner_modus = "No Computer"
            st.info("ℹ️ This desk has no computer")
    
    notizen = st.text_area("📝 Notes (optional):", placeholder="Additional information...", key="notizen")
    
    st.markdown("---")
    st.markdown("### 📅 Select Time Slots (Monday - Friday, 8:00 - 18:00)")
    st.markdown("**Click on time slots to book. Green = Free, Red = Selected, Gray = Already booked**")
    
    # Custom CSS for buttons
    st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 60px;
        font-size: 12px;
        margin: 2px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create button grid for each weekday
    for tag in WEEKDAYS:
        st.markdown(f"#### {tag}")
        
        # Check which slots are already booked
        gebuchte_slots = set()
        for buchung_key, buchung in buchungen.items():
            if buchung.get("tag") == tag:
                gebuchte_slots.add(buchung.get("zeitslot"))
        
        # Create buttons in columns (5 buttons per row)
        cols = st.columns(5)
        for idx, zeitslot in enumerate(TIMESLOTS_BOOKING):
            col_idx = idx % 5
            slot_key = f"{tag}_{zeitslot}"
            
            with cols[col_idx]:
                # Determine button status
                is_gebucht = zeitslot in gebuchte_slots
                is_selected = slot_key in st.session_state.selected_slots
                
                # Button label with time
                stunde = zeitslot.split('-')[0]
                button_label = stunde
                
                # Create button with appropriate status
                if is_gebucht:
                    # Already booked slot - disabled
                    st.button(
                        f"🚫 {button_label}",
                        key=f"btn_{slot_key}",
                        disabled=True,
                        help=f"Already booked on {tag} at {zeitslot}"
                    )
                elif is_selected:
                    # Selected slot - red
                    if st.button(
                        f"🔴 {button_label}",
                        key=f"btn_{slot_key}",
                        type="primary",
                        help=f"Click to deselect: {tag} {zeitslot}"
                    ):
                        st.session_state.selected_slots.discard(slot_key)
                        st.rerun()
                else:
                    # Free slot - green
                    if st.button(
                        f"🟢 {button_label}",
                        key=f"btn_{slot_key}",
                        help=f"Click to select: {tag} {zeitslot}"
                    ):
                        st.session_state.selected_slots.add(slot_key)
                        st.rerun()
        
        st.markdown("")
    
    st.markdown("---")
    
    # Show selected slots
    if st.session_state.selected_slots:
        st.success(f"✅ **{len(st.session_state.selected_slots)} Time slot(s) selected**")
        
        # Group by day for better overview
        selected_by_day = {}
        for slot_key in sorted(st.session_state.selected_slots):
            tag, zeitslot = slot_key.rsplit('_', 1)
            if tag not in selected_by_day:
                selected_by_day[tag] = []
            selected_by_day[tag].append(zeitslot)
        
        for tag, slots in selected_by_day.items():
            st.write(f"**{tag}:** {', '.join(sorted(slots))}")
    else:
        st.info("ℹ️ No time slots selected")
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        if st.button("🗑️ Reset Selection", use_container_width=True):
            st.session_state.selected_slots = set()
            st.rerun()
    
    with col2:
        if st.button("💾 Save Bookings", type="primary", use_container_width=True):
            if not person:
                st.error("Please enter a name!")
            elif not st.session_state.selected_slots:
                st.error("Please select at least one time slot!")
            else:
                # Create bookings for all selected slots
                erfolg_count = 0
                for slot_key in st.session_state.selected_slots:
                    tag, zeitslot = slot_key.rsplit('_', 1)
                    
                    # Create unique ID
                    buchung_id = f"{tag}_{zeitslot}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                    
                    buchungen[buchung_id] = {
                        "person": person,
                        "tag": tag,
                        "zeitslot": zeitslot,
                        "rechner_modus": rechner_modus if rechner_vorhanden else "No Computer",
                        "notizen": notizen,
                        "erstellt_am": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    erfolg_count += 1
                
                # Save configuration
                config["tische"][tisch_id]["buchungen"] = buchungen
                save_config(config)
                
                # Reset selection
                st.session_state.selected_slots = set()
                
                st.success(f"✅ {erfolg_count} Booking(s) for {person} created successfully!")
                st.rerun()

def show_all_bookings(tisch_id: str, buchungen: Dict, config: Dict):
    """Show all bookings with delete option"""
    st.markdown("### 📋 All Bookings")
    
    if not buchungen:
        st.info("ℹ️ No bookings yet")
        return
    
    # Sort bookings by day and time slot
    sorted_buchungen = sorted(
        buchungen.items(),
        key=lambda x: (WEEKDAYS_ALL.index(x[1].get("tag", "Monday")), x[1].get("zeitslot", ""))
    )
    
    for buchung_id, buchung in sorted_buchungen:
        with st.expander(
            f"🕐 {buchung.get('tag')} | {buchung.get('zeitslot')} - {buchung.get('person')}"
        ):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.write(f"**Person:** {buchung.get('person')}")
                st.write(f"**Day:** {buchung.get('tag')}")
                st.write(f"**Time Slot:** {buchung.get('zeitslot')}")
                st.write(f"**Computer Mode:** {buchung.get('rechner_modus', 'N/A')}")
                if buchung.get('notizen'):
                    st.write(f"**Notes:** {buchung.get('notizen')}")
                st.caption(f"Created: {buchung.get('erstellt_am', 'Unknown')}")
            
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{buchung_id}"):
                    del buchungen[buchung_id]
                    config["tische"][tisch_id]["buchungen"] = buchungen
                    save_config(config)
                    st.success("Booking deleted!")
                    st.rerun()
