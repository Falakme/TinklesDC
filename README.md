# Discord Bot with Modular Slash Command System

This project is a Discord bot built in Python using a modular command system. It leverages Discord's slash (/) command system for modern, user-friendly interactions. Each command is organized as a separate module for easy extension and maintenance.

## Features
- Modular command structure: Add or remove commands easily by editing the `commands/` folder.
- Uses Discord's slash command system for all interactions.
- Easy to extend and maintain.

## Getting Started

### Prerequisites
- Python 3.8+
- A Discord bot token ([create one here](https://discord.com/developers/applications))

### Installation
1. Clone this repository or copy the files to your project directory.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your bot token:
   ```env
   DISCORD_TOKEN=your-bot-token-here
   ```
4. Run the bot:
   ```sh
   python bot.py
   ```

## Project Structure
- `bot.py` - Main entry point for the bot.
- `commands/` - Folder containing all modular command files.
- `.env` - Environment file for secrets (not included in repo).
- `requirements.txt` - Python dependencies.

## Adding Commands
1. Create a new Python file in the `commands/` folder.
2. Define a function with the slash command logic.
3. Import and register the command in `bot.py`.

## License
MIT
