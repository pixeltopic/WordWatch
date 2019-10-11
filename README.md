# WordWatch Setup

To run this bot on a Discord server: <br />
1. Visit `https://discordapp.com/developers/applications/me` and set up a bot account. <br />
2. Copy the Client/Application ID. <br />
3. Go to `https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID_GOES_HERE&scope=bot&permissions=0`. <br />
4. Authorize bot access to your desired server. <br />
5. Make sure you've done `pip install discord.py` in command prompt if you don't have it already. <br />
6. Obtain bot token from the developer page. <br />
7. On bot_token.py replace the bot-token placeholder with a valid token. <br />

The bot can now be run! <br />
# About

WordWatch is a Discord chat bot that can track key words and phrases. For example, if a user wants to track the phrase `lorem ipsum` and be alerted every time that phrase is used in a conversation, all they would need to do is run a simple command.
Users can easily customize notification frequency and choose which channels of a server they want the bot to scan messages for.

The inspiration for this bot stems from a conversation on the UCI Discord Server. A user asked if it was possible to track certain phrases (such as UCI courses) and be notified whenever the term appears in conversations.
I ended up creating this chat bot in about 16 hours over the course of 4 days.

# Commands
The bot uses the prefix `..` to invoke commands.

Calling a command in the chat (example demonstrates the `help` command): `..help`

Note: Phrases must be wrapped in quotes but single words don't. Also, commands will not work outside servers the bot is running in.

1. `help` - Displays documentation in chat on how to use the bot.

2. `watched` - Gives user list of all watched words/phrases on the server. Also shows current `cd` setting.

3. `watchword "word" [channels (optional)]` - Start watching a word and be alerted according to your `cd` setting. Channels can be filtered, skipping the `addfilter` step. Simply list channels after the word/phrase separated by spaces.

`..watchword "lorem ipsum" #general` <br />
`..watchword lorem #general #off-topic` <br />
`..watchword "lorem ipsum"` <br />
`..watchword lorem`

4. `deleteword "word"` - Deletes the specified word/phrase from your watch list.

`..deleteword "lorem ipsum"` <br />
`..deleteword lorem`

5. `watchclear` - Clears all watched words/phrases that you are watching.

6. `cd [minutes]` - Toggle how long before you want to be alerted again after the most recent alert. Set at 15 minutes by default.

`..cd` <br />
`..cd 3`

7. `worddetail "word"` - Tells you the filtered channels enabled for the word/phrase and time the word/phrase was last seen.

`..worddetail "lorem ipsum"` <br />
`..worddetail lorem`

8. `addfilter "word" [channels]` - Start watching for word/phrase in specified channels. Will not replace previously watching channels.

`..addfilter lorem #general #games`

9. `deletefilter "word" [channels]` - Stop watching for word/phrase in specified channels.

`..deletefilter "lorem ipsum" #off-topic #general`

10. `clearfilter "word"` - Remove all filters from word/phrase; watch entire server instead.

`..clearfilter "lorem ipsum"` <br />
`..clearfilter lorem`

11. `forcesave` - Force saves all current data into the JSON files. Admin only!

12. `botstop` - Saves data and logs out bot. Admin only!