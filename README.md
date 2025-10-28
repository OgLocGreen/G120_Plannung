# 🪑 G120 Desk Planning System

A modular Streamlit-based application for managing and planning desk bookings in the G120 room.

## 🎯 Features

- **Desk Management**: Manage 11 desks (Desk 0-10)
- **Three Booking Types**:
  - **Schedule**: Time-slot-based bookings with weekly planning (📅)
  - **Full Booking**: Entire desk booked to one person (👤)
  - **Project**: Desk assigned to a project with contact person (🔵)
- **Computer Management**:
  - Display whether computer is available
  - Computer type: GPU, CPU, or None
  - Custom computer name
  - Shutdown mode: Shutdownable or Training Mode (not shutdownable)
  - Number of screens: 0, 1, or 2
- **Weekly Overview**: Visual display of all bookings per weekday
- **Booking Management**: Add, view, and delete bookings
- **Room View**: Visual overview of all desks with color coding and quick booking access

## 📂 Project Structure

```
G120_Plannung/
├── main.py                          # Main application entry point
├── modules/                         # Application modules
│   ├── __init__.py
│   ├── config.py                   # Configuration constants
│   ├── utils.py                    # Utility functions
│   ├── desk_planning.py            # Desk Planning mode (📋)
│   ├── room_view.py                # Room View mode (🗺️)
│   └── desk_config.py              # Desk Configuration mode (🔧)
├── data/
│   └── tische_config.json          # Desk configuration and bookings
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 📋 Requirements

- Python 3.8 or higher
- pip (Python Package Manager)

## 🚀 Installation & Setup

### 1. Clone or download repository

```bash
git clone <repository-url>
cd G120_Plannung
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
streamlit run main.py
```

The application will open automatically in your browser at `http://localhost:8501`

## 🎮 Application Modes

### � Desk Planning
- **Purpose**: Create and manage desk bookings
- **Features**:
  - Select a desk from the dropdown
  - View current desk information and computer configuration
  - Create schedule bookings with time slots (Mon-Fri, 8:00-18:00)
  - Manage full bookings or project assignments
  - Visual time-slot selection with color coding
  - View and delete existing bookings

**Workflow:**
1. Select a desk from the sidebar
2. Choose booking type based on desk configuration
3. For schedule bookings: click green time-slot buttons to select
4. Enter person name, computer mode, and optional notes
5. Click "💾 Save Bookings" to confirm

### 🗺️ Room View
- **Purpose**: Overview of all desks in the G120 room
- **Features**:
  - Visual representation of all 11 desks
  - Color-coded status indicators:
    - 🟢 Green = Free
    - 🟠 Orange = Partially booked (schedule)
    - 🔴 Red = Fully booked (person or project)
    - 🔵 Blue = Project assigned
  - Quick access buttons to book each desk
  - Direct navigation to Desk Planning mode

**Quick Booking:**
1. Find a desk in the Room View
2. Click "📋 Book Desk X" button
3. Desk is pre-selected in Desk Planning mode
4. Create booking directly

### 🔧 Desk Configuration
- **Purpose**: Configure desks and their computer settings
- **Features**:
  - Edit desk names
  - Change booking type (Schedule, Full Booking, or Project)
  - Configure computer availability and type
  - Set computer name and shutdown mode
  - Configure number of screens
  - View current configuration summary

**Configuration Steps:**
1. Select a desk from the sidebar
2. Edit desk name if needed
3. Choose booking type
4. Configure computer settings (if applicable)
5. Set number of screens
6. Click "💾 Save Changes"

## ⚙️ Configuration Details

### Desk Configuration File

The desk configuration is stored in `data/tische_config.json`. Each desk has the following structure:

```json
{
  "name": "Desk X",
  "typ": "schedule | fullbooking | projekt",
  "rechner": {
    "vorhanden": true/false,
    "typ": "GPU | CPU | Leer",
    "name": "Computer name",
    "abschaltbar": true/false,
    "bildschirme": 0/1/2
  },
  "buchungen": {},           // For schedule-type desks
  "gebucht_von": "",         // For fullbooking and project types
  "projekt_name": ""         // For project-type desks
}
```

### Desk Types Explained

#### Schedule (`schedule`)
- **Use Case**: Shared desk with multiple time-slot bookings
- **Availability**: Monday-Friday, 8:00-18:00
- **Booking**: Multiple persons can book different time slots
- **Features**:
  - Computer mode selection per booking
  - Weekly overview display
  - Time-slot conflict prevention
  - Notes per booking

#### Full Booking (`fullbooking`)
- **Use Case**: Personal desk or room reservation
- **Duration**: Complete desk assignment
- **Booking**: Single person for entire desk
- **Features**:
  - Simple name entry
  - No time restrictions
  - Full desk reservation

#### Project (`projekt`)
- **Use Case**: Project-based desk assignment
- **Duration**: Project duration
- **Booking**: Project name + contact person
- **Features**:
  - Project tracking
  - Contact person management
  - Full desk reservation like full booking

### Computer Configuration

**Computer Availability:**
- `vorhanden`: Boolean - indicates if computer is present at desk
- `typ`: Type of computer
  - `GPU`: Graphics Processing Unit (powerful graphics workstations)
  - `CPU`: Central Processing Unit (standard computers)
  - `Leer`: No computer/empty

- `name`: Custom identifier for the computer
  - Examples: "WorkStation-01", "PC-Lab-01", "Lab-Computer"

**Computer Modes (Shutdown Capability):**
- `abschaltbar: true`: Computer can be shut down by user
- `abschaltbar: false`: Training Mode - computer cannot be shut down (for training purposes)

**Screens:**
- `0`: No screens/displays
- `1`: Single monitor
- `2`: Dual monitor setup

## � Time Slots and Scheduling

### Schedule Booking Time Slots
- **Available Days**: Monday to Friday only
- **Time Range**: 8:00 AM - 6:00 PM (18:00)
- **Slot Duration**: 1 hour
- **Total Slots per Day**: 10 slots
- **Multiple Bookings**: One person can book multiple consecutive or separate slots

### Weekly Display
- Shows all 7 days (Monday-Sunday)
- Displays all time slots including extended hours (8:00-20:00)
- Visual color coding for booked/free slots
- Automatic conflict prevention for schedule bookings

## 🎨 Visual Status Indicators

### Room View Color Coding
- 🟢 **Green**: Desk is completely free and available for booking
- 🟠 **Orange**: Desk has partial schedule bookings (some time slots booked)
- 🔴 **Red**: Desk is fully booked (person reservation or all slots occupied)
- 🔵 **Blue**: Desk is assigned to a project

### Time Slot Button States
- 🟢 **Green Button**: Free time slot - click to select for booking
- 🔴 **Red Button**: Time slot selected - click to deselect
- 🚫 **Gray Button**: Already booked - cannot select (disabled)

## 💾 Data Persistence

All bookings and configurations are automatically saved to `data/tische_config.json` and persist across application restarts. The data file is in JSON format for easy editing and backup.

## 📖 Usage Examples

### Example 1: Create a Schedule Booking
```
1. Navigate to "📋 Desk Planning" mode
2. Select desired desk from sidebar
3. Click "➕ New Booking" tab
4. Enter person name (e.g., "John Doe")
5. Select computer usage mode (if computer available)
6. Click green time-slot buttons for Monday-Friday
7. Review selected slots in the summary
8. Optionally add notes
9. Click "💾 Save Bookings"
```

### Example 2: Assign a Project to a Desk
```
1. Navigate to "🔧 Desk Configuration" mode
2. Select target desk from sidebar
3. Change "Booking Type" dropdown to "projekt"
4. Configure computer settings if needed
5. Click "💾 Save Changes"
6. Navigate back to "📋 Desk Planning"
7. Select the same desk
8. Enter project name (e.g., "AI Research 2025")
9. Enter contact person name (e.g., "Dr. Smith")
10. Click "💾 Save"
```

### Example 3: Quick Booking via Room View
```
1. Navigate to "🗺️ Room View" mode
2. Check desk status indicators and computer types
3. Identify free desk (🟢 Green)
4. Click "📋 Book Desk X" button for desired desk
5. Desk is automatically pre-selected in Desk Planning
6. Create booking details directly
```

### Example 4: View and Modify Existing Bookings
```
1. In "📋 Desk Planning" mode, select desk with bookings
2. Click "📋 All Bookings" tab
3. View all bookings in expandable list
4. Click expander to see booking details
5. Click "🗑️ Delete" button to remove booking if needed
6. Confirm deletion in popup
```

## 🔄 Typical Workflow

```
Check Room Status
    ↓
📋 Desk Planning / 🗺️ Room View (select desk)
    ↓
Create/Modify Booking
    ↓
View Weekly Overview
    ↓
Manage Existing Bookings (edit/delete)
    ↓
Optional: Configure Desk Settings (🔧)
```

## 🛠️ Technical Details

### Module Organization

**main.py**
- Application entry point
- Session state management
- Mode routing and navigation
- Configuration loading

**modules/config.py**
- Central constants definition
- Time slots and weekdays
- Desk types and computer types
- Screen count options

**modules/utils.py**
- Shared utility functions
- Configuration I/O operations
- Status determination logic
- Reusable helper functions

**modules/desk_planning.py**
- Schedule booking management
- Full booking interface
- Project booking interface
- Weekly view and time-slot selection

**modules/room_view.py**
- Visual desk overview
- Status color coding
- Quick navigation buttons
- Desk information display

**modules/desk_config.py**
- Configuration form interface
- Computer settings management
- Desk type selection
- Validation and save logic

### Adding New Desks

The system automatically scales. To add desks:

1. **Manual Addition**: Edit `data/tische_config.json` directly
2. **Auto-detection**: System reads all desks in JSON file
3. **Room View Layout**: Modify grid layout in `modules/room_view.py` if needed

Example JSON entry:
```json
"11": {
  "name": "Desk 11",
  "typ": "schedule",
  "rechner": {
    "vorhanden": true,
    "typ": "GPU",
    "name": "WorkStation-06",
    "abschaltbar": true,
    "bildschirme": 2
  },
  "buchungen": {}
}
```

### Extending Features

To add new booking types or modes:

1. Add new type to `modules/config.py`
2. Create new module `modules/new_feature.py`
3. Define mode function: `show_new_feature_mode(config, tische)`
4. Import in `main.py` and add to router
5. Test and commit

## ❓ Troubleshooting

### Application won't start
**Problem**: Streamlit command not found or ModuleNotFoundError
**Solution**:
```bash
pip install -r requirements.txt
python -m streamlit run main.py
```

### Data not saving
**Problem**: Bookings disappear after refresh
**Solution**:
- Check that `data/` directory exists
- Verify write permissions: `ls -l data/`
- Ensure `tische_config.json` has valid JSON syntax
- Check disk space availability

### Computer configuration not visible
**Problem**: Computer settings not showing in Desk Planning
**Solution**:
1. Go to "🔧 Desk Configuration"
2. Select the desk
3. Enable "Computer available" checkbox
4. Save changes
5. Switch back to "📋 Desk Planning" and refresh

### Time slots not selectable
**Problem**: All time slots appear gray/disabled
**Solution**:
- Verify desk type is set to "schedule" (not "fullbooking" or "projekt")
- Check that time slots aren't already fully booked
- Clear browser cache and refresh page

### Desk information not updating
**Problem**: Changes made in config mode not showing in planning
**Solution**:
- Use "💾 Save Changes" button
- Wait for "✅ Saved successfully" confirmation
- Refresh page if needed: F5
- Check browser console for errors

## 📝 Notes

- All times are in 24-hour format (8:00 = 8:00 AM, 18:00 = 6:00 PM)
- Bookings are stored in local JSON file - consider backups for production
- Computer names are for identification only and don't affect functionality
- Project assignments are full-desk reservations similar to full bookings

## 📞 Support & Feedback

For issues, feature requests, or improvements:
- Contact the administrator
- Check logs in browser console (F12)
- Verify configuration file integrity

## 📄 License

This project is for internal use in the G120 room only.

---

**Last Updated**: October 2025  
**Version**: 2.0  
**Status**: Stable - Modular Architecture  
**Language**: English (Fully Translated)