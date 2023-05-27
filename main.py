import discord
import random
import time
from discord.ext import commands
import json
from fishing import fishing
from fishing import init

#################### Data Base ############################

from database import registered
from database import query_money
from database import adding_money

###########################################################

with open('token.json') as f:
    tokens = json.load(f)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="",intents=intents)
token = tokens['token']

@bot.event
async def on_ready():
    print(">> Bot is online <<")

#################### Slash Commands ############################

######## Fishing #########

init()

@bot.slash_command(name="fishing",description='釣一隻魚')
async def fish(ctx):
    status = ctx.author.id
    ans = fishing()
    cm = round(random.uniform(0,1000))
    await ctx.respond('你釣起了一隻 'f'{cm}'' cm 的'f'{ans}'' 獲得了 ' f'{cm/10}' ' 元')
    adding_money(status,cm/10)

##########################

################################################################



bot.run(token)