
description_str = "Do `{prefix}help` to open this. Bot Prefix: `{prefix}`"

watched_str = "Gives user list of all watched words/phrases on the server"

watchword_str = """Start watching a word and be alerted according to your `cd` setting. Optional channel filter.\n`{prefix}watchword "lorem ipsum" #general #off-topic`\n`{prefix}watchword lorem`"""

deleteword_str = """Delete a word or phrase. Phrases must be wrapped in quotes.\n`{prefix}deleteword lorem`\n`{prefix}deleteword "lorem ipsum"`"""

watchclear_str = """Clears all watched words/phrases that you are watching."""

cd_str = """Toggle how long before you want to be alerted again after the most recent alert. 15 minutes by default.\n`{prefix}cd`\n`{prefix}cd 3`"""

worddetail_str = """Gives you details of a watched word/phrase.\n`{prefix}worddetail lorem`\n`{prefix}worddetail "lorem ipsum"`"""

addfilter_str = """Watch for word/phrase in channels separated by spaces.\n`{prefix}addfilter lorem #general #games`"""

deletefilter_str = """Stop watching for word/phrase in channels separated by spaces.\n`{prefix}deletefilter "lorem ipsum" #off-topic #general`"""

clearfilter_str = """Remove all filters from word/phrase; watch entire server instead.\n`{prefix}clearfilter lorem`"""

footer_str = """Phrases must be wrapped in quotes but single words don't. Commands will not work outside servers."""
