from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    # Initial setup
    SETUP_INTRO = State()
    SETUP_ADD_TASK = State()
    SETUP_CONFIRM = State()
    
    # Main menu
    MENU = State()
    
    # During routine
    ROUTINE_ACTIVE = State()
    ROUTINE_ACTIVE_WAITING = State()  # ADD THIS LINE
    
    # Stats
    STATS_VIEW = State()
    
    # Settings
    SETTINGS = State()
    SETTINGS_EDIT_ROUTINE = State()
    SETTINGS_CUSTOMIZE_REPLIES = State()  # ADD THIS LINE
    SETTINGS_EDIT_TASK = State()  # For editing individual tasks
    SETTINGS_EDIT_WINDOW = State()
    SETTINGS_EDIT_TIMEZONE = State()
