# Morner

Telegram bot for morning routine tracking via smartwatch.

<p align="center">
  <img src="./PlaniriumBot.png" alt="Morner Bot" width="600"/>
</p>

## Idea

I believe mornings are more productive for our brain and mind. However, it is difficult to avoid distractions and not get pulled into the phone, hence comes the idea of this bot. You set up your morning routine once via phone, then every morning you interact with the bot via smartwatch using quick replies only, minimizing phone usage, keeping your head clear and not being too much noise is always good in my opinion.

## Try It

Bot is already running and hosted on Oracle Cloud: [@PlanyDbot](https://t.me/PlanyDbot)

Send `/start` to begin.

## Features

Watch-optimized interface with customizable quick replies. Task management with optional/required task types. Configurable time windows and timezone support. Streak tracking with daily/weekly/monthly statistics. Silent notifications at routine start, warnings before deadline, and completion summaries. Pause/resume functionality for interrupted routines.

## How It Works

Setup your routine once through phone. Each morning you receive a silent notification on your watch. Tap any quick reply to start the routine. Complete tasks by tapping any quick reply button. The bot advances automatically regardless of which quick reply you use, since everyone has different button configurations on their watches.

Special commands that require specific text: `Skip` (marks current task as skipped), `Menu` (returns to main menu).

Streaks require 100% completion of required tasks. Optional tasks don't affect your streak if skipped.

## Self-Hosting

If you prefer to run your own instance instead of using the hosted bot.

Requires Python 3.8+ and a Telegram bot token from [@BotFather](https://t.me/BotFather).

```bash
git clone https://github.com/Andebugulin/telegram_bot.git
cd telegram_bot
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create `.env` file with your bot token:

```
BOT_TOKEN=your_token_here
```

Run the bot:

```bash
python function_dir/main.py
```

Data persists to `routines_data.json` in the project directory.

## Task Setup

Send `/start` to begin setup. Add tasks using format: `task_name duration_minutes`. Optional tasks can be marked with `optional` flag. Maximum 15 tasks per routine.

Example task format:

```
Wake up 2
Exercise 15
Shower 10 optional
```

The bot operates within configured time windows (default 6-12 AM). Task status indicators: ✓ completed, ○ incomplete, `opt` for optional tasks. Statistics include 7-day and monthly calendar views, current/best streak tracking, and completion percentages.

## Configuration

Settings accessible through bot menu.

Task editing commands:

```
delete N          # remove task N
edit N            # modify task N
move N M          # reorder task N to position M
add name duration # add new task
```

Quick replies: Customize 3-5 button labels (format: `Done, Next, Great`)

Time window: Set routine hours (format: `window 6 12`)

Timezone: Configure local timezone (format: `timezone Europe/Helsinki`)

Data management: Reset clears tasks while preserving statistics. Delete All removes everything.

## Notifications

All notifications are silent. Schedule based on configured time window:

Window start: routine ready reminder
2 hours before end: time remaining warning
30 minutes after end: missed routine alert
21:00: completion summary (if finished)
Sunday 20:00: weekly statistics report

## Technical Details

Built with aiogram 3.x for async Telegram bot operations. Uses FSM (Finite State Machine) pattern for conversation flow management. Data persistence via JSON file. Timezone handling through pytz library.

State machine handles setup flow, menu navigation, active routine tracking, and settings modification. Automatic data saving after each state change.

## Contributing

Standard fork and pull request workflow. Create feature branches for changes.

## License

MIT License. See LICENSE.md for details.

## Contact

[GitHub Issues](https://github.com/Andebugulin/telegram_bot/issues)
