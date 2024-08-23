import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta
from discord.ext import tasks

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

cooldown_seconds = 60

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
c.execute('''
CREATE TABLE IF NOT EXISTS rewards (
    user_id INTEGER PRIMARY KEY,
    last_claimed TEXT
)
''')
conn.commit()

@bot.command()
@commands.cooldown(1, cooldown_seconds, commands.BucketType.user)
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
@commands.cooldown(1, cooldown_seconds, commands.BucketType.user)
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

@bot.command()
async def list_items(ctx):
    user_id = ctx.author.id
    c.execute('SELECT items FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        items = result[0]
        if items:
            await ctx.send(f'{ctx.author.name} has the following items: {items}')
        else:
            await ctx.send(f'{ctx.author.name} has no items.')
    else:
        await ctx.send(f'{ctx.author.name} is not registered in the system.')

@bot.command()
async def trade_item(ctx, member: discord.Member, item: str):
    sender_id = ctx.author.id
    receiver_id = member.id
    c.execute('SELECT items FROM users WHERE user_id = ?', (sender_id,))
    sender_items = c.fetchone()[0]
    if item in sender_items.split(','):
        new_sender_items = ','.join([i for i in sender_items.split(',') if i != item])
        c.execute('UPDATE users SET items = ? WHERE user_id = ?', (new_sender_items, sender_id))
        c.execute('SELECT items FROM users WHERE user_id = ?', (receiver_id,))
        receiver_items = c.fetchone()[0]
        if receiver_items:
            receiver_items = receiver_items.split(',')
        else:
            receiver_items = []
        receiver_items.append(item)
        c.execute('UPDATE users SET items = ? WHERE user_id = ?', (','.join(receiver_items), receiver_id))
        conn.commit()
        await ctx.send(f'{ctx.author.name} traded {item} to {member.name}.')
    else:
        await ctx.send(f'{ctx.author.name} does not have {item}.')

@bot.command()
async def user_info(ctx):
    user_id = ctx.author.id
    c.execute('SELECT level, experience, items FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        level, experience, items = result
        items_list = items.split(',') if items else 'No items'
        await ctx.send(f'Level: {level}\nExperience: {experience}\nItems: {", ".join(items_list)}')
    else:
        await ctx.send(f'{ctx.author.name} is not registered in the system.')

@bot.command()
async def claim_daily(ctx):
    user_id = ctx.author.id
    now = datetime.utcnow()
    c.execute('SELECT last_claimed FROM rewards WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        last_claimed = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S') if result[0] else None
        if last_claimed and now - last_claimed < timedelta(days=1):
            await ctx.send('You have already claimed your daily reward.')
            return
    c.execute('INSERT OR REPLACE INTO rewards (user_id, last_claimed) VALUES (?, ?)', (user_id, now.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    reward_item = 'Mystery Box'
    c.execute('SELECT items FROM users WHERE user_id = ?', (user_id,))
    current_items = c.fetchone()[0]
    if current_items:
        new_items = current_items + ',' + reward_item
    else:
        new_items = reward_item
    c.execute('UPDATE users SET items = ? WHERE user_id = ?', (new_items, user_id))
    conn.commit()
    await ctx.send(f'You have claimed your daily reward: {reward_item}.')


@bot.command()
async def remove_item(ctx, item: str):
    user_id = ctx.author.id
    c.execute('SELECT items FROM users WHERE user_id = ?', (user_id,))
    items = c.fetchone()[0]
    if items and item in items.split(','):
        new_items = ','.join([i for i in items.split(',') if i != item])
        c.execute('UPDATE users SET items = ? WHERE user_id = ?', (new_items, user_id))
        conn.commit()
        await ctx.send(f'{ctx.author.name} removed {item} from their inventory.')
    else:
        await ctx.send(f'{ctx.author.name} does not have {item}.')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    else:
        await ctx.send("An error occurred. Please try again.")

@bot.event
async def on_member_remove(member):
    c.execute('DELETE FROM users WHERE user_id = ?', (member.id,))
    conn.commit()

@bot.event
async def on_member_join(member):
    c.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (member.id,))
    conn.commit()

@bot.command(aliases=['info'])
async def user_info(ctx):
    user_id = ctx.author.id
    c.execute('SELECT level, experience, items FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        level, experience, items = result
        items_list = items.split(',') if items else 'No items'
        await ctx.send(f'Level: {level}\nExperience: {experience}\nItems: {", ".join(items_list)}')
    else:
        await ctx.send(f'{ctx.author.name} is not registered in the system.')

@bot.command(aliases=['i'])
async def list_items(ctx):
    user_id = ctx.author.id
    c.execute('SELECT items FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    if result:
        items = result[0]
        if items:
            await ctx.send(f'{ctx.author.name} has the following items: {items}')
        else:
            await ctx.send(f'{ctx.author.name} has no items.')
    else:
        await ctx.send(f'{ctx.author.name} is not registered in the system.')

@bot.command()
async def help(ctx):
    help_text = (
        "!earn_experience <amount> - Gain experience points.\n"
        "!add_item <item> - Add an item to your inventory.\n"
        "!list_items - List all items in your inventory.\n"
        "!trade_item <@user> <item> - Trade an item with another user.\n"
        "!remove_item <item> - Remove an item from your inventory.\n"
        "!claim_daily - Claim your daily reward.\n"
        "!user_info - View your user info.\n"
        "!help - Show this help message."
    )
    await ctx.send(help_text)

item_values = {
    'Mystery Box': 100,
    'Rare Sword': 500,
    'Health Potion': 50
}

@bot.command()
async def item_value(ctx, item: str):
    value = item_values.get(item, 'Item not found or no value assigned.')
    await ctx.send(f'The value of {item} is {value}.') if isinstance(value, int) else await ctx.send(value)

@bot.command()
async def add_item_value(ctx, item: str, value: int):
    item_values[item] = value
    await ctx.send(f'Value of {item} set to {value}.')
bot.run('YOUR_BOT_TOKEN')