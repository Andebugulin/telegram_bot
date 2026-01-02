import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import asyncio
from aiogram import Bot, Dispatcher, types, F
import json
from dotenv import load_dotenv
import datetime
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from states_dir.statesform import StepsForm
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from classes_dir.morning_routine_class import MorningRoutine
import pytz

# Load environment
load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)

# Bot initialization
bot_token = str(os.getenv("BOT_TOKEN"))
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# ═══════════════════════════════════════════════════════════════
# UI DESIGN VARIABLES - Change all visual elements here
# ═══════════════════════════════════════════════════════════════

# Box characters
BOX_TOP = "━"
BOX_SIDE = ""
BOX_CORNER_TL = "┏"
BOX_CORNER_TR = " "
BOX_CORNER_BL = "┗"
BOX_CORNER_BR = ""

# Separators
SEPARATOR_LIGHT = "─────────────────────"
SEPARATOR_HEAVY = "━━━━━━━━━━━━━━━━━━━━"

# Progress bar characters
PROGRESS_FILL = "█"
PROGRESS_EMPTY = "░"

# Status icons
ICON_COMPLETE = "✓"
ICON_INCOMPLETE = "○"
ICON_PARTIAL = "◐"
ICON_MISSED = "⭘"
ICON_FUTURE = "·"
ICON_STREAK = "🔥"
ICON_TROPHY = "🏆"

# Calendar symbols
CAL_COMPLETE = "●"
CAL_PARTIAL = "◐"
CAL_INCOMPLETE = "○"
CAL_MISSED = "×"
CAL_FUTURE = "·"

# Spacing character (zero-width space doesn't work, use thin space)
SP = "\u2009"  # Thin space that Telegram respects

# Helper functions for UI
def make_header(text):
    """Create centered header box"""
    padding = 2 
    padded_text = " " * padding + text + " " * (20 - len(text) - padding)
    return f"{BOX_CORNER_TL}{BOX_TOP}{BOX_CORNER_TR}\n{BOX_SIDE}*{padded_text}*{BOX_SIDE}\n{BOX_CORNER_BL}{BOX_TOP}{BOX_CORNER_BR}\n"

def make_progress_bar(percentage, length=20):
    """Create progress bar"""
    filled = int((percentage / 100) * length)
    return PROGRESS_FILL * filled + PROGRESS_EMPTY * (length - filled)

def make_streak_bar(streak, max_icons=10):
    """Create streak visualization"""
    display_count = min(streak, max_icons)
    return ICON_STREAK * display_count

# ═══════════════════════════════════════════════════════════════
# END UI DESIGN VARIABLES
# ═══════════════════════════════════════════════════════════════

# Global storage
routines_dict: dict[int, MorningRoutine] = {}
FILE_NAME = './routines_data.json'

# Customizable quick replies for watches
DEFAULT_REPLIES = ["Done", "Next", "Complete", "Ok", "Great"]
user_replies: dict[int, list[str]] = {}  # chat_id -> list of replies

@dp.message(Command("start", "restart"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    chat_id = message.from_user.id
    
    print(f"\n=== START command from {chat_id} ===\n")
    
    # Initialize routine if new user
    if chat_id not in routines_dict:
        routines_dict[chat_id] = MorningRoutine(chat_id)
        user_replies[chat_id] = DEFAULT_REPLIES.copy()
        await state.set_state(StepsForm.SETUP_INTRO)
        
        intro_text = make_header("MORNING ROUTINE") + """
Build consistent habits
Track your progress

Ready to begin?
"""
        
        markup = ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=[[KeyboardButton(text="Start")]],
            one_time_keyboard=True
        )
        
        await bot.send_message(chat_id, intro_text, reply_markup=markup)
    else:
        # Existing user - go to menu
        await show_main_menu(chat_id, state)

@dp.message(StepsForm.SETUP_INTRO, F.text == "Start")
async def setup_start(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    await state.set_state(StepsForm.SETUP_ADD_TASK)
    
    text = make_header("ADD TASKS") + """
    *Format:*
    `task` `minutes`

    *Examples:*
    `Wake up 2`
    `Exercise 15`
    `Breakfast 30`

    *Optional task:*
    `Shower 10 optional`

    Send your first task:
    """
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text="Wake up 2")]],
        one_time_keyboard=False
    )
    
    await bot.send_message(chat_id, text, reply_markup=markup)

@dp.message(StepsForm.SETUP_ADD_TASK)
async def setup_add_task_or_finish(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    text = message.text.strip()
    
    # Handle finish setup
    if text == "Finish":
        if len(routine.tasks) == 0:
            await bot.send_message(chat_id, "`Add at least one task`")
            return
        
        routine.is_setup_complete = True
        save_routines()
        
        await show_main_menu(chat_id, state)
        
        await bot.send_message(
            chat_id,
            "*Setup complete*\n\nStart your routine between `05:00 \\- 11:00`"
        )
        return
    
    # Handle add another task
    if text == "+ Add":
        await bot.send_message(
            chat_id,
            "Send next task:\n`task name` `minutes`"
        )
        return
    
    # Handle adding a task
    try:
        parts = text.strip().split()
        
        # Check if last part is "optional"
        optional = False
        if parts[-1].lower() == "optional":
            optional = True
            parts = parts[:-1]
        
        # Last part should be duration
        duration = int(parts[-1])
        task_name = " ".join(parts[:-1])
        
        if routine.add_task(task_name, duration, optional):
            current_tasks = routine.get_status_display()
            
            opt_label = " `opt`" if optional else ""
            response_text = f"✓ *Added:* {task_name} `{duration}m`{opt_label}\n\n{SEPARATOR_HEAVY}\n\n{current_tasks}"
            
            markup = ReplyKeyboardMarkup(
                resize_keyboard=True,
                keyboard=[
                    [KeyboardButton(text="+ Add")],
                    [KeyboardButton(text="Finish")]
                ],
                one_time_keyboard=False
            )
            
            await bot.send_message(chat_id, response_text, reply_markup=markup)
        else:
            await bot.send_message(chat_id, "`Max 15 tasks\\. Finish setup\\.`")
    
    except (ValueError, IndexError):
        await bot.send_message(
            chat_id, 
            "`Invalid format`\nUse: `task name` `minutes`"
        )


async def show_main_menu(chat_id: int, state: FSMContext):
    await state.set_state(StepsForm.MENU)
    routine = routines_dict[chat_id]
    
    # Get current time in user's timezone
    user_tz = pytz.timezone(routine.timezone)
    now = datetime.datetime.now(user_tz)
    current_minutes = now.hour * 60 + now.minute
    start_minutes = routine.window_start * 60 + routine.window_start_minute
    end_minutes = routine.window_end * 60 + routine.window_end_minute
    
    # CRITICAL: If outside window and routine started, force finish
    if current_minutes >= end_minutes:
        if routine.routine_started:
            routine.finish_routine()
            save_routines()
            
            completion = routine.get_completion_percentage()
            await bot.send_message(
                chat_id,
                f"*Window closed*\n\n`{completion:.0f}% complete`\n{'Streak maintained' if completion >= 100 else 'Streak reset'}",
            )
    
    status = routine.get_status_display()
    buttons = []
    
    # ONLY show start/continue if IN window
    if current_minutes >= start_minutes and current_minutes < end_minutes:
        if not routine.routine_started:
            buttons.append([KeyboardButton(text="Start Routine")])
        else:
            buttons.append([KeyboardButton(text="Continue")])
    
    buttons.extend([
        [KeyboardButton(text="Stats"), KeyboardButton(text="Settings")]
    ])
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    await bot.send_message(chat_id, status, reply_markup=markup)

@dp.message(StepsForm.MENU, F.text == "Start Routine")
async def start_routine(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    
    print(f"\n[START ROUTINE] Called by {chat_id}")
    
    if not routine.can_start_routine():
        user_tz = pytz.timezone(routine.timezone)
        now = datetime.datetime.now(user_tz)
        print(f"[START ROUTINE] Cannot start - outside window")
        await bot.send_message(
            chat_id,
            f"`Window: {routine.window_start:02d}:{routine.window_start_minute:02d} - {routine.window_end:02d}:{routine.window_end_minute:02d}`\n`Now: {now.strftime('%H:%M')}`"
        )
        return
    
    if routine.start_routine():
        print(f"[START ROUTINE] Success - starting tasks")
        await state.set_state(StepsForm.ROUTINE_ACTIVE)
        save_routines()
        await send_next_task(chat_id, state)
    else:
        print(f"[START ROUTINE] Failed")
        await bot.send_message(chat_id, "`Could not start routine`")


@dp.message(StepsForm.MENU, F.text == "Continue")
async def continue_routine(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    await state.set_state(StepsForm.ROUTINE_ACTIVE)
    await send_next_task(chat_id, state)


async def send_next_task(chat_id: int, state: FSMContext):
    """Send next uncompleted task - watch-friendly"""
    routine = routines_dict[chat_id]
    
    # CHECK IF STILL IN WINDOW
    user_tz = pytz.timezone(routine.timezone)
    now = datetime.datetime.now(user_tz)
    current_minutes = now.hour * 60 + now.minute
    end_minutes = routine.window_end * 60 + routine.window_end_minute
    
    if current_minutes >= end_minutes:
        # Window closed! Force finish
        routine.finish_routine()
        save_routines()
        await bot.send_message(chat_id, "*Window closed*\n\nRoutine finished\\.")
        await show_main_menu(chat_id, state)
        return
    
    # Find next uncompleted AND not skipped task
    next_task = None
    task_num = None
    for i, task in enumerate(routine.tasks):
        if not task.completed and not task.skipped:
            next_task = task
            task_num = i + 1
            break
    
    if next_task:
        await state.set_state(StepsForm.ROUTINE_ACTIVE_WAITING)
        
        # Calculate based on ALL tasks (not just required)
        total_tasks = len(routine.tasks)
        completed_tasks = sum(1 for t in routine.tasks if t.completed)
        skipped_tasks = sum(1 for t in routine.tasks if t.skipped)
        remaining = total_tasks - completed_tasks - skipped_tasks
        completion = ((completed_tasks + skipped_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
        
        opt_label = " `opt`" if next_task.optional else ""
        notes_text = f"\n_{next_task.notes}_\n" if next_task.notes else "\n"
        
        # Progress bar based on completion percentage
        progress_bar = make_progress_bar(completion, 20)
        
        text = make_header(f"TASK {task_num}") + f"""
*{next_task.name}*
`{next_task.duration} minutes`{opt_label}
{notes_text}
{progress_bar}
`{completion:.0f}%` · `{remaining} left`
"""
        
        replies = user_replies.get(chat_id, DEFAULT_REPLIES)
        buttons = [[KeyboardButton(text=reply)] for reply in replies[:3]]
        buttons.append([KeyboardButton(text="Skip")])
        buttons.append([KeyboardButton(text="Menu")])
        
        markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
        
        await bot.send_message(chat_id, text, reply_markup=markup, disable_notification=True)
    else:
        await finish_routine_confirmed(chat_id, state)

@dp.message(StepsForm.ROUTINE_ACTIVE_WAITING)
async def handle_task_response(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    text = message.text.strip()
    
    if text == "Menu":
        await show_main_menu(chat_id, state)
        return
    
    if text == "Skip":
        # Mark current task as skipped (counts as failed)
        for i, task in enumerate(routine.tasks):
            if not task.completed and not task.skipped:
                task.skipped = True
                save_routines()
                break
        
        await send_next_task(chat_id, state)
        return
    
    # Any other response = task completed
    # Find current uncompleted task
    for i, task in enumerate(routine.tasks):
        if not task.completed and not task.skipped:
            routine.complete_task(i)
            save_routines()
            break
    
    # Send next task
    await send_next_task(chat_id, state)


# Keep the old handler for direct access
@dp.message(StepsForm.ROUTINE_ACTIVE)
async def handle_routine_action(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    text = message.text.strip()
    
    if text == "Menu":
        await show_main_menu(chat_id, state)
    else:
        await send_next_task(chat_id, state)


async def finish_routine_confirmed(chat_id: int, state: FSMContext):
    routine = routines_dict[chat_id]
    routine.finish_routine()
    save_routines()
    
    completion = routine.get_completion_percentage()
    
    if completion >= 100:
        progress_bar = make_progress_bar(completion, 20)
        streak_bar = make_streak_bar(routine.current_streak, 10)
        
        duration = routine.history[datetime.date.today().isoformat()]['duration']
        
        message = make_header("✓ COMPLETE") + f"""
{progress_bar}
`{completion:.0f}%`

{streak_bar}
*{routine.current_streak} day streak*

Duration: `{duration} min`

_{get_encouragement_message(routine.current_streak)}_
"""
    else:
        message = make_header("FINISHED") + f"""
`{completion:.0f}% complete`

Streak reset
Tomorrow is a fresh start
"""
    
    await show_main_menu(chat_id, state)
    await bot.send_message(chat_id, message)

def get_encouragement_message(streak: int) -> str:
    """Return encouraging message based on streak"""
    if streak == 1:
        return "Day one"
    elif streak == 3:
        return "Momentum building"
    elif streak == 7:
        return "One week"
    elif streak == 14:
        return "Two weeks strong"
    elif streak == 30:
        return "One month"
    elif streak == 60:
        return "Two months"
    elif streak == 90:
        return "Three months"
    else:
        return "Keep going"

@dp.message(StepsForm.MENU, F.text == "Stats")
async def view_stats(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    
    await state.set_state(StepsForm.STATS_VIEW)
    
    stats = routine.get_weekly_stats()
    visual = create_week_visual(routine)
    
    weekly_bar = make_progress_bar((stats['completed_days'] / 7) * 100, 20)
    
    stats_text = make_header("STATISTICS") + f"""
*Last 7 Days*
{visual}

`{stats['completed_days']}/7` · `{stats['avg_completion']:.0f}%`
{weekly_bar}

{SEPARATOR_LIGHT}

*Streaks*
Current:  `{stats['current_streak']}d` {ICON_STREAK}
Best:       `{stats['best_streak']}d` {ICON_TROPHY}
Total:      `{stats['total_completions']}`

_{get_weekly_insights(stats)}_
"""
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Month"), KeyboardButton(text="Menu")]
        ]
    )
    
    await bot.send_message(chat_id, stats_text, reply_markup=markup)

def create_week_visual(routine: MorningRoutine) -> str:
    """Create visual representation of last 7 days"""
    emojis = []
    labels = []
    
    for i in range(6, -1, -1):
        date = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
        day_data = routine.history.get(date, {'completion': 0})
        
        completion = day_data.get('completion', 0)
        if day_data.get('missed', False):
            emoji = CAL_MISSED + ' '
        elif completion >= 100:
            emoji = CAL_COMPLETE + ' '
        elif completion > 0:
            emoji = CAL_PARTIAL + ' '
        else:
            emoji = CAL_INCOMPLETE + ' '
        
        day_name = (datetime.date.today() - datetime.timedelta(days=i)).strftime('%a')[:2].upper()
        labels.append(day_name)
        emojis.append(emoji)
    
    # Use code block for perfect alignment
    label_line = " ".join(labels)
    emoji_line = " ".join(emojis)
    
    return f"```\n{label_line}\n{emoji_line}\n```"

def get_weekly_insights(stats: dict) -> str:
    """Generate personalized insights"""
    completed = stats['completed_days']
    
    if completed == 7:
        return "`Perfect week`"
    elif completed >= 5:
        return "`Strong consistency`"
    elif completed >= 3:
        return "`Building habit`"
    elif completed >= 1:
        return "`Keep building`"
    else:
        return "`Fresh start`"


@dp.message(StepsForm.STATS_VIEW, F.text == "Month")
async def monthly_view(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    
    month_visual = create_month_visual(routine)
    month_stats = get_month_stats(routine)
    
    month_name = datetime.date.today().strftime('%B %Y').upper()
    
    text = make_header(month_name) + f"""
{month_visual}

{month_stats}
"""
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text="Back")]]
    )
    
    await bot.send_message(chat_id, text, reply_markup=markup)

def create_month_visual(routine: MorningRoutine) -> str:
    """Create calendar-style month view with proper alignment"""
    today = datetime.date.today()
    first_day = today.replace(day=1)
    
    # Calculate last day of month
    if today.month == 12:
        last_day = today.replace(year=today.year + 1, month=1, day=1) - datetime.timedelta(days=1)
    else:
        last_day = today.replace(month=today.month + 1, day=1) - datetime.timedelta(days=1)
    
    lines = []
    
    # Header with day labels in monospace (each label is 2 chars)
    lines.append("`Mo Tu We Th Fr Sa Su`\n")
    
    # Start from Monday of the week containing first day
    current = first_day - datetime.timedelta(days=first_day.weekday())
    week_emojis = []
    
    while current <= last_day:
        if current.month == today.month:
            if current <= today:
                day_data = routine.history.get(current.isoformat(), {})
                completion = day_data.get('completion', 0)
                
                if day_data.get('missed', False):
                    emoji = f"`{CAL_MISSED} `"
                elif completion >= 100:
                    emoji = f"`{CAL_COMPLETE} `"
                elif completion > 0:
                    emoji = f"`{CAL_PARTIAL} `"
                else:
                    emoji = f"`{CAL_INCOMPLETE} `"
            else:
                emoji = f"`{CAL_FUTURE} `"  # Future days
        else:
            emoji = "`\u2009\u2009`"  # Empty slot = 3 thin spaces to match "Mo "
        
        week_emojis.append(emoji)
        
        if len(week_emojis) == 7:
            # Each emoji + 3 spaces to match 2-char day label + space
            lines.append("\u2009\u2009\u2009".join(week_emojis) + "\n")
            week_emojis = []
        
        current += datetime.timedelta(days=1)
    
    # Add remaining days if any
    if week_emojis:
        while len(week_emojis) < 7:
            week_emojis.append("\u2009\u2009\u2009")
        lines.append("\u2009\u2009\u2009".join(week_emojis) + "\n")
    
    return "".join(lines)

def get_month_stats(routine: MorningRoutine) -> str:
    """Calculate current month statistics"""
    today = datetime.date.today()
    first_day = today.replace(day=1)
    
    completed = 0
    total_days = 0
    
    current = first_day
    while current <= today:
        total_days += 1
        day_data = routine.history.get(current.isoformat(), {})
        if day_data.get('completion', 0) >= 80:
            completed += 1
        current += datetime.timedelta(days=1)
    
    rate = (completed / total_days * 100) if total_days > 0 else 0
    month_bar = make_progress_bar(rate, 20)
    
    return f"""`{completed}/{total_days}` · `{rate:.0f}%`
{month_bar}

{SEPARATOR_LIGHT}

*Legend*
{CAL_COMPLETE} Done  {CAL_PARTIAL} Partial  {CAL_INCOMPLETE} Missed"""

@dp.message(StepsForm.STATS_VIEW, F.text == "Back")
async def back_to_stats(message: types.Message, state: FSMContext):
    await view_stats(message, state)


@dp.message(StepsForm.STATS_VIEW, F.text == "Menu")
async def stats_to_menu(message: types.Message, state: FSMContext):
    await show_main_menu(message.from_user.id, state)

@dp.message(StepsForm.MENU, F.text == "Settings")
async def show_settings(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    await state.set_state(StepsForm.SETTINGS)
    
    text = make_header("SETTINGS") + """
Configure your routine
Customize experience
"""
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Edit Routine")],
            [KeyboardButton(text="Quick Replies"), KeyboardButton(text="Time Window")],
            [KeyboardButton(text="Timezone")],
            [KeyboardButton(text="Reset"), KeyboardButton(text="Delete All")],
            [KeyboardButton(text="Menu")]
        ]
    )
    
    await bot.send_message(chat_id, text, reply_markup=markup)

@dp.message(StepsForm.SETTINGS, F.text == "Quick Replies")
async def customize_replies(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    await state.set_state(StepsForm.SETTINGS_CUSTOMIZE_REPLIES)
    
    current = user_replies.get(chat_id, DEFAULT_REPLIES)
    
    text = make_header("QUICK REPLIES") + f"""
Customize watch responses

*Current:*
`{', '.join(current)}`

*Format:*
3-5 short words, comma separated

*Example:*
`Done, Next, Ok`
"""
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Done, Next, Great")],
            [KeyboardButton(text="Back")]
        ]
    )
    
    await bot.send_message(chat_id, text, reply_markup=markup)

@dp.message(StepsForm.SETTINGS, F.text == "Edit Routine")
async def edit_routine(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    
    await state.set_state(StepsForm.SETTINGS_EDIT_ROUTINE)
    
    # Calculate max name length for alignment
    if routine.tasks:
        max_name_length = max(len(t.name) for t in routine.tasks)
    else:
        max_name_length = 0
    
    # Build task list with monospace alignment
    task_lines = []
    for i, task in enumerate(routine.tasks):
        padding = max_name_length - len(task.name)
        spaces = "\u2009" * padding
        opt_label = "  opt" if task.optional else ""
        task_lines.append(f"`{i+1}. {task.name}{spaces}  {task.duration}m{opt_label}`")
    
    tasks_list = "\n".join(task_lines)
    
    text = make_header("EDIT ROUTINE") + f"""
*Your Tasks:*
{tasks_list}

{SEPARATOR_LIGHT}

*Commands:*
`delete N` - remove task N
`edit N` - modify task N
`move N M` - reorder (N to pos M)
`add name duration` - add task
`add name duration optional`
"""
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="edit 1")],
            [KeyboardButton(text="Back")]
        ]
    )
    
    await bot.send_message(chat_id, text, reply_markup=markup)


@dp.message(StepsForm.SETTINGS_EDIT_ROUTINE)
async def handle_edit_routine(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    text = message.text.strip().lower()
    
    if text == "back":
        await show_settings(message, state)
        return
    
    parts = text.split()
    
    # Delete task: "delete 1"
    if parts[0] == "delete" and len(parts) == 2:
        try:
            task_num = int(parts[1]) - 1
            if routine.remove_task(task_num):
                save_routines()
                await bot.send_message(chat_id, "`Removed`")
                await edit_routine(message, state)
            else:
                await bot.send_message(chat_id, "`Invalid number`")
        except ValueError:
            await bot.send_message(chat_id, "`Invalid format`")
    
    # Edit task: "edit 1"
    elif parts[0] == "edit" and len(parts) == 2:
        try:
            task_num = int(parts[1]) - 1
            if 0 <= task_num < len(routine.tasks):
                await state.update_data(editing_task_index=task_num)
                await state.set_state(StepsForm.SETTINGS_EDIT_TASK)
                
                task = routine.tasks[task_num]
                text = make_header(f"EDIT TASK {task_num + 1}") + f"""
*Current:*
Name: `{task.name}`
Duration: `{task.duration}m`
Optional: `{task.optional}`
Notes: `{task.notes or 'none'}`

{SEPARATOR_LIGHT}

*Change property:*
`name new name here`
`duration 15`
`optional true/false`
`notes your note here`
"""
                
                markup = ReplyKeyboardMarkup(
                    resize_keyboard=True,
                    keyboard=[
                        [KeyboardButton(text="name Wake up early")],
                        [KeyboardButton(text="duration 30")],
                        [KeyboardButton(text="Done"), KeyboardButton(text="Back")]
                    ]
                )
                
                await bot.send_message(chat_id, text, reply_markup=markup)
            else:
                await bot.send_message(chat_id, "`Invalid task number`")
        except ValueError:
            await bot.send_message(chat_id, "`Invalid format`")
    
    # Move task: "move 1 3"
    elif parts[0] == "move" and len(parts) == 3:
        try:
            from_idx = int(parts[1]) - 1
            to_idx = int(parts[2]) - 1
            if routine.move_task(from_idx, to_idx):
                save_routines()
                await bot.send_message(chat_id, "`Moved`")
                await edit_routine(message, state)
            else:
                await bot.send_message(chat_id, "`Invalid positions`")
        except ValueError:
            await bot.send_message(chat_id, "`Invalid format`")
    
    # Add task: "add taskname 30" or "add taskname 30 optional"
    elif parts[0] == "add" and len(parts) >= 3:
        try:
            optional = parts[-1] == "optional"
            if optional:
                parts = parts[:-1]
            
            duration = int(parts[-1])
            task_name = " ".join(parts[1:-1])
            
            success, error = routine.add_task(task_name, duration, optional)
            if success:
                save_routines()
                await bot.send_message(chat_id, f"`Added: {task_name}`")
                await edit_routine(message, state)
            else:
                await bot.send_message(chat_id, f"`{error}`")
        except (ValueError, IndexError):
            await bot.send_message(chat_id, "`Invalid format`")
    else:
        await bot.send_message(chat_id, "`Invalid command`")


@dp.message(StepsForm.SETTINGS_EDIT_TASK)
async def handle_edit_task_property(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    text = message.text.strip()
    
    if text.lower() == "back":
        await state.set_state(StepsForm.SETTINGS_EDIT_ROUTINE)
        await edit_routine(message, state)
        return
    
    if text.lower() == "done":
        save_routines()
        await state.set_state(StepsForm.SETTINGS_EDIT_ROUTINE)
        await bot.send_message(chat_id, "`Changes saved`")
        await edit_routine(message, state)
        return
    
    data = await state.get_data()
    task_idx = data.get('editing_task_index')
    
    if task_idx is None:
        await bot.send_message(chat_id, "`Error: no task selected`")
        return
    
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await bot.send_message(chat_id, "`Format: property value`")
        return
    
    prop, value = parts[0].lower(), parts[1]
    
    if prop == "name":
        success, error = routine.edit_task(task_idx, name=value)
    elif prop == "duration":
        try:
            success, error = routine.edit_task(task_idx, duration=int(value))
        except ValueError:
            await bot.send_message(chat_id, "`Duration must be a number`")
            return
    elif prop == "optional":
        optional_val = value.lower() in ['true', 'yes', '1']
        success, error = routine.edit_task(task_idx, optional=optional_val)
    elif prop == "notes":
        success, error = routine.edit_task(task_idx, notes=value)
    else:
        await bot.send_message(chat_id, "`Unknown property`")
        return
    
    if success:
        await bot.send_message(chat_id, f"`Updated {prop}`")
    else:
        await bot.send_message(chat_id, f"`{error}`")


# Add pause/resume functionality to routine handlers:

@dp.message(StepsForm.ROUTINE_ACTIVE_WAITING)
async def handle_task_response(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    text = message.text.strip()
    
    if text == "Menu":
        await show_main_menu(chat_id, state)
        return
    
    if text == "Skip":
        await send_next_task(chat_id, state)
        return
    
    # Any other response = complete task
    for i, task in enumerate(routine.tasks):
        if not task.completed:
            routine.complete_task(i)
            save_routines()
            break
    
    await send_next_task(chat_id, state)


async def send_next_task(chat_id: int, state: FSMContext):
    routine = routines_dict[chat_id]
    
    # Find next uncompleted AND not skipped task
    next_task = None
    task_num = None
    for i, task in enumerate(routine.tasks):
        print(f"DEBUG: Task {i}: {task.name}, completed={task.completed}, skipped={task.skipped}")
        if not task.completed and not task.skipped:
            next_task = task
            task_num = i + 1
            print(f"DEBUG: Selected task {i}: {task.name}")
            break
    
    if next_task:
        await state.set_state(StepsForm.ROUTINE_ACTIVE_WAITING)
        
        # Calculate based on ALL tasks (not just required)
        total_tasks = len(routine.tasks)
        completed_tasks = sum(1 for t in routine.tasks if t.completed)
        skipped_tasks = sum(1 for t in routine.tasks if t.skipped)
        remaining = total_tasks - completed_tasks - skipped_tasks
        completion = ((completed_tasks + skipped_tasks) / total_tasks) * 100 if total_tasks > 0 else 0
        
        opt_label = " `opt`" if next_task.optional else ""
        notes_text = f"\n_{next_task.notes}_\n" if next_task.notes else "\n"
        
        # Progress bar based on completion percentage
        progress_bar = make_progress_bar(completion, 20)
        
        text = make_header(f"TASK {task_num}") + f"""
*{next_task.name}*
`{next_task.duration} minutes`{opt_label}
{notes_text}
{progress_bar}
`{completion:.0f}%` · `{remaining} left`
"""
        
        replies = user_replies.get(chat_id, DEFAULT_REPLIES)
        buttons = [[KeyboardButton(text=reply)] for reply in replies[:3]]
        buttons.append([KeyboardButton(text="Skip")])
        buttons.append([KeyboardButton(text="Menu")])
        
        markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
        
        await bot.send_message(chat_id, text, reply_markup=markup, disable_notification=True)
    else:
        await finish_routine_confirmed(chat_id, state)


# Add time window customization:

@dp.message(StepsForm.SETTINGS, F.text == "Time Window")
async def customize_window(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    
    await state.set_state(StepsForm.SETTINGS_EDIT_WINDOW)
    
    text = make_header("TIME WINDOW") + f"""
*Current:*
`{routine.window_start:02d}:{routine.window_start_minute:02d} - {routine.window_end:02d}:{routine.window_end_minute:02d}`

{SEPARATOR_LIGHT}

*Change window:*
`window 6 12` (6:00 AM - 12:00 PM)
`window 6:30 12:45` (6:30 AM - 12:45 PM)

Hours: 0-23, Minutes: 0-59
"""
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="window 6:30 12")],
            [KeyboardButton(text="Back")]
        ]
    )
    
    await bot.send_message(chat_id, text, reply_markup=markup)


@dp.message(StepsForm.SETTINGS_EDIT_WINDOW)
async def handle_window_change(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    text = message.text.strip().lower()
    
    if text == "back":
        await show_settings(message, state)
        return
    
    parts = text.split()
    if len(parts) == 3 and parts[0] == "window":
        try:
            # Parse start time
            if ':' in parts[1]:
                start_parts = parts[1].split(':')
                start_hour = int(start_parts[0])
                start_minute = int(start_parts[1])
            else:
                start_hour = int(parts[1])
                start_minute = 0
            
            # Parse end time
            if ':' in parts[2]:
                end_parts = parts[2].split(':')
                end_hour = int(end_parts[0])
                end_minute = int(end_parts[1])
            else:
                end_hour = int(parts[2])
                end_minute = 0
            
            # Validate
            if not (0 <= start_hour < 24 and 0 <= start_minute < 60):
                await bot.send_message(chat_id, "`Invalid start time`")
                return
            
            if not (0 <= end_hour <= 24 and 0 <= end_minute < 60):
                await bot.send_message(chat_id, "`Invalid end time`")
                return
            
            # Compare as total minutes
            start_total = start_hour * 60 + start_minute
            end_total = end_hour * 60 + end_minute
            
            if start_total >= end_total:
                await bot.send_message(chat_id, "`Start must be before end`")
                return
            
            routine.window_start = start_hour
            routine.window_start_minute = start_minute
            routine.window_end = end_hour
            routine.window_end_minute = end_minute
            save_routines()
            
            await bot.send_message(
                chat_id, 
                f"`Window: {start_hour:02d}:{start_minute:02d} - {end_hour:02d}:{end_minute:02d}`"
            )
            await show_settings(message, state)
            
        except (ValueError, IndexError):
            await bot.send_message(chat_id, "`Invalid format`")
    else:
        await bot.send_message(chat_id, "`Format: window START END`\n`Example: window 6:30 12:45`")


# Update settings menu to include new options:

@dp.message(StepsForm.MENU, F.text == "Settings")
async def show_settings(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    await state.set_state(StepsForm.SETTINGS)
    
    text = make_header("SETTINGS") + """
Configure your routine
Customize experience
"""
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Edit Routine")],
            [KeyboardButton(text="Quick Replies"), KeyboardButton(text="Time Window")],
            [KeyboardButton(text="Timezone")],
            [KeyboardButton(text="Reset"), KeyboardButton(text="Delete All")],
            [KeyboardButton(text="Menu")]
        ],
        one_time_keyboard=False
    )
    
    await bot.send_message(chat_id, text, reply_markup=markup)


# Update menu to show "Resume" button if paused:

async def show_main_menu(chat_id: int, state: FSMContext):
    await state.set_state(StepsForm.MENU)
    routine = routines_dict[chat_id]
    
    status = routine.get_status_display()
    
    buttons = []
    
    if routine.can_start_routine() and not routine.routine_started:
        buttons.append([KeyboardButton(text="Start Routine")])
    elif routine.routine_started:
        buttons.append([KeyboardButton(text="Continue")])
    
    buttons.extend([
        [KeyboardButton(text="Stats"), KeyboardButton(text="Settings")]
    ])
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons)
    
    await bot.send_message(chat_id, status, reply_markup=markup)

@dp.message(StepsForm.SETTINGS_CUSTOMIZE_REPLIES)
async def handle_customize_replies(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    text = message.text.strip()
    
    if text == "Back":
        await show_settings(message, state)
        return
    
    # Parse comma-separated replies
    replies = [r.strip() for r in text.split(',') if r.strip()]
    
    if 3 <= len(replies) <= 5:
        user_replies[chat_id] = replies
        save_routines()
        await bot.send_message(chat_id, f"`Updated: {', '.join(replies)}`")
        await show_settings(message, state)
    else:
        await bot.send_message(chat_id, "`Send 3\\-5 words separated by commas`")
    
@dp.message(StepsForm.SETTINGS, F.text == "Timezone")
async def customize_timezone(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    
    await state.set_state(StepsForm.SETTINGS_EDIT_TIMEZONE)
    
    text = make_header("TIMEZONE") + f"""
*Current:*
`{routine.timezone}`

{SEPARATOR_LIGHT}

*Common timezones:*
`Europe/Helsinki`
`Europe/Stockholm`
`America/New_York`
`Asia/Tokyo`

*Change timezone:*
`timezone Europe/London`

[Full list](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
"""
    
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="timezone Europe/Helsinki")],
            [KeyboardButton(text="Back")]
        ]
    )
    
    await bot.send_message(chat_id, text, reply_markup=markup)


@dp.message(StepsForm.SETTINGS_EDIT_TIMEZONE)
async def handle_timezone_change(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    text = message.text.strip()
    
    if text.lower() == "back":
        await show_settings(message, state)
        return
    
    parts = text.split(maxsplit=1)
    if len(parts) == 2 and parts[0].lower() == "timezone":
        tz_name = parts[1]
        try:
            # Validate timezone
            pytz.timezone(tz_name)
            routine.timezone = tz_name
            save_routines()
            await bot.send_message(chat_id, f"`Timezone set to {tz_name}`")
            await show_settings(message, state)
        except pytz.exceptions.UnknownTimeZoneError:
            await bot.send_message(chat_id, "`Invalid timezone\\. Check spelling\\.`")
    else:
        await bot.send_message(chat_id, "`Format: timezone Europe/Helsinki`")

@dp.message(StepsForm.SETTINGS_EDIT_ROUTINE)
async def handle_edit_routine(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    text = message.text.strip()
    
    if text == "Back":
        await show_settings(message, state)
        return
    
    # Remove task
    if text.isdigit():
        task_num = int(text) - 1
        if routine.remove_task(task_num):
            save_routines()
            await bot.send_message(chat_id, "`Removed`")
            await edit_routine(message, state)
        else:
            await bot.send_message(chat_id, "`Invalid number`")
    
    # Add task
    elif text.lower().startswith("add "):
        try:
            parts = text[4:].strip().split()
            optional = parts[-1].lower() == "optional"
            if optional:
                parts = parts[:-1]
            
            duration = int(parts[-1])
            task_name = " ".join(parts[:-1])
            
            if routine.add_task(task_name, duration, optional):
                save_routines()
                await bot.send_message(chat_id, f"`Added: {task_name}`")
                await edit_routine(message, state)
            else:
                await bot.send_message(chat_id, "`Max 15 tasks`")
        except (ValueError, IndexError):
            await bot.send_message(chat_id, "`Invalid format`")
    else:
        await bot.send_message(chat_id, "`Invalid command`")

@dp.message(StepsForm.SETTINGS, F.text == "Reset")
async def reset_routine_confirm(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Confirm Reset")],
            [KeyboardButton(text="Cancel")]
        ]
    )
    
    await bot.send_message(
        message.from_user.id,
        "*Reset routine?*\n\nClears tasks, keeps statistics",
        reply_markup=markup
    )


@dp.message(StepsForm.SETTINGS, F.text == "Confirm Reset")
async def reset_routine_confirmed(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    routine.tasks = []
    routine.is_setup_complete = False
    save_routines()
    
    await bot.send_message(chat_id, "`Routine reset`")
    await state.set_state(StepsForm.SETUP_ADD_TASK)
    await setup_start(message, state)


@dp.message(StepsForm.SETTINGS, F.text == "Delete All")
async def delete_data_confirm(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Confirm Delete")],
            [KeyboardButton(text="Cancel")]
        ]
    )
    
    await bot.send_message(
        message.from_user.id,
        "*Delete all data?*\n\n`Cannot be undone`",
        reply_markup=markup
    )


@dp.message(StepsForm.SETTINGS, F.text == "Confirm Delete")
async def delete_data_confirmed(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    if chat_id in routines_dict:
        del routines_dict[chat_id]
        if chat_id in user_replies:
            del user_replies[chat_id]
        save_routines()
    
    await bot.send_message(chat_id, "`All data deleted`\nUse /start to begin")
    await state.clear()


@dp.message(StepsForm.SETTINGS, F.text == "Cancel")
async def cancel_action(message: types.Message, state: FSMContext):
    await show_settings(message, state)


@dp.message(StepsForm.SETTINGS, F.text == "Menu")
async def settings_to_menu(message: types.Message, state: FSMContext):
    await show_main_menu(message.from_user.id, state)

async def on_startup(chat_id:int, task_dictionary:dict) -> None:   
    await bot.send_message(chat_id, "Bot has been started!", disable_notification=True)

    # Schedule the message to be sent daily at 12:00
    asyncio.create_task(scheduled_messages(task_dictionary))

@dp.message(StepsForm.MENU)
async def handle_menu_fallback(message: types.Message, state: FSMContext):
    """Catch-all for menu - handles watch quick replies"""
    chat_id = message.from_user.id
    routine = routines_dict[chat_id]
    text = message.text.strip()
    
    # List of known button commands that should be ignored here
    known_commands = ["Start Routine", "Continue", "Stats", "Settings"]
    
    # If it's a known command, ignore it (other handlers will catch it)
    if text in known_commands:
        return
    
    # Check if text is "Skip" - never start routine with this
    if text == "Skip":
        await bot.send_message(chat_id, "`Cannot start with Skip`")
        return
    
    # Check if we're in the time window
    user_tz = pytz.timezone(routine.timezone)
    now = datetime.datetime.now(user_tz)
    current_minutes = now.hour * 60 + now.minute
    start_minutes = routine.window_start * 60 + routine.window_start_minute
    end_minutes = routine.window_end * 60 + routine.window_end_minute
    
    # If outside window, show menu
    if current_minutes < start_minutes or current_minutes >= end_minutes:
        await bot.send_message(
            chat_id,
            f"`Window: {routine.window_start:02d}:{routine.window_start_minute:02d} - {routine.window_end:02d}:{routine.window_end_minute:02d}`\n`Now: {now.strftime('%H:%M')}`"
        )
        await show_main_menu(chat_id, state)
        return
    
    # ANY other text should start the routine if conditions are met
    if routine.can_start_routine() and not routine.routine_started:
        if routine.start_routine():
            print(f"[WATCH START] Starting routine from watch input: '{text}'")
            await state.set_state(StepsForm.ROUTINE_ACTIVE)
            save_routines()
            await send_next_task(chat_id, state)
        else:
            await bot.send_message(
                chat_id,
                f"`Window: {routine.window_start:02d}:{routine.window_start_minute:02d} - {routine.window_end:02d}:{routine.window_end_minute:02d}`\n`Now: {now.strftime('%H:%M')}`"
            )
    elif routine.routine_started:
        # If routine already started, go to continue
        print(f"[WATCH CONTINUE] Continuing from watch input: '{text}'")
        await state.set_state(StepsForm.ROUTINE_ACTIVE)
        await send_next_task(chat_id, state)
    else:
        # Unknown situation, show menu
        await show_main_menu(chat_id, state)

async def action_over_time(current_time, last_sent=None) -> None:
    """Scheduled tasks that run at specific times"""
    global routines_dict
    
    if last_sent is None:
        last_sent = {}
    
    # Check notifications for each user in their timezone
    for chat_id, routine in list(routines_dict.items()):
        if not routine.is_setup_complete:
            continue
        
        try:
            # Initialize tracking for this user
            if chat_id not in last_sent:
                last_sent[chat_id] = {}
            
            # Get current time in user's timezone
            user_tz = pytz.timezone(routine.timezone)
            user_time = datetime.datetime.now(user_tz)
            today = user_time.date().isoformat()
            current_time_str = user_time.strftime('%Y-%m-%d %H:%M')
            
            current_minutes = user_time.hour * 60 + user_time.minute
            start_minutes = routine.window_start * 60 + routine.window_start_minute
            end_minutes = routine.window_end * 60 + routine.window_end_minute
            
            print(f"[DEBUG {chat_id}] Current: {user_time.strftime('%H:%M')}, Window: {routine.window_start:02d}:{routine.window_start_minute:02d} - {routine.window_end:02d}:{routine.window_end_minute:02d}")
            
            # AUTO-CLEANUP: Force finish any ongoing routine after window closes
            if current_minutes >= end_minutes and routine.routine_started:
                finish_key = f'finish_{today}'
                if last_sent[chat_id].get(finish_key) != current_time_str:
                    print(f"[DEBUG {chat_id}] Auto-finishing routine")
                    routine.finish_routine()
                    save_routines()
                    
                    completion = routine.get_completion_percentage()
                    if completion < 100:
                        await bot.send_message(
                            chat_id,
                            f"*Routine auto-finished*\n\n`{completion:.0f}% complete`\nStreak reset\\.",
                            disable_notification=True
                        )
                    last_sent[chat_id][finish_key] = current_time_str
            
            # Morning reminder - at window start (SILENT)
            if current_minutes == start_minutes:
                start_key = f'start_{today}'
                if today not in routine.history and last_sent[chat_id].get(start_key) != current_time_str:
                    print(f"[DEBUG {chat_id}] Sending morning reminder")
                    await bot.send_message(
                        chat_id,
                        make_header("Good morning") + "Ready to start?",
                        disable_notification=True
                    )
                    last_sent[chat_id][start_key] = current_time_str
            
            # Warning - 1 hour before window ends (SILENT)
            warning_minutes = end_minutes - 60
            if warning_minutes > 0 and current_minutes == warning_minutes:
                warning_key = f'warning_{today}'
                if today not in routine.history and last_sent[chat_id].get(warning_key) != current_time_str:
                    minutes_left = end_minutes - current_minutes
                    hours_left = minutes_left // 60
                    if hours_left > 0:
                        print(f"[DEBUG {chat_id}] Sending warning")
                        await bot.send_message(
                            chat_id,
                            f"*⏰ ~{hours_left} hour{'s' if hours_left != 1 else ''} left*\n\n`{routine.current_streak}d` {ICON_STREAK}",
                            disable_notification=True
                        )
                        last_sent[chat_id][warning_key] = current_time_str
            
            # Check for missed routines - 30 minutes after window ends
            missed_check_minutes = end_minutes + 30
            if current_minutes == missed_check_minutes:
                missed_key = f'missed_{today}'
                if last_sent[chat_id].get(missed_key) != current_time_str:
                    routine.check_missed_routine()
                    
                    if routine.history.get(today, {}).get('missed', False):
                        print(f"[DEBUG {chat_id}] Sending missed notification")
                        await bot.send_message(
                            chat_id,
                            "*Window closed*\n\nStreak reset\\. Tomorrow is fresh\\.",
                            disable_notification=True
                        )
                    save_routines()
                    last_sent[chat_id][missed_key] = current_time_str
            
            # Evening success message - 9:00 PM (SILENT)
            elif user_time.hour == 21 and user_time.minute == 0:
                evening_key = f'evening_{today}'
                if last_sent[chat_id].get(evening_key) != current_time_str:
                    day_data = routine.history.get(today, {})
                    
                    if day_data.get('completion', 0) >= 100:
                        streak_bar = make_streak_bar(routine.current_streak, 10)
                        await bot.send_message(
                            chat_id,
                            make_header("Great day!") + f"\n{streak_bar}\n`{routine.current_streak}d`",
                            disable_notification=True
                        )
                        last_sent[chat_id][evening_key] = current_time_str
            
            # Weekly report - Sunday 8:00 PM (SILENT)
            elif user_time.weekday() == 6 and user_time.hour == 20 and user_time.minute == 0:
                weekly_key = f'weekly_{today}'
                if last_sent[chat_id].get(weekly_key) != current_time_str:
                    stats = routine.get_weekly_stats()
                    visual = create_week_visual(routine)
                    
                    report = f"""*WEEK COMPLETE*

{visual}

`{stats['completed_days']}/7` days
`{stats['avg_completion']:.0f}%` average
`{stats['current_streak']}d` current streak
`{stats['best_streak']}d` best

{get_weekly_insights(stats)}"""
                    
                    await bot.send_message(chat_id, report, disable_notification=True)
                    last_sent[chat_id][weekly_key] = current_time_str
        
        except Exception as e:
            print(f"[ERROR] {chat_id}: {e}")
            if 'blocked' in str(e).lower():
                del routines_dict[chat_id]
                print(f"Removed blocked user: {chat_id}")

async def scheduled_messages(task_dictionary=None):
    """Background task for scheduled notifications"""
    print("\n SCHEDULED MESSAGES TASK IS RUNNING \n")
    
    loop_count = 0
    last_notified = {}
    
    while True:
        try:
            loop_count += 1
            now = datetime.datetime.now()
            
            print(f"\n[LOOP {loop_count}] Checking at {now.strftime('%H:%M:%S')}")
            
            for chat_id, routine in list(routines_dict.items()):
                if not routine.is_setup_complete:
                    continue
                
                try:
                    user_tz = pytz.timezone(routine.timezone)
                    user_time = datetime.datetime.now(user_tz)
                    today = user_time.date().isoformat()
                    
                    current_minutes = user_time.hour * 60 + user_time.minute
                    start_minutes = routine.window_start * 60 + routine.window_start_minute
                    end_minutes = routine.window_end * 60 + routine.window_end_minute
                    
                    print(f"  - Chat {chat_id}: {user_time.strftime('%H:%M')} | Window: {routine.window_start:02d}:{routine.window_start_minute:02d}-{routine.window_end:02d}:{routine.window_end_minute:02d} | Started: {routine.routine_started}")
                    
                    if chat_id not in last_notified:
                        last_notified[chat_id] = {}
                    
                    # START NOTIFICATION
                    if (start_minutes <= current_minutes < end_minutes and 
                        not routine.routine_started and 
                        today not in routine.history and
                        last_notified[chat_id].get('start') != today):
                        
                        print(f"    → Sending start notification")
                        await bot.send_message(
                            chat_id,
                            make_header("Good morning") + "Ready to start?",
                            disable_notification=True
                        )
                        last_notified[chat_id]['start'] = today
                    
                    # END NOTIFICATION
                    if current_minutes >= end_minutes and routine.routine_started:
                        print(f"    → Window closed, finishing routine")
                        routine.finish_routine()
                        save_routines()
                        
                        completion = routine.get_completion_percentage()
                        await bot.send_message(
                            chat_id,
                            f"*Window closed*\n\n`{completion:.0f}% complete`\n{'Streak maintained' if completion >= 100 else 'Streak reset'}",
                            disable_notification=True
                        )
                        last_notified[chat_id]['end'] = today
                    
                except Exception as e:
                    print(f"    ✗ ERROR: {e}")
                    import traceback
                    traceback.print_exc()
            
            print(f"[LOOP {loop_count}] Sleeping 60s\n")
            
        except Exception as e:
            print(f"\n!!! LOOP ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        await asyncio.sleep(60)

def save_routines() -> None:
    """Save all routines to JSON"""
    data = {
        'routines': {
            str(chat_id): routine.to_dict() 
            for chat_id, routine in routines_dict.items()
        },
        'user_replies': {
            str(chat_id): replies
            for chat_id, replies in user_replies.items()
        }
    }
    with open(FILE_NAME, 'w') as f:
        json.dump(data, f, indent=2)


def load_routines() -> dict:
    """Load routines from JSON"""
    try:
        with open(FILE_NAME, 'r') as f:
            data = json.load(f)
        
        # Load routines
        routines = {}
        routine_data = data.get('routines', data) if isinstance(data.get('routines'), dict) else data
        for chat_id, routine_info in routine_data.items():
            routines[int(chat_id)] = MorningRoutine.from_dict(routine_info)
        
        # Load custom replies
        global user_replies
        if 'user_replies' in data:
            user_replies = {int(k): v for k, v in data['user_replies'].items()}
        else:
            user_replies = {}
        
        print(f"Loaded {len(routines)} routines from file")
        return routines
    
    except FileNotFoundError:
        print("No existing routines file found")
        return {}
    except json.JSONDecodeError:
        print("ERROR: Invalid JSON in routines file")
        return {}
    except Exception as e:
        print(f"ERROR loading routines: {e}")
        return {}

async def main() -> None:
    global FILE_NAME, routines_dict
    
    FILE_NAME = './routines_data.json'
    routines_dict = load_routines()
    
    print(f"\n{'='*50}")
    print(f"BOT STARTING")
    print(f"Loaded {len(routines_dict)} users")
    print(f"{'='*50}\n")
    
    # Create the scheduled task
    scheduled_task = asyncio.create_task(scheduled_messages())
    print("✓ Scheduled notifications task created")
    
    try:
        # Start polling
        print("✓ Starting bot polling...")
        await dp.start_polling(bot)
    finally:
        scheduled_task.cancel()
        save_routines()
        await bot.session.close()
if __name__ == "__main__":
    asyncio.run(main())
