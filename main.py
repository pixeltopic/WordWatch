import discord
from discord.ext import commands
import asyncio
import calendar
import time
from collections import defaultdict

bot = commands.Bot(command_prefix='..', description='TextPing Bot')

bot.user_words = defaultdict(dict)
# bot.user_cds = defaultdict(int)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)

# TODO: custom help command, bot stop command

@bot.command()
async def hello():
    print("hi there!")


@bot.command(pass_context=True)
async def deleteword(ctx, *, word):
    """Deletes specified word from the user's pinged words"""
    member = ctx.message.author
    if member.id not in bot.user_words:
        embed = discord.Embed(title="You don't have any words added.", color=0x39c12f)
    else:
        for pingedword in bot.user_words[member.id].keys():
            if pingedword == word:
                embed = discord.Embed(title="\"{}\" deleted from ping list".format(word), color=0x39c12f)
                bot.user_words[member.id].pop(word, None)
                await bot.say(embed=embed)
                print(dict(bot.user_words))
                return
        embed = discord.Embed(title="\"{}\" was not found on your ping list".format(word), color=0x39c12f)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def pingword(ctx, *, word):
    """Adds word to user's pinged word list along with timestamp of when"""
    member = ctx.message.author

    if member.id not in bot.user_words:
        bot.user_words[member.id] = {word: calendar.timegm(time.gmtime())}
        embed = discord.Embed(title="\"{}\" added to ping list".format(word), color=0x39c12f)
    else:
        for pingedword in bot.user_words[member.id].keys():
            if pingedword == word:
                embed = discord.Embed(title="You are already pinged for \"{}\"".format(word), color=0x39c12f)
                await bot.say(embed=embed)
                print(dict(bot.user_words))
                return
        bot.user_words[member.id][word] = calendar.timegm(time.gmtime())
        embed = discord.Embed(title="\"{}\" added to ping list".format(word), color=0x39c12f)

    await bot.say(embed=embed)
    print(dict(bot.user_words))
    print(member.id)
    user= await bot.get_user_info(member.id)
    await bot.send_message(user, embed=embed)

# TODO: view your pinged words command.


@bot.event
async def on_message(message):
    # TODO: check keyword in ALL channels, or just certain ones
    if "51" in message.content or "33" in message.content:
        print("ping user")
        print("channel:", message.channel)
    await bot.process_commands(message)

bot.run('Mzc0NzYxNDQwMjU2NDU4NzUy.DNmAsw.NmWQZLK9zDhSlvXntrFzPBQnHAM')
