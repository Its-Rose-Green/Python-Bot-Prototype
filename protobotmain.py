import os
import json
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
    await ctx.send('pong')

'''TRAVELLING'''
# Reacting to a preset destination in the travel-destinations text channel will DM the reactor and invite
# to whatever destination server they reacted to.

# TODO: kick the user out of the original server after sending the invite
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id

    # compares the channel id of the message being reacted to, to every channel in that guild, making sure it only executes when
    # the name of the text channel is travel-destination
    if (payload.channel_id == discord.utils.get(bot.get_guild(payload.guild_id).channels, name='travel-destinations').id):
        msg = await bot.get_channel(payload.channel_id).fetch_message(message_id)
        if (msg.content == 'Windvale'):
            # A link to the Windvale discord will be sent
            await payload.member.send('https://discord.gg/jJ3FetRgVu')
        if (msg.content == 'HQ'):
            # A link to the HQ discord will be sent
            await payload.member.send('https://discord.gg/MVGm6gFS42')
        await msg.remove_reaction(payload.emoji, payload.member)

'''TAVERN THINGS'''
@bot.command()
async def purchase(ctx, amount: int, item):
    if (ctx.channel.id != discord.utils.get(ctx.guild.channels, name='tavern').id):
        return
    else:
        await ctx.send("You have purchased " + str(amount) + " " + item)
    
'''ECONOMY THINGS'''
@bot.command()
async def balance(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    pouch_amt = users[str(ctx.author.id)]["pouch"]
    bank_amt = users[str(ctx.author.id)]["bank"]

    em = discord.Embed(title = f"{ctx.author.name}'s balance")
    em.add_field(name = "Pouch Amount", value = pouch_amt)
    em.add_field(name = "Bank Balance", value = bank_amt)
    await ctx.send(embed = em)

@bot.command()
@commands.has_role('Creator')
async def give_myself_money(ctx):
    await open_account(ctx.author)
    users = await get_bank_data()

    earnings = 1000
    await ctx.send(f"Obtained {earnings} coins")

    users[str(ctx.author.id)]["pouch"] += earnings

    with open('centralbank.json', 'w') as file:
        json.dump(users,file)

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["pouch"] = 0
        users[str(user.id)]["bank"] = 0

    with open('centralbank.json', 'w') as file:
        json.dump(users, file)
    
    return True

async def get_bank_data():
    with open('centralbank.json', 'r') as file:
        users = json.load(file)
    return users

'''FIGHTING'''
# Turn-taking prototype - fix it up later for our purposes
@bot.command()
async def test(ctx, user: discord.Member):
    turn = 0
    aut = 5
    ops = 5
    userM = user.mention
    cmam = ctx.message.author.mention
    if user == cmam:
        await ctx.send(f"You can't fight yourself {cmam}")
    else:
        await ctx.send(f"{cmam} vs {userM}, who will win?")
        while aut > 0 and ops > 0:
            # Turn 1
            if turn == 0:
                await ctx.send(f"{cmam}: `test`")
                def check(m):
                    return m.content == "test" and m.author == ctx.message.author
                response = await bot.wait_for('message', check = check)
                if "test" in response.content.lower() and turn == 0:
                    await ctx.send("a nice test")
                    turn = turn + 1
            # Turn 2
            elif turn == 1:
                await ctx.send(f"{userM}: `test`")
                def check(o):
                    return o.content == "test" and o.author == user
                response = await bot.wait_for('message', check = check)
                if "test" in response.content.lower() and turn == 1:
                    await ctx.send("the test is strong with this one")
                    turn = turn - 1

bot.run(TOKEN)
