'''
  ## ## ## ## ## ## ## ## ##
  ### ArcheAge Cargo Bot ###
  ## ## ## ## ## ## ## ## ##

  Author: reoky
  Date: 3/30/2022

  Cargo bot that offers Discord users the ability to subscribe to notifications
  about the current status of the cargo ship for their family quests. ~
'''
# Standard Library
import asyncio
import discord

# Third-party
import discord
from discord.ext import commands, tasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Project
from config import *
from compute import *
from store import *
from command import *
from tick import handle_tick

bot = commands.Bot(command_prefix = '/')
sql_engine = create_async_engine("sqlite+aiosqlite:///reborn-cargo.db", echo=False, future=True)
async_session = sessionmaker(
  sql_engine,
  expire_on_commit=False,
  autocommit=False,
  autoflush=True,
  class_=AsyncSession
)

@bot.event
async def on_ready():

  # Create the database and start the Discord event looper
  async with sql_engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
    cargo_tick.start()
  
  # Set the bot status to playing ArcheAge
  await bot.change_presence(activity=discord.Game(name="ArcheAge Unchained"))
  print('~ ~ ~ Online ~ ~ ~')

@bot.command()
async def cargo(ctx, *args):

  # Guard: Too many or too few arguments
  if (len(args) < 1 or len(args) > 3):
    await ctx.send(STR_USAGE)
    return

  cmd = (args[0])

  # Start Command
  if (cmd == "start"):
    await set_active(ctx, async_session, True)
    await ctx.send(STR_STARTING)
    return

  # Stop Command
  if (cmd == "stop"):
    await set_active(ctx, async_session, False)
    await ctx.send(STR_SHUTDOWN)
    return

  # Configure the boat for the user's channel
  if (cmd == "set"):
    if (len(args) == 3):
      await set_timer(ctx, async_session, args[1], args[2])
    else:
      await ctx.send(STR_USAGE)
    return

  # Tell where the boat currently is
  if (cmd == "where"):
    await get_boat_status(ctx, async_session)
    return

  # Toggle Notifcations
  if (cmd == "notify"):
    await set_notify(ctx, async_session, args[1])
    return

  # Add Happiness
  if (cmd == "happy"):
    await set_happiness(ctx, async_session, 1)
    return

  # Remove Happiness
  if (cmd == "sad"):
    await set_happiness(ctx, async_session, -1)
    return

  # Version Command
  if (cmd == "version"):
    await ctx.send(STR_VERSION)
    return

  # Default Action
  await ctx.send(STR_USAGE)

# The main event loop
@tasks.loop(seconds=3)
async def cargo_tick():
  await handle_tick(bot, async_session)

# # Bot Run : Secret Token
bot.run('<Your Token Here>')
