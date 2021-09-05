import discord
from discord.ext import commands

class Tavern(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purchase")
    async def purchase(self, context, quantity: int, item):
        """ Allows the user to purchase an quantity of items. The cost right now is set at 2*quantity and the user can purchase anything.
        The item they purchase currently goes nowhere.

        Input:  commands.Context, quantity(Int), item(Str)
        Output: (Bool) True if successfully purchased, False otherwise
        """

        if (context.channel.id != discord.utils.get(context.guild.channels, name='tavern').id):
            await context.send("The 'purchase' command can only be used in a Tavern")
            return False

        else:
            Economy = self.bot.get_cog('Economy')

            if Economy is not None: 
                users = await Economy.get_bank_data()
                pouch_value = await Economy.get_user_pouch_value(context.author)
                cost = quantity*2
                if (str(context.author.id) not in users):
                    return False

                if (pouch_value < cost):
                    await context.send("You can't afford this.")
                    return False

                if (pouch_value >= cost):
                    await context.send("You have purchased " + str(quantity) + " " + item + ".")
                    await context.send("Spent " + str(cost) + " coins.")
                    await Economy.subtract_money(context.author, cost)
                    return True

def setup(bot):
    bot.add_cog(Tavern(bot))