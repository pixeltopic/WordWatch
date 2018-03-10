import discord
from discord.ext import commands
import calendar
import time
from collections import defaultdict
from bot_token import token

prefix = ".."
bot = commands.Bot(command_prefix=prefix, description='WordWatch Bot')

bot.prefix = prefix
bot.user_words = defaultdict(dict)
bot.user_cds = defaultdict(int)


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)

# TODO: custom help command, bot stop command.
# TODO: channel filtering. NOTE: limit term search to server in case they share names
# TODO: saving user data via json


@bot.command(pass_context=True)
async def cd(ctx, mins=15.0):
    """Set cooldown (in minutes) for each word. If no parameter, automatically defaults to 15 minutes"""
    if mins >= 0:
        bot.user_cds[ctx.message.author.id] = int(mins)*60
        embed = discord.Embed(title="Notification cooldown set to {} min".format(int(mins)), color=0x39c12f)
    else:
        embed = discord.Embed(title="Minute cooldown must be positive.", color=0xe23a1d)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def deleteword(ctx, *, word):
    """Deletes specified word from the user's pinged words"""
    member = ctx.message.author
    if member.id not in bot.user_words:
        embed = discord.Embed(title="You don't have any words added.", color=0x39c12f)
    else:
        for watchedword in bot.user_words[member.id].keys():
            if watchedword == word:
                embed = discord.Embed(title="\"{}\" deleted from watch list".format(word), color=0x39c12f)
                bot.user_words[member.id].pop(word, None)
                await bot.say(embed=embed)
                print(dict(bot.user_words))
                return
        embed = discord.Embed(title="\"{}\" was not found on your watch list".format(word), color=0x39c12f)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def watchword(ctx, *, word):
    """Adds word to user's watched word list along with timestamp of when"""
    member = ctx.message.author

    if member.id not in bot.user_words:
        bot.user_words[member.id] = {word: calendar.timegm(time.gmtime())}
        embed = discord.Embed(title="\"{}\" added to watch list".format(word), color=0x39c12f)
        if member.id not in bot.user_cds:
            bot.user_cds[member.id] = 15 * 60
    else:
        for watchedword in bot.user_words[member.id].keys():
            if watchedword == word:
                embed = discord.Embed(title="You are already watching \"{}\"".format(word), color=0x39c12f)
                await bot.say(embed=embed)
                print(dict(bot.user_words))
                return
        bot.user_words[member.id][word] = calendar.timegm(time.gmtime())
        embed = discord.Embed(title="\"{}\" added to watch list".format(word), color=0x39c12f)

    await bot.say(embed=embed)
    print(dict(bot.user_words))


@bot.command(pass_context=True)
async def watched(ctx):
    member = ctx.message.author
    if member.id not in bot.user_cds:
        bot.user_cds[member.id] = 15 * 60
    if member.id not in bot.user_words:
        bot.user_words[member.id] = dict()
        watched_str = "No words or phrases currently watched."
    elif bot.user_words[member.id] != dict():
        watched_str = ""
        for watchedword in bot.user_words[member.id].keys():
            watched_str += "\"{}\", ".format(watchedword)
        watched_str = watched_str[:-2]
    else:
        watched_str = "No words or phrases currently watched."
    embed = discord.Embed(
        title="{}'s watched words/phrases".format(member.name), description=watched_str, color=0x76c7e9)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Cooldown: {} min".format(int(bot.user_cds[member.id]/60)))
    await bot.say(embed=embed)


@bot.event
async def on_message(message):
    current_time = calendar.timegm(time.gmtime())

    for mem in bot.user_words.keys():
        for keyword, timestamp in bot.user_words[mem].items():
            # print(word, timestamp)
            if keyword in message.content and current_time-timestamp >= bot.user_cds[mem] and message.content[:2] != bot.prefix:
                bot.user_words[mem][keyword] = current_time
                user = await bot.get_user_info(mem)
                embed = discord.Embed(title="A watched word/phrase was detected!", color=0xeb8d25)
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/421783600246161408/421912111132704799/alertimage.gif")
                embed.add_field(name="Server", value=message.server, inline=False)
                embed.add_field(name="Channel", value=message.channel, inline=False)
                embed.add_field(name="Author", value=message.author, inline=False)
                embed.add_field(name="Content", value=message.content, inline=False)
                embed.set_footer(text="Detected message sent at {}".format(message.timestamp))

                await bot.send_message(user, embed=embed)

    await bot.process_commands(message)

bot.run(token)
