import discord
from discord.ext import commands
import calendar
import time
import datetime
import asyncio
import json
import os
from bot_token import token

prefix = ".."
bot = commands.Bot(command_prefix=prefix, description='WordWatch Bot')
bot.remove_command('help')  # removes default help command!

# Const attributes
bot.prefix = prefix
bot.user_words_file = "userwords.json"
bot.user_cds_file = "usercds.json"
bot.thumb = "https://raw.githubusercontent.com/pixeltopic/WordWatch/master/alertimage.gif"
bot.static = -1  # used for channel dict values to mimic a set

# Non-Constants
bot.user_words = dict()
bot.user_cds = dict()
bot.last_checked = -1  # throttles event checking to prevent overload


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print("Warning: bot requires both {} and {} to load data.".format(bot.user_words_file, bot.user_cds_file))
    if os.path.isfile("./" + bot.user_words_file) and os.path.isfile("./" + bot.user_cds_file):
        # bot.user_words = json.load(open(bot.user_words_file, "r"))
        # bot.user_cds = json.load(open(bot.user_cds_file, "r"))
        with open(bot.user_words_file) as word_data:
            bot.user_words = json.load(word_data)
        with open(bot.user_cds_file) as cd_data:
            bot.user_cds = json.load(cd_data)
        print("Data loaded successfully.")
    else:
        print("No data files provided or one was missing. No user data loaded.")
    await bot.change_presence(game=discord.Game(name="Looking for text..."))


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="WordWatch Bot", description="Checks messages for key words and notifies you!", color=0x30abc0)
    embed.set_thumbnail(url=bot.thumb)
    embed.set_footer(text="by pixeltopic")
    await bot.send_message(ctx.message.author, embed=embed)

    embed = discord.Embed(title="WordWatch Bot Commands", description="Do {prefix}help to open this. Bot Prefix: {prefix}".format(prefix=bot.prefix), color=0xa3a3a3)
    embed.set_thumbnail(url="")
    embed.add_field(name="watched",
                    value="Gives user list of all watched words/phrases on the server",
                    inline=False)
    embed.add_field(name="watchword \"word\" [channels (optional)]",
                    value="""
                    Start watching a word, receiving alerts based on your cooldown setting. Add channels separated by spaces after to only watch those channels for word/phrase.\neg. `{prefix}watchword "hey there" #general #off-topic`
                    """.format(prefix=bot.prefix), inline=False)
    embed.add_field(name="deleteword \"word\"", value="Delete a word or phrase. Phrases must be wrapped in quotes.", inline=False)
    embed.add_field(name="watchclear", value="Clears all watched words/phrases that you are watching.",
                    inline=False)
    embed.add_field(name="cd [minutes]",
                    value="Toggle how long before you want to be alerted again after the most recent alert", inline=False)
    embed.add_field(name="worddetail \"word\"",
                    value="Gives you details of a watched word/phrase.", inline=False)
    embed.add_field(name="addfilter \"word\" [channels]",
                    value="Based on word/phrase and channels separated by spaces, only watch for it in those channels",
                    inline=False)
    embed.add_field(name="deletefilter \"word\" [channels]",
                    value="Based on word/phrase and channels separated by spaces, stop watching it in those channels",
                    inline=False)
    embed.add_field(name="clearfilter \"word\"",
                    value="Based on word/phrase, removes all enabled filters from it.",
                    inline=False)
    embed.set_footer(text="Phrases must be wrapped in quotes but single words don't. Commands will not work when DMing bot.")

    await bot.send_message(ctx.message.author, embed=embed)


def check_user(member):
    """Given a member, check if they are in the dictionary. if not, create one for them."""
    if member.id not in bot.user_words:
        bot.user_words[member.id] = dict()
        bot.user_cds[member.id] = 15 * 60


def check_server(member, server_id):
    """Given a server ID, checks if it exists in the dictionary. Intended to be used after check_user"""
    if server_id not in bot.user_words[member.id]:
        bot.user_words[member.id][server_id] = dict()


def ensure_valid_channels(member, server, word):
    """If a word's watched channel is nonxistent, removes it from the dict to prevent errors"""
    result = dict()
    # print("Server channels:", [x.id for x in server.channels])
    if word not in bot.user_words[member.id][server.id].keys():
        return
    all_channels = [x.id for x in server.channels]
    for channel_id in bot.user_words[member.id][server.id][word]["channels"].keys():
        if channel_id[2:-1] in all_channels:
            result[channel_id] = bot.static
    bot.user_words[member.id][server.id][word]["channels"] = result


def get_timeStamp() -> str:
    """Returns current time (hr:min:sec)"""
    return datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')


def write_to_json():
    """Opens .json files and writes data into it"""
    user_word_str = json.dumps(bot.user_words)
    user_cd_str = json.dumps(bot.user_cds)

    f = open(bot.user_words_file, "w+")
    f.write(user_word_str)
    f.close()
    f = open(bot.user_cds_file, "w+")
    f.write(user_cd_str)
    f.close()
    print("Saving user data @ {}".format(get_timeStamp()))


# TODO: add instructions on how to use commands on the commands themselves for good documentation. eg word = ""


# example_dict = {"user id":
#     {"server": {
#             "word":
#                 {"last_alerted": 0, "channels": dict()}
#             }
#         }
#     }


@bot.command(pass_context=True)
async def cd(ctx, mins=15.0):
    """Set cooldown (in minutes) for each word. If no parameter, automatically defaults to 15 minutes"""
    if ctx.message.server == None:
        return
    check_user(ctx.message.author)
    if mins >= 0:
        bot.user_cds[ctx.message.author.id] = int(mins)*60
        embed = discord.Embed(title="Notification cooldown set to {} min".format(int(mins)), color=0x39c12f)
    else:
        embed = discord.Embed(title="Minute cooldown must be positive.", color=0xe23a1d)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def deleteword(ctx, word):
    """Deletes specified word from the user's pinged words"""
    if ctx.message.server == None:
        return

    member = ctx.message.author
    server_id = ctx.message.server.id

    check_user(member)
    check_server(member, server_id)
    if len(bot.user_words[member.id][server_id]) == 0:
        embed = discord.Embed(title="You don't have any words added.", color=0xe23a1d)
        await bot.say(embed=embed)
        return

    if word in bot.user_words[member.id][server_id].keys():
        embed = discord.Embed(title="\"{}\" deleted from watch list".format(word), color=0x39c12f)
        bot.user_words[member.id][server_id].pop(word, None)
        await bot.say(embed=embed)
        # print(dict(bot.user_words))
        return

    embed = discord.Embed(title="\"{}\" was not found on your watch list".format(word), color=0xe23a1d)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def watchclear(ctx):
    """Clears all the user's watched words."""
    if ctx.message.server == None:
        return

    member = ctx.message.author
    server_id = ctx.message.server.id

    check_user(member)
    check_server(member, server_id)

    bot.user_words[member.id][server_id] = dict()

    embed = discord.Embed(title="Your watch list is cleared.", color=0x39c12f)
    await bot.say(embed=embed)



@bot.command(pass_context=True)
async def watchword(ctx, word, *args):
    """Adds word to user's watched word list along with timestamp of when. optionally, allow channel filtering"""
    if ctx.message.server == None:
        return

    member = ctx.message.author
    server_id = ctx.message.server.id

    check_user(member)
    check_server(member, server_id)

    if word in bot.user_words[member.id][server_id].keys():
        embed = discord.Embed(title="You are already watching \"{}\"".format(word), color=0x39c12f)
        await bot.say(embed=embed)
        return

    for channel in args:
        if channel[:2] != "<!#" and channel[-1:] != ">":
            embed = discord.Embed(title="Invalid channel(s), use the \"#\" symbol to select channel.", color=0xe23a1d)
            await bot.say(embed=embed)
            return

    bot.user_words[member.id][server_id][word] = {"last_alerted": calendar.timegm(time.gmtime()),
                                                  "channels": {x: bot.static for x in args}}
    if len(args) == 0:
        embed = discord.Embed(title="\"{}\" added to watch list".format(word), color=0x39c12f)
        embed.set_footer(text="Watching entire server. Use \"{}addfilter\" to only watch certain channels.".format(bot.prefix))
    else:
        embed = discord.Embed(title="\"{}\" added to watch list".format(word), color=0x39c12f)
        embed.set_footer(text="Watching {}".format(", ".join({"#"+bot.get_channel(x[2:-1]).name for x in args})))
    await bot.say(embed=embed)
    # print(dict(bot.user_words))


@bot.command(pass_context=True)
async def worddetail(ctx, word):
    """Gives user details for a watched word or phrase."""
    if ctx.message.server == None:
        return

    member = ctx.message.author
    server_id = ctx.message.server.id

    check_user(member)
    check_server(member, server_id)
    ensure_valid_channels(member, ctx.message.server, word)
    if word in bot.user_words[member.id][server_id].keys():
        data = bot.user_words[member.id][server_id][word]
        embed = discord.Embed(title="Word Details for {}".format(member.name), color=0xeb8d25)
        embed.add_field(name="Word/Phrase", value=word, inline=False)
        channels_watching = ", ".join({"#"+bot.get_channel(x[2:-1]).name for x in data["channels"].keys()})
        embed.add_field(name="Channels watching", value="All channels" if channels_watching == "" else channels_watching, inline=False)
        current_time = calendar.timegm(time.gmtime())
        embed.add_field(name="Last seen", value=str((current_time - data["last_alerted"])//60) + " min ago", inline=False)

    else:
        embed = discord.Embed(title="\"{}\" was not found on your watch list".format(word), color=0xe23a1d)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def addfilter(ctx, word, *args):
    """Adds filter to specified word"""
    if ctx.message.server == None:
        return

    member = ctx.message.author
    server_id = ctx.message.server.id

    check_user(member)
    check_server(member, server_id)
    if len(args) == 0:
        embed = discord.Embed(title="No channels specified.", color=0xe23a1d)
        await bot.say(embed=embed)
        return

    for channel in args:
        if channel[:2] != "<!#" and channel[-1:] != ">":
            embed = discord.Embed(title="Invalid channel(s), use the \"#\" symbol to select channel.", color=0xe23a1d)
            await bot.say(embed=embed)
            return

    if word in bot.user_words[member.id][server_id].keys():
        bot.user_words[member.id][server_id][word]["channels"].update({x: bot.static for x in args})
        embed = discord.Embed(title="{} added to \"{}\"".format(", ".join({"#"+bot.get_channel(x[2:-1]).name for x in args}), word), color=0x39c12f)
        await bot.say(embed=embed)
        return
    embed = discord.Embed(title="\"{}\" is not being watched.".format(word), color=0xe23a1d)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def deletefilter(ctx, word, *args):
    """Removes filter from specified word"""
    if ctx.message.server == None:
        return

    member = ctx.message.author
    server_id = ctx.message.server.id

    check_user(member)
    check_server(member, server_id)

    if len(args) == 0:
        embed = discord.Embed(title="No channels specified.", color=0xe23a1d)
        await bot.say(embed=embed)
        return

    for channel in args:
        if channel[:2] != "<!#" and channel[-1:] != ">":
            embed = discord.Embed(title="Invalid channel(s), use the \"#\" symbol to select channel.", color=0xe23a1d)
            await bot.say(embed=embed)
            return

    if word in bot.user_words[member.id][server_id].keys():
        for to_remove in args:
            bot.user_words[member.id][server_id][word]["channels"].pop(to_remove, None)
        embed = discord.Embed(title="{} removed from \"{}\"".format(", ".join({"#"+bot.get_channel(x[2:-1]).name for x in args}), word), color=0x39c12f)
        await bot.say(embed=embed)
        return
    embed = discord.Embed(title="\"{}\" is not being watched.".format(word), color=0xe23a1d)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def clearfilter(ctx, word):
    """Clears filter from specified word"""
    if ctx.message.server == None:
        return

    member = ctx.message.author
    server_id = ctx.message.server.id

    check_user(member)
    check_server(member, server_id)

    if word in bot.user_words[member.id][server_id].keys():
        bot.user_words[member.id][server_id][word]["channels"] = dict()
        embed = discord.Embed(title="All filters removed from \"{}\"".format(word), color=0x39c12f)
        embed.set_footer(text="Now watching entire server for word/phrase.")
        await bot.say(embed=embed)
        return
    embed = discord.Embed(title="\"{}\" is not being watched.".format(word), color=0xe23a1d)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def watched(ctx):
    """Shows user a list of their watched words"""
    if ctx.message.server == None:
        return
    member = ctx.message.author
    server_id = ctx.message.server.id

    check_user(member)
    check_server(member, server_id)

    if bot.user_words[member.id][server_id] != dict():
        watched_str = ""
        for watchedword in bot.user_words[member.id][server_id].keys():
            watched_str += "\"{}\", ".format(watchedword)
        watched_str = watched_str[:-2]
    else:
        watched_str = "No words or phrases currently watched."
    embed = discord.Embed(
        title="{}'s watched words/phrases".format(member.name), description=watched_str, color=0x76c7e9)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Notification Cooldown Preference: {} min".format(int(bot.user_cds[member.id]/60)))
    await bot.say(embed=embed)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    current_time = calendar.timegm(time.gmtime())

    if (bot.last_checked == -1 or current_time - bot.last_checked >= 5) and message.content[:2] != bot.prefix:
        # print("Check Paused.")
        bot.last_checked = current_time

        for mem in bot.user_words.keys():
            if message.server.id in bot.user_words[mem]:
                for keyword, innerdict in bot.user_words[mem][message.server.id].items():
                    if len(innerdict["channels"]) == 0 and \
                            keyword in message.content and \
                            current_time-innerdict["last_alerted"] >= bot.user_cds[mem] and \
                            message.content[:2] != bot.prefix:

                        # print("ping for whole server: ", keyword)

                        bot.user_words[mem][message.server.id][keyword]["last_alerted"] = current_time
                        user = await bot.get_user_info(mem)
                        embed = discord.Embed(title="A watched word/phrase was detected!", color=0xeb8d25)
                        embed.set_thumbnail(url=bot.thumb)
                        embed.add_field(name="Server", value=message.server, inline=False)
                        embed.add_field(name="Channel", value=message.channel, inline=False)
                        embed.add_field(name="Author", value=message.author, inline=False)
                        embed.add_field(name="Content", value=message.content, inline=False)
                        embed.set_footer(text="Detected message sent at {}".format(message.timestamp))
                        await bot.send_message(user, embed=embed)

                    elif "<#"+message.channel.id+">" in innerdict["channels"] and \
                            keyword in message.content and \
                            current_time-innerdict["last_alerted"] >= bot.user_cds[mem] and \
                            message.content[:2] != bot.prefix:

                        # print("ping!", keyword, message.channel.id)

                        bot.user_words[mem][message.server.id][keyword]["last_alerted"] = current_time
                        user = await bot.get_user_info(mem)
                        embed = discord.Embed(title="A watched word/phrase was detected!", color=0xeb8d25)
                        embed.set_thumbnail(url=bot.thumb)
                        embed.add_field(name="Server", value=message.server, inline=False)
                        embed.add_field(name="Channel", value=message.channel, inline=False)
                        embed.add_field(name="Author", value=message.author, inline=False)
                        embed.add_field(name="Content", value=message.content, inline=False)
                        embed.set_footer(text="Detected message sent at {}".format(message.timestamp))
                        await bot.send_message(user, embed=embed)

    await bot.process_commands(message)


async def save_json():
    """Saves user data in JSON format periodically."""
    await bot.wait_until_ready()
    while not bot.is_closed:
        await asyncio.sleep(900)  # task runs every 900 seconds (15 mins)
        write_to_json()


@bot.command()
async def botstop():
    """Turns off the bot"""
    embed = discord.Embed(title="WordWatch Bot saving data and logging out.", color=0xe23a1d)
    await bot.say(embed=embed)
    print("Saving before logging out...")
    write_to_json()
    print("Done.")
    await bot.logout()

bot.loop.create_task(save_json())
bot.run(token)
