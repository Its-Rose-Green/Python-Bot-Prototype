#!/usr/bin/python3
import os
import sys
import discord
import classyjson as cj

from util.setup import getCogs, getConfig


from discord.ext import commands, tasks
from discord.ext.commands import Bot

# Get Config
try:
    config = getConfig()
except FileNotFoundError as error:
    sys.exit(error)



intents = discord.Intents.all()
bot = Bot(command_prefix=config.command_prefix, intents=intents)

# Load Extensions
extensions = getCogs()
for item in extensions:
    try:
        bot.load_extension(item)
        print(f"Loaded extension '{item}'")
    except Exception as error:
        error_str = f"{type(error).__name__}: {error}"
        print(f"Falied to load extension {item}\n{error_str}")



# The code in this event is executed when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print("-------------------")
    


bot.run(config["discord_token"])