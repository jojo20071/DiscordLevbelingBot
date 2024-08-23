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

@bot.command()
async def earn_experience(ctx, amount: int):
    user_id = ctx.author.id
    c.execute('SELECT experience FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        new_exp = result[0] + amount
        level = new_exp // 1000 + 1
        c.execute('UPDATE users SET experience = ?, level = ? WHERE user_id = ?', (new_exp, level, user_id))
        conn.commit()
        await ctx.send(f'{ctx.author.name} earned {amount} experience and is now level {level}.')
    else:
        c.execute('INSERT INTO users (user_id, experience, level) VALUES (?, ?, ?)', (user_id, amount, amount // 1000 + 1))
        conn.commit()
        await ctx.send(f'{ctx.author.name} has been added to the system with {amount} experience and level 1.')

@bot.command()
async def add_item(ctx, item: str):
    user_id = ctx.author.id
    c.execute('SELECT items FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        items = result[0]
        if items:
            items = items.split(',')
        else:
            items = []
        items.append(item)
        items_str = ','.join(items)
        c.execute('UPDATE users SET items = ? WHERE user_id = ?', (items_str, user_id))
        conn.commit()
        await ctx.send(f'{ctx.author.name} added {item} to their inventory.')
    else:
        c.execute('INSERT INTO users (user_id, items) VALUES (?, ?)', (user_id, item))
        conn.commit()
        await ctx.send(f'{ctx.author.name} has been added to the system with {item} in their inventory.')

bot.run('YOUR_BOT_TOKEN')