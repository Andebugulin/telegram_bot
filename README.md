---

# Telegram Bot [@Planirium](https://web.telegram.org/k/#@PlanyDbot)

\|   To streamline daily planning effortlessly   \| </br>
\|   Make people feel better in general   \| </br></br> 
\~   Ensures users efficiently organize their schedules    \~
#### \*hassle-free\*


# Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Support](#support)
- [License](#license)


## Features

- **Efficient Daily Planning**: Automate daily tasks effortlessly.
  
- **User-Friendly Interface**: Intuitive design for easy navigation.

- **Daily Template Setup**: Personalized templates for daily activities.

- **Real-Time Silent Notifications**: Visual notifications for updates without sound interruptions.

- **Modern, Minimalist Design**: Distraction-free interface for enhanced usability.

- **Free to Use**: No hidden charges, access all features without cost.

- **Deactivation and Deletion**: Control to delete or deactivate the bot anytime.


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
      pip install aiogram==3.1.1 python-dotenv==1.0.0
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
    - Start the bot using the appropriate command for your bot's programming language:
      - For Python:
        ```
        python function_dir/main.py  
        ```

## Usage

#### Interface Overview:
- **Simple Interface**: The bot provides a straightforward interface with two main buttons:
  - **"Working" Button**: Accesses tasks scheduled for the day.
  - **"Template" Button**: Manages and modifies template tasks.

#### Working with "Working" Button:
- **View Tasks for Today**: Clicking the "Working" button displays tasks scheduled for the day.
- **Add and Delete Tasks**:
  - **Add Tasks**: Users can add tasks and specify the task's name and duration in minutes.
  - **Delete Tasks**: Delete tasks individually to manage the task list.

- **Start or Stop Tasks**:
  - Users can start or stop tasks that are in progress, enabling better task management.

#### Working with "Template" Button:
- **Manage Template Tasks**: Accesses a separate set of tasks for templates.
- **Add and Delete Template Tasks**:
  - **Add Template Tasks**: Specify task name and duration for future scheduling.
  - **Delete Template Tasks**: Remove template tasks through button commands.

- **Replace Current Tasks with Template**:
  - Option to replace the tasks scheduled for today with tasks from the template.
- **Replace Template with Current Tasks**:
  - Option to update the template tasks with the currently scheduled tasks.

#### Command Flow:
- **Navigation and Commands**: Users navigate using buttons, then interact through button-based commands for task management (add, delete, start, stop), template management, and task-template interchange.

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

Specify the license under which your Telegram bot is released.

This project is licensed under the [License Name] - see the [LICENSE.md](LICENSE.md) file for details.

---

Replace the placeholders (`your-telegram-bot`, `Feature 1`, `yourusername`, etc.) with your actual bot name, features, usernames, and relevant information.

Remember to include specific details that can guide users on how to install, use, and contribute to your Telegram bot effectively.
