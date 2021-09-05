#!/usr/bin/python3
import discord
import json
from discord.ext import commands

class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="balance")
    async def balance(self, context):
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
        await self.open_account(context.author)
        await context.send(f"Obtained {amount} coins")
        await self.add_money(context.author, amount)

    @commands.command(name="donate_to_thin_air")
    async def donate_to_thin_air(self, context, amount):
        await self.open_account(context.author)
        await context.send(f"Lost {amount} coins")
        await self.subtract_money(context.author, amount)

    async def add_money(self, user, amount):
        users = await self.get_bank_data()

        if str(user.id) not in users:
            return False       

        else:
            users[str(user.id)]["pouch"] += int(amount)
            with open('centralbank.json', 'w') as file:
                json.dump(users,file)

    async def subtract_money(self, user, amount):
        users = await self.get_bank_data()

        if str(user.id) not in users:
            return False       

        else:
            users[str(user.id)]["pouch"] -= int(amount)
            with open('centralbank.json', 'w') as file:
                json.dump(users,file)

    async def open_account(self,user):
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
        with open('centralbank.json', 'r') as file:
            users = json.load(file)
        return users

    async def get_user_pouch_value(self, user):
        with open('centralbank.json', 'r') as file:
            users = json.load(file)
        return users[str(user.id)]["pouch"]

def setup(bot):
    bot.add_cog(Economy(bot))