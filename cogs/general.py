#!/usr/bin/python3

from discord.ext import commands

#--------------------------- 
# General purpose functions
#---------------------------
class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ping")
    async def ping(self, context):
        """ 
        Check if the bot is alive
        """

        await context.send("pong")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        When a member joins, duh
        """
        await member.send(f'Hi {member.name}, welcome to my Discord server!')


def setup(bot):
    bot.add_cog(General(bot))