# 🪑 G120 Tischplanungs-System

Eine Streamlit-basierte Anwendung zur Verwaltung und Planung von Tischbuchungen im G120-Raum.

## 🎯 Funktionen

- **Tischverwaltung**: Verwaltung von 11 Tischen (Tisch 0-10)
- **Zwei Buchungstypen**:
  - **Vollbuchung**: Tisch wird komplett auf eine Person gebucht (nur Name erforderlich)
  - **Stundenplan-Buchung**: Detaillierte Zeitslot-Buchungen mit Wochenplanung
- **Rechner-Management**:
  - Anzeige ob Rechner vorhanden ist
  - Kennzeichnung ob Rechner abschaltbar ist (Trainings-Modus)
  - Verwaltung von Bildschirmen
  - Verschiedene Nutzungsmodi: Nur Bildschirme, Rechner aktiv, Trainings-Modus
- **Wochenübersicht**: Visuelle Darstellung aller Buchungen pro Wochentag
- **Buchungsverwaltung**: Hinzufügen, Anzeigen und Löschen von Buchungen

## 📋 Voraussetzungen

- Python 3.8 oder höher
- pip (Python Package Manager)

## 🚀 Installation

1. **Repository klonen oder Dateien herunterladen**

2. **Abhängigkeiten installieren**:
```bash
pip install -r requirements.txt
```

## ▶️ Anwendung starten

```bash
streamlit run tischplanung_app.py
```

Die Anwendung öffnet sich automatisch im Browser unter `http://localhost:8501`

## 📁 Projektstruktur

```
G120_Plannung/
├── tischplanung_app.py          # Hauptanwendung
├── requirements.txt              # Python-Abhängigkeiten
├── data/
│   └── tische_config.json       # Tischkonfiguration und Buchungen
└── README.md                     # Diese Datei
```

## 🔧 Konfiguration

Die Tischkonfiguration befindet sich in `data/tische_config.json`. Jeder Tisch hat folgende Eigenschaften:

```json
{
  "name": "Tisch X",
  "typ": "stundenplan" | "vollbuchung",
  "rechner": {
    "vorhanden": true/false,
    "abschaltbar": true/false,
    "bildschirme": 0-2
  },
  "buchungen": {},
  "gebucht_von": ""
}
```

### Tisch-Typen:

- **`stundenplan`**: Ermöglicht zeitbasierte Buchungen mit Wochentagen und Zeitslots
- **`vollbuchung`**: Tisch kann nur komplett auf eine Person gebucht werden

### Rechner-Einstellungen:

- **`vorhanden`**: Gibt an, ob ein Rechner am Tisch vorhanden ist
- **`abschaltbar`**: 
  - `true`: Rechner kann ausgeschaltet werden
  - `false`: Trainings-Modus, Rechner darf nicht ausgeschaltet werden
- **`bildschirme`**: Anzahl der verfügbaren Bildschirme (0-2)

## 💡 Verwendung

### Tisch auswählen
- Wählen Sie in der Sidebar einen Tisch aus (Tisch 0-10)
- Die Tischinformationen werden oben angezeigt

### Vollbuchung (z.B. Tisch 3, 6)
- Geben Sie einfach den Namen der Person ein
- Klicken Sie auf "Speichern"
- Der Tisch ist komplett für diese Person reserviert

### Stundenplan-Buchung (z.B. Tisch 0-10)
- **Wochenübersicht**: Sehen Sie alle Buchungen auf einen Blick
- **Neue Buchung**: 
  - Name der Person eingeben
  - Wochentag auswählen
  - Zeitslot wählen (8:00-20:00 Uhr)
  - Rechner-Modus festlegen
  - Optional: Notizen hinzufügen
- **Alle Buchungen**: Detaillierte Liste mit Löschfunktion

### Rechner-Modi:
- **Nur Bildschirme**: Person nutzt nur die Bildschirme
- **Rechner aktiv (abschaltbar)**: Person nutzt den Rechner und darf ihn ausschalten
- **Trainings-Modus (nicht abschaltbar)**: Person nutzt den Rechner, darf ihn aber nicht ausschalten

## 📊 Zeitslots

Die Buchungen können in 1-Stunden-Slots von 8:00 bis 20:00 Uhr erfolgen:
- 8:00-9:00, 9:00-10:00, ..., 19:00-20:00

## 🗓️ Wochentage

Buchungen können für alle Wochentage gemacht werden:
- Montag bis Sonntag

## 🔄 Datenspersistenz

Alle Buchungen werden automatisch in `data/tische_config.json` gespeichert und bleiben auch nach einem Neustart der Anwendung erhalten.

## 🎨 Anpassung

Sie können das Raumlayout später anpassen, indem Sie die `data/tische_config.json` bearbeiten:
- Tische hinzufügen/entfernen
- Rechner-Konfigurationen ändern
- Tisch-Typen anpassen

## 📝 Lizenz

Dieses Projekt ist für den internen Gebrauch im G120-Raum bestimmt.

## 🤝 Support

Bei Fragen oder Problemen wenden Sie sich bitte an den Administrator.