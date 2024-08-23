# Discord Leveling and Trading Bot

## Overview

This Discord bot allows users to level up, gain items, trade items with other users, and interact with various commands to manage their virtual inventory and experience points.

## Features

- **Leveling System**: Users can earn experience points and level up.
- **Item Management**: Users can add, list, and remove items from their inventory.
- **Trading**: Users can trade items with other users.
- **Daily Rewards**: Users can claim daily rewards.
- **Command Cooldowns**: Prevents command spamming with cooldowns.
- **Leaderboard**: Displays a leaderboard based on experience points.
- **Persistent Data**: User data is backed up and can be restored.
- **Item Value System**: Displays and sets values for items.

## Prerequisites

- Python 3.8+
- `discord.py` library
- SQLite3 database

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/discord-bot.git
    cd discord-bot
    ```

2. **Install dependencies:**
    ```sh
    pip install discord.py
    ```

3. **Create a `config.json` file:**
    ```json
    {
      "DISCORD_TOKEN": "YOUR_DISCORD_BOT_TOKEN"
    }
    ```

4. **Run the bot:**
    ```sh
    python bot.py
    ```

## Commands

- `!earn_experience <amount>`: Gain experience points.
- `!add_item <item>`: Add an item to your inventory.
- `!list_items`: List all items in your inventory.
- `!trade_item <@user> <item>`: Trade an item with another user.
- `!remove_item <item>`: Remove an item from your inventory.
- `!claim_daily`: Claim your daily reward.
- `!user_info`: View your user info.
- `!item_value <item>`: Show the value of an item.
- `!add_item_value <item> <value>`: Set the value of an item.
- `!leaderboard`: Show the leaderboard based on experience.
- `!backup`: Create a backup of the database.
- `!restore`: Restore the database from the backup.
- `!item_info <item>`: Show which users own a specific item.
- `!clear_inventory`: Clear your inventory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes or feature requests, please open an issue to discuss.

## Contact



