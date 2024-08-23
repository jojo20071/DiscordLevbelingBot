import discord
from discord.ext import commands
import sqlite3

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

conn = sqlite3.connect('game.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    level INTEGER DEFAULT 1,
    experience INTEGER DEFAULT 0,
    items TEXT DEFAULT ''
)
''')
conn.commit()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

bot.run('YOUR_BOT_TOKEN')