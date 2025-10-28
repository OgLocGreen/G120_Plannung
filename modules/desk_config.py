"""
Desk Configuration Mode (🔧 Desk Configuration Tab)
"""
import streamlit as st
from typing import Dict, Any
from modules.config import DESK_TYPES, COMPUTER_TYPES, SCREEN_COUNTS
from modules.utils import save_config

def show_tischbearbeitung_modus(config: Dict, tische: Dict):
    """Show the desk configuration mode"""
    st.header("🔧 Desk Configuration")
    st.markdown("Here you can configure individual desks.")
    
    # Sidebar for desk selection
    st.sidebar.subheader("Select Desk")
    
    # Sort desks numerically
    tisch_nummern = sorted([int(t) for t in tische.keys()])
    tisch_optionen = [str(t) for t in tisch_nummern]
    
    selected_tisch = st.sidebar.selectbox(
        "Configure desk:",
        tisch_optionen,
        format_func=lambda x: f"Desk {x}"
    )
    
    if selected_tisch not in tische:
        st.error(f"Desk {selected_tisch} not found in configuration!")
        return
    
    tisch_data = tische[selected_tisch]
    
    st.subheader(f"⚙️ Configuration: {tisch_data['name']}")
    st.markdown("---")
    
    # Form for desk settings
    with st.form(key=f"edit_tisch_{selected_tisch}"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 General Settings")
            
            tisch_name = st.text_input(
                "Desk Name:",
                value=tisch_data.get("name", f"Desk {selected_tisch}")
            )
            
            tisch_typ = st.selectbox(
                "Booking Type:",
                DESK_TYPES,
                index=DESK_TYPES.index(tisch_data.get("typ", "schedule")) if tisch_data.get("typ") in DESK_TYPES else 0
            )
            
            st.markdown("#### 🖥️ Screen Configuration")
            bildschirme = st.selectbox(
                "Number of Screens:",
                SCREEN_COUNTS,
                index=tisch_data.get("rechner", {}).get("bildschirme", 0)
            )
        
        with col2:
            st.markdown("#### 💻 Computer Configuration")
            
            rechner_vorhanden = st.checkbox(
                "Computer available",
                value=tisch_data.get("rechner", {}).get("vorhanden", False)
            )
            
            if rechner_vorhanden:
                rechner_typ = st.selectbox(
                    "Computer Type:",
                    COMPUTER_TYPES,
                    index=COMPUTER_TYPES.index(
                        tisch_data.get("rechner", {}).get("typ", "CPU")
                    ) if tisch_data.get("rechner", {}).get("typ") in COMPUTER_TYPES else 1
                )
                
                rechner_name = st.text_input(
                    "Computer Name:",
                    value=tisch_data.get("rechner", {}).get("name", "")
                )
                
                abschaltbar = st.checkbox(
                    "Computer shutdownable (unchecked = Training Mode)",
                    value=tisch_data.get("rechner", {}).get("abschaltbar", True)
                )
            else:
                rechner_typ = "Leer"
                rechner_name = ""
                abschaltbar = False
        
        st.markdown("---")
        
        # Submit button
        col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 1])
        with col_submit2:
            submit_button = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True,
                type="primary"
            )
        
        if submit_button:
            # Update configuration
            config["tische"][selected_tisch]["name"] = tisch_name
            config["tische"][selected_tisch]["typ"] = tisch_typ
            config["tische"][selected_tisch]["rechner"] = {
                "vorhanden": rechner_vorhanden,
                "typ": rechner_typ if rechner_vorhanden else "Leer",
                "name": rechner_name if rechner_vorhanden else "",
                "abschaltbar": abschaltbar if rechner_vorhanden else False,
                "bildschirme": bildschirme
            }
            
            # Initialize fields based on desk type
            if tisch_typ == "schedule":
                if "buchungen" not in config["tische"][selected_tisch]:
                    config["tische"][selected_tisch]["buchungen"] = {}
            elif tisch_typ == "fullbooking":
                if "gebucht_von" not in config["tische"][selected_tisch]:
                    config["tische"][selected_tisch]["gebucht_von"] = ""
            elif tisch_typ == "projekt":
                if "projekt_name" not in config["tische"][selected_tisch]:
                    config["tische"][selected_tisch]["projekt_name"] = ""
                if "gebucht_von" not in config["tische"][selected_tisch]:
                    config["tische"][selected_tisch]["gebucht_von"] = ""
            
            # Save configuration
            save_config(config)
            
            st.success(f"✅ Configuration for Desk {selected_tisch} saved successfully!")
            st.rerun()
    
    # Display current configuration
    st.markdown("---")
    st.markdown("### 📊 Current Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Type:** {tisch_data.get('typ', 'N/A')}")
        st.info(f"**Screens:** {tisch_data.get('rechner', {}).get('bildschirme', 0)}")
    
    with col2:
        rechner = tisch_data.get("rechner", {})
        if rechner.get("vorhanden"):
            st.success(f"**Computer:** {rechner.get('typ', 'N/A')}")
            st.success(f"**Name:** {rechner.get('name', 'Unnamed')}")
        else:
            st.warning("**Computer:** Not available")
    
    with col3:
        if rechner.get("vorhanden"):
            if rechner.get("abschaltbar"):
                st.success("**Status:** Shutdownable")
            else:
                st.warning("**Status:** Training Mode")
