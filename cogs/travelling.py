import discord
from discord.ext import commands

class Travelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Reacting to a preset destination in the travel-destinations text channel will DM the reactor and invite
    # to whatever destination server they reacted to.
    # TODO: kick the user out of the original server after sending the invite
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id

        # compares the channel id of the message being reacted to, to every channel in that guild, making sure it only executes when
        # the name of the text channel is travel-destination
        if (payload.channel_id == discord.utils.get(self.bot.get_guild(payload.guild_id).channels, name='travel-destinations').id):
            msg = await self.bot.get_channel(payload.channel_id).fetch_message(message_id)
            if (msg.content == 'Windvale'):
                # A link to the Windvale discord will be sent
                await payload.member.send('https://discord.gg/jJ3FetRgVu')
            if (msg.content == 'HQ'):
                # A link to the HQ discord will be sent
                await payload.member.send('https://discord.gg/MVGm6gFS42')

            await msg.remove_reaction(payload.emoji, payload.member)

def setup(bot):
    bot.add_cog(Travelling(bot))