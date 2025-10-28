import streamlit as st
import json
import os
from datetime import datetime, time
from typing import Dict, Any

# Konfiguration
DATA_FILE = "data/tische_config.json"

# Wochentage für den Stundenplan (Mo-Fr)
WOCHENTAGE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag"]
WOCHENTAGE_ALLE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

# Zeitslots für den Stundenplan (8:00 - 18:00 für Buchung, 8:00-20:00 für Anzeige)
ZEITSLOTS_BUCHUNG = [f"{h:02d}:00-{h+1:02d}:00" for h in range(8, 18)]
ZEITSLOTS = [f"{h:02d}:00-{h+1:02d}:00" for h in range(8, 20)]

def load_config() -> Dict[str, Any]:
    """Lade die Tischkonfiguration aus der JSON-Datei"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        st.error(f"Konfigurationsdatei {DATA_FILE} nicht gefunden!")
        return {"tische": {}}

def save_config(config: Dict[str, Any]):
    """Speichere die Tischkonfiguration in die JSON-Datei"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def main():
    st.set_page_config(
        page_title="G120 Tischplanung",
        page_icon="🪑",
        layout="wide"
    )
    
    st.title("🪑 G120 Tischplanungs-System")
    st.markdown("---")
    
    # Lade Konfiguration
    config = load_config()
    tische = config.get("tische", {})
    
    # Initialize session state
    if 'selected_modus' not in st.session_state:
        st.session_state.selected_modus = "📋 Tischplanung"
    if 'selected_tisch_from_room' not in st.session_state:
        st.session_state.selected_tisch_from_room = None
    
    # Sidebar - Modus-Auswahl
    st.sidebar.title("⚙️ Navigation")
    
    # Radio button mit aktuellem Modus aus Session State
    modus = st.sidebar.radio(
        "Modus auswählen:",
        ["📋 Tischplanung", "🗺️ Raumansicht", "🔧 Tischbearbeitung"],
        label_visibility="collapsed",
        index=["📋 Tischplanung", "🗺️ Raumansicht", "🔧 Tischbearbeitung"].index(st.session_state.selected_modus)
    )
    
    # Update session state wenn manuell gewechselt wird
    if modus != st.session_state.selected_modus:
        st.session_state.selected_modus = modus
        st.session_state.selected_tisch_from_room = None  # Reset bei manuellem Wechsel
    
    st.sidebar.markdown("---")
    
    # Je nach Modus unterschiedliche Ansicht
    if modus == "📋 Tischplanung":
        show_tischplanung_modus(config, tische)
    elif modus == "🗺️ Raumansicht":
        show_raumansicht_modus(config, tische)
    elif modus == "🔧 Tischbearbeitung":
        show_tischbearbeitung_modus(config, tische)

def show_tischplanung_modus(config: Dict, tische: Dict):
    """Zeige den Tischplanungs-Modus (ursprüngliche Funktionalität)"""
    st.header("📋 Tischplanung")
    
    # Sidebar für Tischauswahl
    st.sidebar.subheader("Tischauswahl")
    
    # Sortiere Tische numerisch
    tisch_nummern = sorted([int(t) for t in tische.keys()])
    tisch_optionen = [str(t) for t in tisch_nummern]
    
    # Wenn von Raumansicht gewechselt wurde, verwende den vorausgewählten Tisch
    default_index = 0
    if st.session_state.selected_tisch_from_room is not None:
        if st.session_state.selected_tisch_from_room in tisch_optionen:
            default_index = tisch_optionen.index(st.session_state.selected_tisch_from_room)
    
    selected_tisch = st.sidebar.selectbox(
        "Wähle einen Tisch:",
        tisch_optionen,
        format_func=lambda x: f"Tisch {x}",
        index=default_index,
        key="tisch_selector"
    )
    
    # Reset der Vorauswahl nach dem ersten Laden
    if st.session_state.selected_tisch_from_room is not None:
        st.session_state.selected_tisch_from_room = None
    
    if selected_tisch not in tische:
        st.error(f"Tisch {selected_tisch} nicht in der Konfiguration gefunden!")
        return
    
    tisch_data = tische[selected_tisch]
    
    # Anzeige der Tischinformationen
    st.subheader(f"📍 {tisch_data['name']}")
    
    # Rechner-Informationen
    col1, col2, col3, col4 = st.columns(4)
    
    rechner_info = tisch_data.get("rechner", {})
    
    with col1:
        if rechner_info.get("vorhanden", False):
            st.success("✅ Rechner vorhanden")
        else:
            st.info("ℹ️ Kein Rechner")
    
    with col2:
        if rechner_info.get("vorhanden", False):
            if rechner_info.get("abschaltbar", False):
                st.success("🔌 Rechner abschaltbar")
            else:
                st.warning("⚠️ Trainings-Modus (nicht abschaltbar)")
    
    with col3:
        bildschirme = rechner_info.get("bildschirme", 0)
        if bildschirme > 0:
            st.info(f"🖥️ {bildschirme} Bildschirm(e)")
        else:
            st.info("🖥️ Keine Bildschirme")
    
    with col4:
        tisch_typ = tisch_data.get("typ", "stundenplan")
        if tisch_typ == "vollbuchung":
            st.warning("👤 Vollbuchung möglich")
        else:
            st.info("📅 Stundenplan-Buchung")
    
    st.markdown("---")
    
    # Unterscheidung zwischen Vollbuchung und Stundenplan
    if tisch_data.get("typ") == "vollbuchung":
        show_vollbuchung_view(selected_tisch, tisch_data, config)
    else:
        show_stundenplan_view(selected_tisch, tisch_data, config)

def show_raumansicht_modus(config: Dict, tische: Dict):
    """Zeige die Raumansicht mit allen Tischen"""
    st.header("🗺️ Raumansicht")
    st.markdown("### G120 Raum - Übersicht aller Tische")
    
    # CSS für die Raumansicht
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
    /* Styling für die Buchungs-Buttons */
    div[data-testid="column"] button[kind="secondary"] {
        border: 2px solid #1f77b4;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ Grün = Frei | Orange = Teilweise gebucht | Rot = Vollständig gebucht | 📋 Klicken Sie auf einen Tisch, um ihn zu buchen")
    
    # Demo-Layout: 2 Reihen mit 5 Tischen pro Reihe
    st.markdown("---")
    
    # Erste Reihe (Tisch 0-4)
    cols1 = st.columns(5)
    for idx, tisch_id in enumerate(["0", "1", "2", "3", "4"]):
        if tisch_id in tische:
            tisch_data = tische[tisch_id]
            buchungen = tisch_data.get("buchungen", {})
            gebucht_von = tisch_data.get("gebucht_von", "")
            
            # Status bestimmen
            if tisch_data.get("typ") == "vollbuchung" and gebucht_von:
                status = "🔴"
                info = f"Gebucht: {gebucht_von}"
            elif len(buchungen) > 0:
                status = "🟠"
                info = f"{len(buchungen)} Buchungen"
            else:
                status = "🟢"
                info = "Frei"
            
            with cols1[idx]:
                st.markdown(f"### {status}")
                st.info(f"**Tisch {tisch_id}**\n\n{info}")
                
                rechner = tisch_data.get("rechner", {})
                if rechner.get("vorhanden"):
                    rechner_typ = rechner.get("typ", "N/A")
                    st.caption(f"💻 {rechner_typ}")
                
                # Button zum Wechseln zur Tischplanung
                if st.button(f"📋 Tisch {tisch_id} buchen", key=f"goto_tisch_{tisch_id}", use_container_width=True):
                    st.session_state.selected_modus = "📋 Tischplanung"
                    st.session_state.selected_tisch_from_room = tisch_id
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Zweite Reihe (Tisch 5-9)
    cols2 = st.columns(5)
    for idx, tisch_id in enumerate(["5", "6", "7", "8", "9"]):
        if tisch_id in tische:
            tisch_data = tische[tisch_id]
            buchungen = tisch_data.get("buchungen", {})
            gebucht_von = tisch_data.get("gebucht_von", "")
            
            # Status bestimmen
            if tisch_data.get("typ") == "vollbuchung" and gebucht_von:
                status = "🔴"
                info = f"Gebucht: {gebucht_von}"
            elif len(buchungen) > 0:
                status = "🟠"
                info = f"{len(buchungen)} Buchungen"
            else:
                status = "🟢"
                info = "Frei"
            
            with cols2[idx]:
                st.markdown(f"### {status}")
                st.info(f"**Tisch {tisch_id}**\n\n{info}")
                
                rechner = tisch_data.get("rechner", {})
                if rechner.get("vorhanden"):
                    rechner_typ = rechner.get("typ", "N/A")
                    st.caption(f"💻 {rechner_typ}")
                
                # Button zum Wechseln zur Tischplanung
                if st.button(f"📋 Tisch {tisch_id} buchen", key=f"goto_tisch_{tisch_id}", use_container_width=True):
                    st.session_state.selected_modus = "📋 Tischplanung"
                    st.session_state.selected_tisch_from_room = tisch_id
                    st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tisch 10 einzeln (zentriert)
    col_left, col_center, col_right = st.columns([2, 1, 2])
    with col_center:
        if "10" in tische:
            tisch_data = tische["10"]
            buchungen = tisch_data.get("buchungen", {})
            gebucht_von = tisch_data.get("gebucht_von", "")
            
            # Status bestimmen
            if tisch_data.get("typ") == "vollbuchung" and gebucht_von:
                status = "🔴"
                info = f"Gebucht: {gebucht_von}"
            elif len(buchungen) > 0:
                status = "🟠"
                info = f"{len(buchungen)} Buchungen"
            else:
                status = "🟢"
                info = "Frei"
            
            st.markdown(f"### {status}")
            st.info(f"**Tisch 10**\n\n{info}")
            
            rechner = tisch_data.get("rechner", {})
            if rechner.get("vorhanden"):
                rechner_typ = rechner.get("typ", "N/A")
                st.caption(f"💻 {rechner_typ}")
            
            # Button zum Wechseln zur Tischplanung
            if st.button(f"📋 Tisch 10 buchen", key=f"goto_tisch_10", use_container_width=True):
                st.session_state.selected_modus = "📋 Tischplanung"
                st.session_state.selected_tisch_from_room = "10"
                st.rerun()
    
    st.markdown("---")
    st.caption("💡 Tipp: Wechseln Sie zu 'Tischplanung' um Buchungen vorzunehmen")

def show_tischbearbeitung_modus(config: Dict, tische: Dict):
    """Zeige den Tischbearbeitungs-Modus"""
    st.header("🔧 Tischbearbeitung")
    st.markdown("Hier können Sie die Konfiguration einzelner Tische anpassen.")
    
    # Sidebar für Tischauswahl
    st.sidebar.subheader("Tisch wählen")
    
    # Sortiere Tische numerisch
    tisch_nummern = sorted([int(t) for t in tische.keys()])
    tisch_optionen = [str(t) for t in tisch_nummern]
    
    selected_tisch = st.sidebar.selectbox(
        "Tisch bearbeiten:",
        tisch_optionen,
        format_func=lambda x: f"Tisch {x}"
    )
    
    if selected_tisch not in tische:
        st.error(f"Tisch {selected_tisch} nicht in der Konfiguration gefunden!")
        return
    
    tisch_data = tische[selected_tisch]
    
    st.subheader(f"⚙️ Konfiguration: {tisch_data['name']}")
    st.markdown("---")
    
    # Formular für Tisch-Einstellungen
    with st.form(key=f"edit_tisch_{selected_tisch}"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Allgemeine Einstellungen")
            
            tisch_name = st.text_input(
                "Tischname:",
                value=tisch_data.get("name", f"Tisch {selected_tisch}")
            )
            
            tisch_typ = st.selectbox(
                "Buchungstyp:",
                ["stundenplan", "vollbuchung"],
                index=0 if tisch_data.get("typ") == "stundenplan" else 1
            )
            
            st.markdown("#### 🖥️ Bildschirm-Konfiguration")
            bildschirme = st.selectbox(
                "Anzahl Bildschirme:",
                [0, 1, 2],
                index=tisch_data.get("rechner", {}).get("bildschirme", 0)
            )
        
        with col2:
            st.markdown("#### 💻 Rechner-Konfiguration")
            
            rechner_vorhanden = st.checkbox(
                "Rechner vorhanden",
                value=tisch_data.get("rechner", {}).get("vorhanden", False)
            )
            
            if rechner_vorhanden:
                rechner_typ = st.selectbox(
                    "Rechner-Typ:",
                    ["GPU", "CPU", "Leer"],
                    index=["GPU", "CPU", "Leer"].index(
                        tisch_data.get("rechner", {}).get("typ", "CPU")
                    ) if tisch_data.get("rechner", {}).get("typ") in ["GPU", "CPU", "Leer"] else 1
                )
                
                rechner_name = st.text_input(
                    "Rechner-Name:",
                    value=tisch_data.get("rechner", {}).get("name", "")
                )
                
                abschaltbar = st.checkbox(
                    "Rechner abschaltbar (aus = Trainings-Modus)",
                    value=tisch_data.get("rechner", {}).get("abschaltbar", True)
                )
            else:
                rechner_typ = "Leer"
                rechner_name = ""
                abschaltbar = False
        
        st.markdown("---")
        
        # Submit Button
        col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 1])
        with col_submit2:
            submit_button = st.form_submit_button(
                "💾 Änderungen speichern",
                use_container_width=True,
                type="primary"
            )
        
        if submit_button:
            # Update Konfiguration
            config["tische"][selected_tisch]["name"] = tisch_name
            config["tische"][selected_tisch]["typ"] = tisch_typ
            config["tische"][selected_tisch]["rechner"] = {
                "vorhanden": rechner_vorhanden,
                "typ": rechner_typ if rechner_vorhanden else "Leer",
                "name": rechner_name if rechner_vorhanden else "",
                "abschaltbar": abschaltbar if rechner_vorhanden else False,
                "bildschirme": bildschirme
            }
            
            # Speichere Konfiguration
            save_config(config)
            
            st.success(f"✅ Konfiguration für Tisch {selected_tisch} erfolgreich gespeichert!")
            st.rerun()
    
    # Aktuelle Konfiguration anzeigen
    st.markdown("---")
    st.markdown("### 📊 Aktuelle Konfiguration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**Typ:** {tisch_data.get('typ', 'N/A')}")
        st.info(f"**Bildschirme:** {tisch_data.get('rechner', {}).get('bildschirme', 0)}")
    
    with col2:
        rechner = tisch_data.get("rechner", {})
        if rechner.get("vorhanden"):
            st.success(f"**Rechner:** {rechner.get('typ', 'N/A')}")
            st.success(f"**Name:** {rechner.get('name', 'Unbenannt')}")
        else:
            st.warning("**Rechner:** Nicht vorhanden")
    
    with col3:
        if rechner.get("vorhanden"):
            if rechner.get("abschaltbar"):
                st.success("**Status:** Abschaltbar")
            else:
                st.warning("**Status:** Trainings-Modus")


def show_vollbuchung_view(tisch_id: str, tisch_data: Dict, config: Dict):
    """Zeige die Vollbuchungs-Ansicht"""
    st.subheader("👤 Vollbuchung")
    
    gebucht_von = tisch_data.get("gebucht_von", "")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        neuer_name = st.text_input(
            "Gebucht von:",
            value=gebucht_von,
            placeholder="Name der Person eingeben"
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("💾 Speichern", type="primary"):
            config["tische"][tisch_id]["gebucht_von"] = neuer_name
            save_config(config)
            st.success("Buchung gespeichert!")
            st.rerun()
    
    if gebucht_von:
        st.success(f"✅ Tisch ist vollständig gebucht von: **{gebucht_von}**")
    else:
        st.info("ℹ️ Tisch ist aktuell nicht gebucht")

def show_stundenplan_view(tisch_id: str, tisch_data: Dict, config: Dict):
    """Zeige die Stundenplan-Ansicht"""
    st.subheader("📅 Stundenplan-Buchungen")
    
    buchungen = tisch_data.get("buchungen", {})
    
    # Tabs für verschiedene Ansichten
    tab1, tab2, tab3 = st.tabs(["📊 Wochenübersicht", "➕ Neue Buchung", "📋 Alle Buchungen"])
    
    with tab1:
        show_wochenansicht(buchungen)
    
    with tab2:
        add_new_buchung(tisch_id, buchungen, config)
    
    with tab3:
        show_all_buchungen(tisch_id, buchungen, config)

def show_wochenansicht(buchungen: Dict):
    """Zeige eine visuelle Wochenübersicht"""
    st.markdown("### 📅 Wochenplan")
    
    # Erstelle eine Tabelle für die Wochenansicht
    for tag in WOCHENTAGE_ALLE:
        st.markdown(f"**{tag}**")
        
        tag_buchungen = {slot: [] for slot in ZEITSLOTS}
        
        # Sammle alle Buchungen für diesen Tag
        for buchung_key, buchung in buchungen.items():
            if buchung.get("tag") == tag:
                slot = buchung.get("zeitslot")
                if slot in tag_buchungen:
                    tag_buchungen[slot].append(buchung.get("person", "Unbekannt"))
        
        # Zeige die Buchungen in einer Grid-Ansicht
        cols = st.columns(4)
        for idx, slot in enumerate(ZEITSLOTS):
            col_idx = idx % 4
            with cols[col_idx]:
                personen = tag_buchungen[slot]
                if personen:
                    st.success(f"**{slot}**\n\n{', '.join(personen)}")
                else:
                    st.info(f"{slot}\n\nFrei")
        
        st.markdown("---")

def add_new_buchung(tisch_id: str, buchungen: Dict, config: Dict):
    """Füge eine neue Buchung hinzu mit visuellem Zeitslot-Grid"""
    st.markdown("### ➕ Neue Buchung erstellen")
    
    # Initialize session state for selected slots if not exists
    if 'selected_slots' not in st.session_state:
        st.session_state.selected_slots = set()
    
    # Name und Rechner-Modus Eingabe
    col1, col2 = st.columns(2)
    
    with col1:
        person = st.text_input("👤 Name der Person:", placeholder="Max Mustermann", key="person_name")
    
    with col2:
        # Rechner-Modus (nur wenn Rechner vorhanden)
        tisch_data = config["tische"][tisch_id]
        rechner_vorhanden = tisch_data.get("rechner", {}).get("vorhanden", False)
        
        if rechner_vorhanden:
            rechner_modus = st.selectbox(
                "💻 Rechner-Nutzung:",
                ["Nur Bildschirme", "Rechner aktiv (abschaltbar)", "Trainings-Modus (nicht abschaltbar)"]
            )
        else:
            rechner_modus = "Kein Rechner"
            st.info("ℹ️ Dieser Tisch hat keinen Rechner")
    
    notizen = st.text_area("📝 Notizen (optional):", placeholder="Zusätzliche Informationen...", key="notizen")
    
    st.markdown("---")
    st.markdown("### 📅 Zeitslots auswählen (Montag - Freitag, 8:00 - 18:00 Uhr)")
    st.markdown("**Klicken Sie auf die Zeitslots, um sie zu buchen. Grün = Frei, Rot = Ausgewählt, Grau = Bereits gebucht**")
    
    # Custom CSS für die Buttons
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
    
    # Erstelle einen Button-Grid für jeden Wochentag
    for tag in WOCHENTAGE:
        st.markdown(f"#### {tag}")
        
        # Prüfe welche Slots bereits gebucht sind
        gebuchte_slots = set()
        for buchung_key, buchung in buchungen.items():
            if buchung.get("tag") == tag:
                gebuchte_slots.add(buchung.get("zeitslot"))
        
        # Erstelle Buttons in Spalten (5 Buttons pro Reihe)
        cols = st.columns(5)
        for idx, zeitslot in enumerate(ZEITSLOTS_BUCHUNG):
            col_idx = idx % 5
            slot_key = f"{tag}_{zeitslot}"
            
            with cols[col_idx]:
                # Bestimme Button-Status
                is_gebucht = zeitslot in gebuchte_slots
                is_selected = slot_key in st.session_state.selected_slots
                
                # Button-Label mit Uhrzeit
                stunde = zeitslot.split('-')[0]
                button_label = stunde
                
                # Erstelle Button mit entsprechendem Status
                if is_gebucht:
                    # Bereits gebuchter Slot - deaktiviert
                    st.button(
                        f"� {button_label}",
                        key=f"btn_{slot_key}",
                        disabled=True,
                        help=f"Bereits gebucht am {tag} um {zeitslot}"
                    )
                elif is_selected:
                    # Ausgewählter Slot - rot
                    if st.button(
                        f"🔴 {button_label}",
                        key=f"btn_{slot_key}",
                        type="primary",
                        help=f"Klicken zum Abwählen: {tag} {zeitslot}"
                    ):
                        st.session_state.selected_slots.discard(slot_key)
                        st.rerun()
                else:
                    # Freier Slot - grün
                    if st.button(
                        f"🟢 {button_label}",
                        key=f"btn_{slot_key}",
                        help=f"Klicken zum Auswählen: {tag} {zeitslot}"
                    ):
                        st.session_state.selected_slots.add(slot_key)
                        st.rerun()
        
        st.markdown("")
    
    st.markdown("---")
    
    # Zeige ausgewählte Slots
    if st.session_state.selected_slots:
        st.success(f"✅ **{len(st.session_state.selected_slots)} Zeitslot(s) ausgewählt**")
        
        # Gruppiere nach Tag für bessere Übersicht
        selected_by_day = {}
        for slot_key in sorted(st.session_state.selected_slots):
            tag, zeitslot = slot_key.rsplit('_', 1)
            if tag not in selected_by_day:
                selected_by_day[tag] = []
            selected_by_day[tag].append(zeitslot)
        
        for tag, slots in selected_by_day.items():
            st.write(f"**{tag}:** {', '.join(sorted(slots))}")
    else:
        st.info("ℹ️ Keine Zeitslots ausgewählt")
    
    # Buttons für Aktionen
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        if st.button("🗑️ Auswahl zurücksetzen", use_container_width=True):
            st.session_state.selected_slots = set()
            st.rerun()
    
    with col2:
        if st.button("💾 Buchungen speichern", type="primary", use_container_width=True):
            if not person:
                st.error("Bitte gib einen Namen ein!")
            elif not st.session_state.selected_slots:
                st.error("Bitte wähle mindestens einen Zeitslot aus!")
            else:
                # Erstelle Buchungen für alle ausgewählten Slots
                erfolg_count = 0
                for slot_key in st.session_state.selected_slots:
                    tag, zeitslot = slot_key.rsplit('_', 1)
                    
                    # Erstelle eindeutige ID
                    buchung_id = f"{tag}_{zeitslot}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
                    
                    buchungen[buchung_id] = {
                        "person": person,
                        "tag": tag,
                        "zeitslot": zeitslot,
                        "rechner_modus": rechner_modus if rechner_vorhanden else "Kein Rechner",
                        "notizen": notizen,
                        "erstellt_am": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    erfolg_count += 1
                
                # Speichere Konfiguration
                config["tische"][tisch_id]["buchungen"] = buchungen
                save_config(config)
                
                # Reset selection
                st.session_state.selected_slots = set()
                
                st.success(f"✅ {erfolg_count} Buchung(en) für {person} erfolgreich erstellt!")
                st.rerun()

def show_all_buchungen(tisch_id: str, buchungen: Dict, config: Dict):
    """Zeige alle Buchungen mit Löschoption"""
    st.markdown("### 📋 Alle Buchungen")
    
    if not buchungen:
        st.info("ℹ️ Noch keine Buchungen vorhanden")
        return
    
    # Sortiere Buchungen nach Tag und Zeitslot
    sorted_buchungen = sorted(
        buchungen.items(),
        key=lambda x: (WOCHENTAGE_ALLE.index(x[1].get("tag", "Montag")), x[1].get("zeitslot", ""))
    )
    
    for buchung_id, buchung in sorted_buchungen:
        with st.expander(
            f"🕐 {buchung.get('tag')} | {buchung.get('zeitslot')} - {buchung.get('person')}"
        ):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.write(f"**Person:** {buchung.get('person')}")
                st.write(f"**Tag:** {buchung.get('tag')}")
                st.write(f"**Zeitslot:** {buchung.get('zeitslot')}")
                st.write(f"**Rechner-Modus:** {buchung.get('rechner_modus', 'N/A')}")
                if buchung.get('notizen'):
                    st.write(f"**Notizen:** {buchung.get('notizen')}")
                st.caption(f"Erstellt am: {buchung.get('erstellt_am', 'Unbekannt')}")
            
            with col2:
                if st.button("🗑️ Löschen", key=f"delete_{buchung_id}"):
                    del buchungen[buchung_id]
                    config["tische"][tisch_id]["buchungen"] = buchungen
                    save_config(config)
                    st.success("Buchung gelöscht!")
                    st.rerun()

if __name__ == "__main__":
    main()
