import os
import discord

#Set all intents to true, I think
intents = discord.Intents.all()

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
    
    
class MyClient(discord.Client):
    # on_ready, or on launch
    async def on_ready(self):
        print('Logged on as', self.user)
        
    # When a member joins, duh
    async def on_member_join(self, member):
        print('on_member_join works')

        # DMs the member with a welcome message
        await member.send(
            f'Hi {member.name}, welcome to my Discord server!'
        )

    # Literally whenever a message shows up in the server
    async def on_message(self, message):
        print('pingpong works')

        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

client = MyClient(intents=intents)
client.run(TOKEN)