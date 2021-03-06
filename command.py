'''
  Handles individual commands generated by user input and responds to the user with something useful.
  Author: reoky : 03 30 22
'''
import time

from sqlalchemy import update
from sqlalchemy.future import select

from store import Guild
from config import *
from compute import compute_cycle_offset
from compute import locate_boat
from util import get_location_id
from util import get_notify_id
from util import get_unique_id
from util import state_our_happiness

#
# Find or create guild record to associate state with.
#
async def find_or_create_guild(ctx, async_session):
  identity = get_unique_id(ctx)
  async with async_session() as session:
    async with session.begin():
      result = await session.execute(select(Guild).where(Guild.id == identity['id']))
      guild = result.scalars().first()
      if (guild != None):
        return guild
      else:
        guild = Guild(
          id = identity['id'],
          name = identity['name'],
          isuser = identity['isuser']
        )
      session.add(guild)
    return guild

#
# Find the boat and time remaining until the next stage.
#
async def get_boat_status(ctx, async_session):
  guild = await find_or_create_guild(ctx, async_session)
  status = locate_boat(guild)

  # Guard: The starting time is set and not 0. (or worse, negative)
  if (guild.starting <= 0):
    await ctx.send(STR_NOT_READY)
    return

  try:
    if (status['location'] == LOCATION_TC):
      msg = "%s %s minutes." % (STR_DOCKED_TC, int((DOCK_TIME_MS - (status['ratio'] * DOCK_TIME_MS)) / 60000))
      await ctx.send(msg)
    elif(status['location'] == LOCATION_TC_SOLIS):
      msg = "%s %s percent of the way there." % (STR_TRANSIT_SOLIS, int(status['ratio'] * 100))
      await ctx.send(msg)
    elif(status['location'] == LOCATION_SOLIS):
      msg = "%s %s minutes." % (STR_DOCKED_SOLIS, int((DOCK_TIME_MS - (status['ratio'] * DOCK_TIME_MS)) / 60000))
      await ctx.send(msg)
    elif(status['location'] == LOCATION_SOLIS_TC):
      msg = "%s %s percent of the way there." % (STR_TRANSIT_TC, int(status['ratio'] * 100))
      await ctx.send(msg)
  except Exception as e:
    print("[Reborn Cargo@get_boat_status] - %s" % e)

#
# Sets the user's bot instance to active or inactive.
#
async def set_active(ctx, async_session, is_active):
  guild = await find_or_create_guild(ctx, async_session)
  async with async_session() as session:
    async with session.begin():
      stmt = update(Guild).where(Guild.id == guild.id).values(
        active = 1 if is_active else 0
      )
      await session.execute(stmt)

#
# Sets a value for the last spoken location by the bot. This is so it doesn't keep speaking
# the same boat stage over and over again. We actually look in the database to see if it
# already did.
#
async def set_last_spoken(async_session, guild, last_spoken):
  async with async_session() as session:
    async with session.begin():
      stmt = update(Guild).where(Guild.id == guild.id).values(
        lastspoken = last_spoken
      )
      await session.execute(stmt)

#
# Sets the notification level.
# 
async def set_notify(ctx, async_session, level):
  guild = await find_or_create_guild(ctx, async_session)

  # Guard: Notify level an actual lvl and not nonesense.
  lvl = get_notify_id(level)
  if (lvl < 0):
    return await ctx.send(STR_USAGE)

  async with async_session() as session:
    async with session.begin():
      stmt = update(Guild).where(Guild.id == guild.id).values(notify = lvl)
      await session.execute(stmt)

  if (lvl == NOTIFY_LEVEL_FULL):
    await ctx.send(STR_NOTIFY_FULL)
  elif (lvl == NOTIFY_LEVEL_DOCKED):
    await ctx.send(STR_NOTIFY_DOCKED)
  elif (lvl == NOTIFY_LEVEL_SILENT):
    await ctx.send(STR_NOTIFY_SILENT)

#
# Sets the notification level.
# 
async def set_happiness(ctx, async_session, offset):
  guild = await find_or_create_guild(ctx, async_session)

  # local feelings
  feels = guild.happiness

  # Guard: Notify level an actual lvl and not nonesense. -5 to 5 non-inclusive.
  if (feels <= -5 or feels >= 5):
    feels = 1 if offset >= 0 else -1 # reset it in the postive or negative inclination
  else:
    feels += offset # increment / decrement it
  
  # Guard: Feels is still zero because it wasn't outside the range of the previous guard.
  if (feels == 0):
    feels = 1 if offset >= 0 else -1

  # Update happiness to reflect
  async with async_session() as session:
    async with session.begin():
      stmt = update(Guild).where(Guild.id == guild.id).values(happiness = feels)
      await session.execute(stmt)
  
  # State our new happiness level ~
  await state_our_happiness(ctx, feels)

#
# Configures the boat timer for a specific guild's (or user's bot instance)
#
async def set_timer(ctx, async_session, location, timer):
  guild = await find_or_create_guild(ctx, async_session)

  # Guard: Get and validate location
  location_id = get_location_id(location)
  if (location_id < 0):
    return await ctx.send(STR_USAGE)
  
  # Get and validate the boat timer
  offset_ms = compute_cycle_offset(location_id, timer)
  if (offset_ms < 0):
    return await ctx.send(STR_USAGE)

  async with async_session() as session:
    async with session.begin():
      stmt = update(Guild).where(Guild.id == guild.id).values(
        starting = int(time.time() * 1000),
        offset = offset_ms,
        lastspoken = location_id
      )
      await session.execute(stmt)
  await ctx.send(STR_SET)
