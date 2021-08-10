# bot.py
from dis import disco
import os
import random
import datetime
import re
import discord
from urllib.request import Request, urlopen
import json

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
async def buckibot(ctx):
    response = 'Nathan how could you do this to me'
    await ctx.send(response)
    
@bot.command(name='butterdog', help='The dog with the butter on it')
async def butterdog(ctx):
    await ctx.send(file=discord.File("butterdog.jpg"))

imposter_names = ['Ethan', 'Daniel', 'Nathan', 'Sujay', 'Archana', 'Dr. Elizabeth', 'Grace', 'Karin', 'Nick', 'Tiffany', 'Dr. Wynne', 'Kevin', 'Bib']
@bot.command(name='imposter', help='There is one imposter among us')
async def imposter(ctx):
    imposter_name = imposter_names[sum([ord(c) for c in str(datetime.date.today())]) % len(imposter_names)] # converts date into unique list idx
    response = imposter_name + ' is the imposter today'
    await ctx.send(response)
  
conch_answers = ["Yes.", "No.", "Maybe someday.", "Nothing.", "Neither.", "I don't think so.", "Try asking again."]
@bot.command(name='conch', help='The Magic Conch shell')
async def conch(ctx):
    response = random.choice(conch_answers)
    await ctx.send(response)
   
@bot.command(name='ygo', help='Display a random YuGiOh card')
async def ygo(ctx, *args):
    if len(args):
        req = Request('https://db.ygoprodeck.com/api/v7/cardinfo.php?name=' + "%20".join(args), headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read().decode('utf8')
        obj = json.loads(webpage)
        response = obj['data'][0]['card_images'][0]['image_url']
    else:
        req = Request('https://db.ygoprodeck.com/api/v7/randomcard.php', headers={'User-Agent': 'Mozilla/5.0'})     
        webpage = urlopen(req).read().decode('utf8')
        obj = json.loads(webpage)
        response = obj['card_images'][0]['image_url']
    await ctx.send(response)
    
@bot.command(name='pfuse', help='Display a fused sprite of two Gen 1 Pokemon')
async def pfuse(ctx, *args):
    with open('gen1_pokemon.json') as f:
        pokemon_mapping = json.load(f)
        poke1 = args[0] if len(args) > 0 else random.choice(list(pokemon_mapping.keys()))
        poke2 = args[1] if len(args) > 1 else random.choice(list(pokemon_mapping.keys()))
        poke1_id = poke1 if poke1.isnumeric() and int(poke1) > 0 and int(poke1) < 152 else pokemon_mapping.get(poke1.lower(), "1")
        poke2_id = poke2 if poke2.isnumeric() and int(poke2) > 0 and int(poke2) < 152 else pokemon_mapping.get(poke2.lower(), "1")
        response = f"https://images.alexonsager.net/pokemon/fused/{poke1_id}/{poke1_id}.{poke2_id}.png"
        await ctx.send(response)

@bot.command(name='mtg', help='Display a MTG card')
async def mtg(ctx, *args):
    if len(args):
        req = Request('https://api.scryfall.com/cards/named?fuzzy=' + "%20".join(args), headers={'User-Agent': 'Mozilla/5.0'})
    else: 
        req = Request('https://api.scryfall.com/cards/random', headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read().decode('utf8')
    obj = json.loads(webpage)
    if 'card_faces' in obj.keys():
        if 'image_uris' in obj.keys(): # Split cards
            response = obj['image_uris']['normal']
        else: # Dual faced cards
            response = '\n'.join([face['image_uris']['normal'] for face in obj['card_faces']])
    else:
        response = obj['image_uris']['normal']
    await ctx.send(response)
   
@bot.command(name='norm', help='Probably inappropriate jokes with Norm Macdonald')
async def norm(ctx):
    with open("jokes.list", 'r') as f:
        jokes = f.read().split('\n,\n')

    response = random.choice(jokes)
    await ctx.send(response)
    
@bot.command(name='sus', help='When the...')
async def sus(ctx):
    await ctx.send(file=discord.File("sus.png"))
    
@bot.command(name='when', help='When in doubt...')
async def when(ctx, *args):
    joined_arg = ' '.join(args)
    if 'in doubt' in joined_arg:
        choices = ['Katie', 'Nathan', 'Dr. Wynne']
        choice = choices[datetime.datetime.now().minute % 3]
        response = choice + ' out'
        await ctx.send(response)

@bot.command(name='mad', help='I am very mad')
async def mad(ctx):
    response = "I am very mad. I drove all the way to CSU to play in a tournament, get stuck in traffic and lost against these stupid ass libs. Down threw polices and wouldn't stop stalling I really cannot think straight right now. I offered to MM him for more than $20. Nope. I thought I would have made it out of pools if I knew how to fucking pass a policy. But they didn't even give me the frames to do it. Bullshit, just straight up bullshit. Probably will never go to a tournament that dumb ass libs enter ever again. This definitely ruined my day."
    await ctx.send(response)

@bot.command(name='burn', help='I honestly don\'t know')
async def burn(ctx):
    response = 'My name is Nathan Bucki. \n I used to be a nerd, until...\n "We got a doctorate on you. You\'re rich."\n whistles\n When you\'re rich, you have everything.\n Tons of cash,\n Perfect credit.\n You\'re free to leave whatever resort you decide to stay in.\n "Where am I?"\n "Hawai\'i."\n You do whatever work is worthy of you.\n You narrow down all those who keep talking to you.\n A spending-happy ex best friend -\n "Shall we snake some ice cold cruisers?"\n An old roommate who used to inform on you to your high school buddy -\n "You know theorists. A bunch of bitchy little girls."\n Family too -\n "Bitch, I fly fighter jets."\n If you\'re desperate.\n Bottom line, as long as you\'re rich, you\'re going anywhere.'
    await ctx.send(response)

@bot.command(name='persona4', help='Every day\'s great at your Junes!')
async def persona4(ctx):
    print("persona4")
    response = "https://media1.tenor.com/images/8dbdda6b59364b8cdff469889a68924f/tenor.gif?itemid=17075642"
    await ctx.send(response)

command_list = [rice_maps, sujay, mike, cynical, korn, corn, developers, buckibot, butterdog, imposter, conch, pfuse, mtg, norm, sus, when, mad, burn]
@bot.command(name='zombocom', help='Anything is possible')
async def zombocom(ctx):
    await random.choice(command_list)(ctx)

@bot.command(name='github', help='GitHub repo link')
async def github(ctx):
    response = 'https://github.com/dmw2174/ChickenKitchenBot'
    await ctx.send(response)
    
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
