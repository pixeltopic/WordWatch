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
Users can customize how often they want to be alerted before getting another alert, and choose which channels of a server they want the bot to scan messages for.

I was inspired to create this chat bot for the UCI Discord Server after a user asked if it was possible to track certain phrases (such as UCI courses) and be notified whenever the term appears in conversations. As a result, I spent about 16 hours in the next 4 days to complete this bot.

# Commands
The bot uses the prefix `..` to invoke commands.

Calling a command in the chat (example demonstrates the `help` command): `..help`

Note: Phrases must be wrapped in quotes but single words don't. Also, commands will not work outside servers the bot is running in.

`help` - Displays documentation in chat on how to use the bot.

`watched` - Gives user list of all watched words/phrases on the server. Also shows current `cd` setting.

`watchword "word" [channels (optional)]` - Start watching a word and be alerted according to your `cd` setting. Channels can be filtered, skipping the `addfilter` step. Simply list channels after the word/phrase separated by spaces.

`..watchword "lorem ipsum" #general`
`..watchword lorem #general #off-topic`
`..watchword "lorem ipsum"`
`..watchword lorem`

`deleteword "word"` - Deletes the specified word/phrase from your watch list.

`..deleteword "lorem ipsum"`
`..deleteword lorem`

`watchclear` - Clears all watched words/phrases that you are watching.

`cd [minutes]` - Toggle how long before you want to be alerted again after the most recent alert. Set at 15 minutes by default.

`..cd`
`..cd 3`

`worddetail "word"` - Tells you the filtered channels enabled for the word/phrase and time the word/phrase was last seen.

`..worddetail "lorem ipsum"`
`..worddetail lorem`

`addfilter "word" [channels]` - Start watching for word/phrase in specified channels. Will not replace previously watching channels.

`..addfilter lorem #general #games`

`deletefilter "word" [channels]` - Stop watching for word/phrase in specified channels.

`..deletefilter "lorem ipsum" #off-topic #general`

`clearfilter "word"` - Remove all filters from word/phrase; watch entire server instead.

`..clearfilter "lorem ipsum"`
`..clearfilter lorem`

`forcesave` - Force saves all current data into the JSON files. Admin only!

`botstop` - Saves data and logs out bot. Admin only!