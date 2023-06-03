import discord
import random
import time
from discord.ext import commands
import json
from fishing import fishing
from fishing import init
from vocabulary import init_vocabulary
from vocabulary import compare_vocabulary
from vocabulary import get_vocabulary

#################### Data Base ############################

from database import registered
from database import query_money
from database import adding_money
from database import query_account_vocabulary
from database import query_times
from database import vocabulary_insert

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
######## Account #########

@bot.slash_command(name="register",description="將你的 Discord 帳號註冊在這一隻機器人上")
async def register(ctx):
    status = registered(ctx.author.id)
    print(ctx.author.id)
    if( status == -1 ): await ctx.respond("你已經註冊過了！")
    else: await ctx.respond("註冊成功！")

@bot.slash_command(name="money",description='查詢當前擁有的金額')
async def announcement(ctx):
    status = ctx.author.id
    check = query_money(status)

    if( check == None ):
        check = 0

    if( check == -1 ): # 還沒註冊的 User
        await ctx.respond('你還沒有註冊帳號，請使用 /register 註冊你的 Discord 帳號資訊到資料庫中！')
    else:
        await ctx.respond('你目前擁有的金額為 ' f'{check}' ' 元！')

######## Fishing #########

init()

@bot.slash_command(name="fishing",description='釣一隻魚')
async def fish(ctx):
    status = ctx.author.id
    ans = fishing()
    cm = round(random.uniform(0,1000))
    await ctx.respond('你釣起了一隻 'f'{cm}'' cm 的'f'{ans}'' 獲得了 ' f'{cm/10}' ' 元')
    adding_money(status,cm/10)

    if( query_money(ctx.author.id) == -1 ):
        await ctx.respond('你的帳號還沒有註冊到機器人的資料庫中！請使用 /register 指令註冊')

##########################

################################################################


######## QA Game #########

@bot.slash_command(name="vocabulary",description='開始進行猜單字遊戲')
async def vocabulary(ctx):
    init_vocabulary()
    if( query_money(ctx.author.id) == -1 ):
        await ctx.respond('你的帳號還沒有註冊到機器人的資料庫中！請使用 /register 指令註冊後再進行遊戲')
    else:
        await ctx.respond('接下來將開始進行猜單字遊戲，遊戲規則為盡可能的在越少的次數中猜到正確單字！')
        await ctx.send('如果猜錯，我會告訴你哪些位置的字對了，祝你好運！')
        await ctx.send('你可以透過 /guess 來猜單字')

        answer = get_vocabulary()
        word_length = len(answer)
        await ctx.send('你的單字長度為 'f'{word_length}')
        vocabulary_insert(ctx.author.id,answer)


@bot.slash_command(name="guess",description='猜單字')
async def guess(ctx,vocabulary: str):
    if( query_money(ctx.author.id) == -1 ):
        await ctx.respond('你的帳號還沒有註冊到機器人的資料庫中！請使用 /register 指令註冊後再進行遊戲')
    elif( query_account_vocabulary(ctx) == "None Start" ):
        await ctx.respond('請先使用指令 /vocabulary 開始遊戲')
    else:
        answer = query_account_vocabulary(ctx.author.id)
        times = query_times(ctx.author.id) + 1
        s = compare_vocabulary(ctx.author.id,vocabulary,str(answer))
        
        if( s == "1" ):
            await ctx.respond('恭喜你答對了！正確答案為 'f'{answer}')
            ctx.send('你總共使用了 'f'{times}'' 次猜中答案！')
        else: 
            await ctx.respond('猜錯了！正確的單字會是 'f'{s}'' 請繼續猜！')



bot.run(token)