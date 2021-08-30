import os

import discord
from discord.ext import commands

# Set all intents to true, I think
intents_new = discord.Intents.all()

# Set prefix to call bot to >, as well as set intents to the intents from the thing before
bot = commands.Bot(command_prefix='>', intents=intents_new)

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# on_ready, or on launch
@bot.event
async def on_ready():
    print('Logged on as', bot.user)

# When a member joins, duh
@bot.event
async def on_member_join(member):
    # DMs the member that just joined
    await member.send(f'Hi {member.name}, welcome to my Discord server!')

# When they use command prefix with name, like >ping
@bot.command()
async def ping(ctx):
    await ctx.send('message')
    
bot.run(TOKEN)