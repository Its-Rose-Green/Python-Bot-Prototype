import discord
from discord.ext import commands

class Tavern(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purchase")
    async def purchase(self, context, amount: int, item):
        if (context.channel.id != discord.utils.get(context.guild.channels, name='tavern').id):
            await context.send("The 'purchase' command can only be used in a Tavern")
            return False

        else:
            Economy = self.bot.get_cog('Economy')

            if Economy is not None: 
                users = await Economy.get_bank_data()
                pouchValue = await Economy.get_user_pouch_value(context.author)
                cost = amount*2
                if (str(context.author.id) not in users):
                    return False

                if (pouchValue < cost):
                    await context.send("You can't afford this.")

                if (pouchValue >= cost):
                    await context.send("You have purchased " + str(amount) + " " + item + ".")
                    await context.send("Spent " + str(cost) + " coins.")
                    await Economy.subtract_money(context.author, cost)

def setup(bot):
    bot.add_cog(Tavern(bot))