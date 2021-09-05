import discord
from discord.ext import commands

class Encounters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # make new channel
    # TO DO: A command to let user escape with an automatic loss or something similar
    # TO DO: Look into threads maybe
    # TO DO: Something to track if the user stops replying in the encounter for however long the channel will close and auto loss or similar
    @commands.command(name="make_channel")
    async def make_channel(self, context):
        guild = context.guild
        member = context.author
        admin_role = discord.utils.get(guild.roles, name="Creator")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel('your-encounter', overwrites=overwrites)

    # Surrendering/Escape out of encounter
    # TO DO: Surrendering will detract fame from the user
    # TO DO: Timing out will detract HP from the user, possibly KO-ing them
    # Possibly could use channel.history to get the last message then compare that timestamp with current
    @commands.command(name="surrender")
    async def surrender(self, context):
        channelID = context.message.channel
        if (channelID.name == 'your-encounter'):
            await channelID.delete()
        else:
            return

    # Turn-taking prototype - fix it up later for our purposes
    @commands.command(name="turn_test")
    async def test(self, context, user: discord.Member):
        turn = 0
        aut = 5
        ops = 5
        userM = user.mention
        cmam = context.message.author.mention
        if user == cmam:
            await context.send(f"You can't fight yourself {cmam}")
        else:
            await context.send(f"{cmam} vs {userM}, who will win?")
            while aut > 0 and ops > 0:
                # Turn 1
                if turn == 0:
                    await context.send(f"{cmam}: `test`")
                    def check(m):
                        return m.content == "test" and m.author == context.message.author
                    response = await self.bot.wait_for('message', check = check)
                    if "test" in response.content.lower() and turn == 0:
                        await context.send("a nice test")
                        turn = turn + 1
                # Turn 2
                elif turn == 1:
                    await context.send(f"{userM}: `test`")
                    def check(o):
                        return o.content == "test" and o.author == user
                    response = await self.bot.wait_for('message', check = check)
                    if "test" in response.content.lower() and turn == 1:
                        await context.send("the test is strong with this one")
                        turn = turn - 1

def setup(bot):
    bot.add_cog(Encounters(bot))