import os

# Overrideable app settings for things like gameplay values and other stuff we want easy access to

PLAYER_MAX_MOVES = int(os.getenv("PLAYER_MAX_MOVES", "3"))
PLAYER_MAX_IDLE_SECONDS = int(os.getenv("PLAYER_MAX_IDLE_SECONDS", "300"))

PUSHER_APP_ID =  os.getenv('PUSHER_APP_ID', '41450')
PUSHER_KEY = os.getenv('PUSHER_KEY', 'ae35d633bac49aecadaf')
PUSHER_SECRET = os.getenv('PUSHER_SECRET', '0aeed0cdd5cfe2fd5acd')