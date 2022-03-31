'''
  Handles what to do everytime the bot ticks and new events are generated.
  Author: reoky : 03 30 22
'''
from sqlalchemy import update
from sqlalchemy.future import select

from config import *
from command import find_or_create_guild
from command import set_last_spoken
from compute import locate_boat
from store import *

async def handle_tick(bot, async_session):
  guilds = None
  async with async_session() as session:
    async with session.begin():
      result = await session.execute(select(Guild))
      guilds = result.scalars().all()
  
    for guild in guilds:

      await handle_guild_tick(async_session, bot, guild)

#
# Handles conveying updates to exactly one guild.
#
async def handle_guild_tick(async_session, bot, guild):
  status = locate_boat(guild)

  # Guard: There is a status and not nothing
  if (status == None):
    return

  # Guard: The starting time is set and not 0. (or worse, negative)
  if (guild.starting <= 0):
    return

  # Guard: The guild status updates are active
  if (guild.active != True):
    return
  
  # Handle status updates
  if (guild.lastspoken != status["location"]):

    # Mark this status as spoken so we don't speak it over and over
    await set_last_spoken(async_session, guild, status["location"])

    # Guard: The target wants to get status updates.
    if (guild.notify != NOTIFY_LEVEL_FULL and guild.notify != NOTIFY_LEVEL_DOCKED):
      return

    # It's either a channel or a user that interacted with the bot
    msg_target = None
    try:
      if (guild.isuser):
        msg_target = await bot.fetch_user(guild.id)
        await handle_broadcast_message(bot, msg_target, guild, status)
      else:
        msg_target = await bot.fetch_channel(guild.id)
        await handle_broadcast_message(bot, msg_target, guild, status)
    except Exception as e:
      print("[Reborn Cargo@handle_guild_tick] - %s" % e)

#
# Sends those boat status messages to everyone's channels.
#
async def handle_broadcast_message(bot, msg_target, guild, status):
  try:
    if (status['location'] == LOCATION_TC):
      await msg_target.send(STR_ARRIVED_TC)
    elif(status['location'] == LOCATION_TC_SOLIS):
      if (guild.notify == NOTIFY_LEVEL_DOCKED):
        return
      await msg_target.send(STR_DEPART_SOLIS)
    elif(status['location'] == LOCATION_SOLIS):
      await msg_target.send(STR_ARRIVED_SOLIS)
    elif(status['location'] == LOCATION_SOLIS_TC):
      if (guild.notify == NOTIFY_LEVEL_DOCKED):
        return
      await msg_target.send(STR_DEPART_TC)
  except Exception as e:
    print("[Reborn Cargo@handle_broadcast_message] - %s" % e)

