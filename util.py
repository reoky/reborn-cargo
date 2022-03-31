from config import *

#
# We really don't want to mix up people's server states.
#
def get_unique_id(ctx):
  if (ctx.guild != None):
    return {
      'id': ctx.channel.id,
      'name': ctx.guild.name,
      'isuser': False
    }
  else:
    return {
      'id': ctx.author.id,
      'name': ctx.author.name + "#" + ctx.author.discriminator,
      'isuser': True
    }

#
# Simply returns the location_id given a location string. [tc|solis]
#
def get_location_id(location):
  loc = location.lower()
  if (loc == 'tc'):
    return LOCATION_TC
  elif (loc == 'solis'):
    return LOCATION_SOLIS
  return -1 # nope

#
# Gets the notifcation level from a string
#
def get_notify_id(level):
  lvl = level.lower()
  if (lvl == 'full'):
    return NOTIFY_LEVEL_FULL
  elif (lvl == 'docked'):
    return NOTIFY_LEVEL_DOCKED
  elif (lvl == 'silent'):
    return NOTIFY_LEVEL_SILENT
  return -1 # nope

#
# Messages the bot's current happiness level to Discord.
#
async def state_our_happiness(ctx, feelings):
  if (feelings == -5):
    await ctx.send(STR_SAD_5)
  elif (feelings == -4):
    await ctx.send(STR_SAD_4)
  elif (feelings == -3):
    await ctx.send(STR_SAD_3)
  elif (feelings == -2):
    await ctx.send(STR_SAD_2)
  elif (feelings == -1):
    await ctx.send(STR_SAD_1)
  elif (feelings == 1):
    await ctx.send(STR_HAPPY_1)
  elif (feelings == 2):
    await ctx.send(STR_HAPPY_2)
  elif (feelings == 3):
    await ctx.send(STR_HAPPY_3)
  elif (feelings == 4):
    await ctx.send(STR_HAPPY_4)
  elif (feelings == 5):
    await ctx.send(STR_HAPPY_5)
  else:
    return
