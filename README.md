# reborn-cargo
An ArcheAge Discord bot for &lt;Reborn> guild in AAU.

## Description
I wanted to do something fun that would also have educational value for those learning Python and about the asynchronous version of SQLAlchemy. This Discord bot is designed to support multiple Discord servers simultaneously. In order to accomplish this, it leverages a SQLite database to persist state changes for every Discord server. This basically means that everyone using a bot instance can set their own cargo timers.

## Commands
For example: /cargo [solis|tc] 12:43 (for 12 minutes and 43 seconds) Don't forget to `/cargo start ` to activate tracking. Starting also picks up from the last `/cargo stop`.

Set the postion of the boat: `/cargo set [solis|tc] 12:43`
Start tracking the boat: `/cargo start`
Stop sending tracking: `/cargo stop`
Version information type: `/cargo version`
Add happiness: `/cargo happy`
Remove happiness: `/cargo sad`
Notification settings: `/cargo notify [full|docked|silent]`

## Installing / Using
Pull the code down, install Python and `pip install pipenv`. Then go inside the bot directory and type `pipenv install` to pull the bot's dependencies. You can run the code by installing your Discord API on the last line of bot.py and start it with `pipenv run python bot.py`. The code runs inside a virtualenv managed by pipenv.

You'll need to have a Discord application and API key: https://discord.com/developers/applications

Thanks friends ~
