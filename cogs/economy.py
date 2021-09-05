#!/usr/bin/python3
import discord
import json
from discord.ext import commands

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance")
    async def balance(self, context):
        """ Displays User's balance

        Input:  commands.Context
        Output: None
        """

        await self.open_account(context.author)

        users = await self.get_bank_data()

        pouch_amt = users[str(context.author.id)]["pouch"]
        bank_amt = users[str(context.author.id)]["bank"]

        em = discord.Embed(title = f"{context.author.name}'s balance")
        em.add_field(name = "Pouch Amount", value = pouch_amt)
        em.add_field(name = "Bank Balance", value = bank_amt)
        await context.send(embed = em)
    
    @commands.command(name="give_myself_money")
    @commands.has_role('Creator')
    async def give_myself_money(self, context, amount):
        """ Test command, gives the caller's money

        Input:  commands.Context, amount(Str)
        Output: None
        """

        await self.open_account(context.author)
        await context.send(f"Obtained {amount} coins")
        await self.add_money(context.author, amount)

    @commands.command(name="donate_to_thin_air")
    async def donate_to_thin_air(self, context, amount):
        """ Test command, subtracts the caller's money

        Input:  commands.Context, amount(Str)
        Output: None
        """

        await self.open_account(context.author)
        await context.send(f"Lost {amount} coins")
        await self.subtract_money(context.author, amount)

    async def add_money(self, user, amount):
        """ Helper function, adds money to user's pouch

        Input:  discord.User, amount(Str)
        Output: (Bool) False if user does not exist in the bank, True otherwise
        """

        users = await self.get_bank_data()

        if str(user.id) not in users:
            return False       

        else:
            users[str(user.id)]["pouch"] += int(amount)
            with open('centralbank.json', 'w') as file:
                json.dump(users,file)
            return True

    async def subtract_money(self, user, amount):
        """ Helper function, subtracts money from user's pouch

        Input:  discord.User, amount(Str)
        Output: (Bool) False if user does not exist in the bank, True otherwise
        """

        users = await self.get_bank_data()

        if str(user.id) not in users:
            return False       

        else:
            users[str(user.id)]["pouch"] -= int(amount)
            with open('centralbank.json', 'w') as file:
                json.dump(users,file)
            return True

    async def open_account(self,user):
        """ Helper function, adds an entry to the centralbank.json

        Input:  discord.User
        Output: (Bool) False if user already exist in the bank, returns True if/once the user has an account in the bank
        """

        users = await self.get_bank_data()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["pouch"] = 0
            users[str(user.id)]["bank"] = 0

        with open('centralbank.json', 'w') as file:
            json.dump(users, file)
        
        return True

    async def get_bank_data(self):
        """ Helper function, gets all the entries in the centralbank.json

        Input:  None
        Output: (Dict) all user centralbank accounts
        """

        with open('centralbank.json', 'r') as file:
            users = json.load(file)
        return users

    async def get_user_pouch_value(self, user):
        """ Helper function, gets a specific user's pouch value

        Input:  discord.User
        Output: (Int) pouch value of user
        """

        with open('centralbank.json', 'r') as file:
            users = json.load(file)
        return users[str(user.id)]["pouch"]

def setup(bot):
    bot.add_cog(Economy(bot))