'''
  This is the global configuration for the bot. If you want to tweak the bot without making major edits to
  the code then this is the place to do that.
  Author: reoky : 03 30 22
'''
###############
### Globals ###
###############
APP_DEBUG = False
APP_VERSION = 143
DOCK_TIME_MS = 1200000 # 1,200 seconds (20 minutes)
SOLIS_TO_TC_TIME_MS = 620950 # 620.95 seconds prod
TC_TO_SOLIS_TIME_MS = 647950 # 647.95 seconds prod
COMPLETE_CYCLE_TIME_MS = (DOCK_TIME_MS * 2) + SOLIS_TO_TC_TIME_MS + TC_TO_SOLIS_TIME_MS
DEFAULT_NOTIFY_LEVEL = 2
NOTIFY_LEVEL_FULL = 2
NOTIFY_LEVEL_DOCKED = 1
NOTIFY_LEVEL_SILENT = 0
LOCATION_TC = 0
LOCATION_TC_SOLIS = 1
LOCATION_SOLIS = 2
LOCATION_SOLIS_TC = 3

# Writes a human-readable time.
def time_str(ms, unit):
  if (unit == "seconds"):
    return "%s %s" % (ms / 1000, unit)
  elif (unit == "minutes"):
    return "%s %s" % (ms / 60000, unit)
  return "%s %s" % (ms, unit)

###############
### STRINGS ###
###############
STR_UNIT = "seconds" if APP_DEBUG else "minutes"
STR_SOLIS = "Solis Headlands"
STR_TC = "Two Crowns"
STR_USAGE = '''\
Please tell me where the cargo boat is currently docked and the remaining time on the boat. I will post regular updates so that friends never miss the boat. ~

For example: /cargo [solis|tc] 12:43 (for 12 minutes and 43 seconds) Don't forget to `/cargo start ` to activate tracking. Starting also picks up from the last `/cargo stop`.

Set the postion of the boat: `/cargo set [solis|tc] 12:43`
Start tracking the boat: `/cargo start`
Stop sending tracking: `/cargo stop`
Version information type: `/cargo version`
Add happiness: `/cargo happy`
Remove happiness: `/cargo sad`
Notification settings: `/cargo notify [full|docked|silent]`

Note: Due to server maintenance and in-game variance friends will need to re-start and adjust me often.

Author: Reoky (Kraken Server) ~
'''
STR_RDY   = "I'm the bot and ready for commands. ~"
STR_SET   = "Good configuration. Now type /cargo start to begin tracking. ~"
STR_STARTING = "Okie! I will send cargo boat status updates to this channel for us. ~"
STR_SHUTDOWN = "Will I dream? *The bot nods in agreement that it will no longer send notifcations.*"
STR_NOTIFY_FULL = "Okie! Notifications have been set to their fullest. ~"
STR_NOTIFY_DOCKED = "Okie! I will only notify you when the boat docks. ~"
STR_NOTIFY_SILENT = "Okie! Not a peep unless you type `/cargo where` and I will tell you where the boat currently is. ~"
STR_NOT_READY = "Alrighty so you have to set the boat timer in this channel with `/cargo set [solis|tc] 12:43` before I can send you status updates.."
STR_SAD_1 = "Guys I was really hoping we could go on an ocean adventure, but nobody is getting on the boat. D:"
STR_SAD_2 = "They sure are making a lot of bots these days friends.. D:"
STR_SAD_3 = "Maybe they hate cargo bot. D:"
STR_SAD_4 = "Friends I don't know if I want to go anymore. We should all just uninstall the game instead. D:"
STR_SAD_5 = "* Cargo bot sails away never to be seen again. * :ocean:"
STR_HAPPY_1 = "Bring your friends! There's smooth sailing ahead of us. ~"
STR_HAPPY_2 = "OMG I love it when they play songs on the boat. ~"
STR_HAPPY_3 = "Guys is it normal if your body is shaking in excitement??"
STR_HAPPY_4 = "I'm so happy all the time!!"
STR_HAPPY_5 = "* The bot appears to have dissociated from reality due to happiness. * :rainbowcat:"
STR_VERSION = "I'm a version %s bot and every bit as friendly as the other versions. ^_^" % APP_VERSION

# Stage Messages
STR_DEPART_SOLIS = ":sailboat: Cargo Boat has departed for %s. :sailboat:" % STR_SOLIS
STR_DEPART_TC = ":sailboat: Cargo Boat has departed for %s. :sailboat:" % STR_TC
STR_ARRIVED_SOLIS = ":anchor: The cargo ship has arrived at %s and it leaves in %s. :anchor:" % (STR_SOLIS, time_str(DOCK_TIME_MS, STR_UNIT))
STR_ARRIVED_TC = ":anchor: The cargo ship has arrived at %s and it leaves in %s. :anchor:" % (STR_TC, time_str(DOCK_TIME_MS, STR_UNIT))

# Transit Messages
STR_TRANSIT_SOLIS = "The cargo ship is currently in transit to %s and it's" % STR_SOLIS
STR_TRANSIT_TC = "The cargo ship is currently in transit to %s and it's" % STR_TC
STR_DOCKED_TC = "The cargo ship is docked in %s and will leave in" % STR_TC
STR_DOCKED_SOLIS = "The cargo ship is docked in %s and will leave in" % STR_SOLIS
