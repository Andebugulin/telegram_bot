---

# Telegram Bot Morner

\| To build consistent morning habits effortlessly \| </br>
\| Make people feel better in general \| </br></br>
\~ Ensures users efficiently complete their morning routines \~

<p align="center">
  <img src="./PlaniriumBot.png" alt="Wizard" width="600"/>
</p>

# Main Idea

If you would like to have a morning routine, but often find yourself skipping it due to lack of motivation or forgetfulness, or you start to doomscroll on your phone
and end up wasting your morning, this bot tries to help you.
Many of us now have smartwatches and they are usually not as distracting as phones, the idea is to not use your phone, but rather rely on your watch to complete your morning routine.

At first you setup morning routine with tasks, and I mean yes, this is easier on the phone, after that
each morning you get silent notification on your watch, like "Ready to start?" in the watch you can choose any message from your quick replies, like "yes" or any ather one you want. Just send it, then the bot will understand that you have woken up and it will start guiding you through your routine, sending you each task one by one.
After receiving another notification from the bot with the task, you can again use quick replies to respond with "Done", "Next", "Great" or any other message you set up.
To make the task complete, just send almost any quick reply message, or press it on the phone.
If you send "Skip" button, the bot will mark current task as failed and go to the next one.

Be aware of your mornings and good luck :)

#### \*hassle-free\*

# Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)

## Installation

To get started with the bot, it's recommended to set up a virtual environment to manage dependencies. Here's a step-by-step guide:

1. **Create a Virtual Environment (Optional but Recommended)**

   - For Python users:
     ```
     python -m venv venv_name
     ```

2. **Activate the Virtual Environment**

   - For Windows:
     ```
     venv_name\Scripts\activate
     ```
   - For macOS and Linux:
     ```
     source venv_name/bin/activate
     ```

3. **Clone the Repository**

   ```
   git clone https://github.com/Andebugulin/telegram_bot.git
   cd telegram_bot
   ```

4. **Install Dependencies**

   - For Python:
     ```
     pip install -r requirements.txt
     ```

5. **Set Up Bot Token**

   - Obtain your bot token from [@BotFather](https://web.telegram.org/k/#@BotFather) on Telegram.
   - Set the token in the configuration file or as an environment variable.

     #

     Here's an example of what your `.env` file might contain:

     ```
     BOT_TOKEN=YOUR_BOT_TOKEN_HERE
     ```

     #

6. **Run the Bot**
   - Start the bot using the appropriate command:
     - For Python:
       ```
       python function_dir/main.py
       ```

## Usage

#### Routine Setup:

- **Initial Setup**: Add tasks with name, duration in minutes, and optional flag.
  - Example: `Wake up 2`, `Exercise 15`, `Shower 10 optional`
- **Task Management**: Up to 15 tasks per routine.

#### Running Your Routine:

- **Start Routine**: Available during your configured time window (default 05:00-11:00).
- **Task Flow**: Complete tasks one by one using quick reply buttons or "Skip" for tasks you can't complete, use your watch to respond easily.
- **Watch Commands**: Use customizable quick replies ("Done", "Next", "Great") from your smartwatch.
- **Progress Tracking**: Real-time progress bar shows completion percentage.

#### Task Status Indicators:

- ✓ **Completed**: Task finished successfully.
- ○ **Incomplete**: Task not yet started or skipped.
- **Optional tasks** are marked with `opt` label.

#### Statistics View:

- **Weekly View**: 7-day calendar with completion status:

  - ● Done
  - ◐ Partial completion
  - ○ Missed
  - × Failed (outside time window)

- **Monthly Calendar**: Full month view with daily completion tracking.

- **Streak Tracking**:
  - Current streak
  - Best streak record
  - Total completions

#### Settings:

- **Edit Routine**: Add, delete, move, or edit tasks.

  - Commands: `delete N`, `edit N`, `move N M`, `add name duration [optional]`

- **Quick Replies**: Customize watch response buttons (3-5 words).

  - Format: `Done, Next, Great`

- **Time Window**: Set custom routine hours.

  - Format: `window 6 12` (6 AM to 12 PM)

- **Reset**: Clear tasks while keeping statistics.

- **Delete All**: Remove all data and start fresh.

#### Smart Notifications:

- **06:00**: Morning reminder (silent) - "Ready to start?"
- **10:00**: One-hour warning (silent)
- **11:30**: Missed routine notification
- **21:00**: Evening success message (if completed)
- **Sunday 20:00**: Weekly report with statistics

#### Command Flow:

- **Navigation**: Use buttons to navigate between Menu, Stats, and Settings.
- **Task Completion**: Respond with any quick reply or press "Done" to complete tasks.
- **Skip Tasks**: Skip button marks optional tasks complete, leaves required tasks incomplete.
- **Pause/Resume**: Pause routine anytime and resume later (pause time excluded from duration).

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`
3. Make changes and commit: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request.

## Support

- Email: gulin.andrey2005@gmail.com
- Issue Tracker: [@Issues](https://github.com/Andebugulin/telegram_bot/issues)

## License

This project is licensed under the [MIT License] - see the [LICENSE.md](LICENSE) file for details.
