# bot.py
from dis import disco
import os
import random
import datetime
import re
import discord

from glob import glob
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# print(TOKEN)
print(datetime.datetime.today())

bot  = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(
        f'{bot.user.name} has connected to Discord!'
    )

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.command(name='ricemaps', help='Makes sure no one will be as flustered as we were')
async def rice_maps(ctx):
    response = ('When my teammates and I first arrived at Rice University, '
    'we looked around and realized we had no idea where anything was. That\'s '
    'why I, Nathan Bucki, and my team, created Rice Maps: an interactive '
    'mapping service designed so that future freshmen and even upperclassmen '
    'won\'t be as flustered as we were.')
    await ctx.send(response)

@bot.command(name='roll', help='Simulates rolling dice (!roll <X> d<Y>)')
async def roll(ctx, number_of_dice: int, number_of_sides: str):
    number_of_sides = int(number_of_sides.lower().replace('d',''))
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice)+f' (Total: {sum([int(die) for die in dice])})')

@bot.command(name='sujay', help='Wisdom from the Habanero Javanero')
async def sujay(ctx):
    with open("sujay.list", 'r') as f:
        sujay_quotes = f.read().split('\n,\n')

    response = random.choice(sujay_quotes)
    await ctx.send(response)

@bot.command(name='mike', help='Is it Wednesday my dudes?')
async def mike(ctx):
    day_of_the_week = datetime.datetime.today().weekday()
    days_to_wednesday = (7 - (day_of_the_week - 2)) % 7
    if days_to_wednesday == 0:
        response = 'Humpdaaaaaaaaaaaayyyyyyyyyyyy!'
    elif days_to_wednesday == 1:
        response = 'It is almost Wednesday my dudes'
    elif days_to_wednesday == 5:
        response = 'https://www.youtube.com/watch?v=A5U8ypHq3BU'
    else:
        response = f'It is {days_to_wednesday} days until Wednesday'
    await ctx.send(response)

@bot.command(name='cynical', help='Calms down Sujay')
async def cynical(ctx):
    await ctx.send(file=discord.File('cynical.png'))

@bot.command(name='korn', help="why")
async def korn(ctx):
    response = random.choice(glob("kornheiserish/*"))
    await ctx.send(file=discord.File(response))

@bot.command(name='corn', help='Nick in high school')
async def corn(ctx):
    await ctx.send(file=discord.File("corn.png"))

@bot.command(name='developers', help='Developers')
async def developers(ctx):
    await ctx.send(file=discord.File("developers.gif"))

@bot.command(name='buckibot', help='Fuck you Nathan!')
async def buckbot(ctx):
    response = 'Nathan how could you do this to me'
    await ctx.send(response)
    
@bot.command(name='butterdog', help='The dog with the butter on it')
async def butterdog(ctx):
    await ctx.send(file=discord.File("butterdog.jpg"))

command_list = [rice_maps, sujay, mike, cynical, korn, corn, developers, butterdog]
@bot.command(name='zombocom', help='Anything is possible')
async def zombocom(ctx):
    await random.choice(command_list)(ctx)

# @bot.command(name='create-channel')
# @commands.has_role('admin')
# async def create_channel(ctx, channel_name='test-channel'):
#     guild = ctx.guild
#     channel_name = re.sub('[^a-zA-Z0-9-]+', '', channel_name)
#     existing_channel = discord.utils.get(guild.channels, name=channel_name)
#     if not existing_channel:
#         print(f'Creating a new channel : {channel_name}')
#         await guild.create_text_channel(channel_name)


bot.run(TOKEN)
