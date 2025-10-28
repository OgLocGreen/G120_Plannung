"""
Configuration constants for G120 Desk Planning System
"""

# Data file
DATA_FILE = "data/tische_config.json"

# Weekdays
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
WEEKDAYS_ALL = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Time slots
TIMESLOTS_BOOKING = [f"{h:02d}:00-{h+1:02d}:00" for h in range(8, 18)]
TIMESLOTS = [f"{h:02d}:00-{h+1:02d}:00" for h in range(8, 20)]

# Desk types
DESK_TYPES = ["schedule", "fullbooking", "projekt"]

# Computer types
COMPUTER_TYPES = ["GPU", "CPU", "None"]

# Screen counts
SCREEN_COUNTS = [0, 1, 2]
