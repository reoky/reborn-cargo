import time
import math
from config import *

'''
  Anything mathy such as determining where the boat currently is that could pollute the readability of the rest of the bot code.
  Author: reoky : 03 30 22
'''
# Returns the current stage and position of the boat given the starting time.
def locate_boat(guild):

  # Substract already completed cycles to determine the time into the current cycle.
  current_ms = int(time.time() * 1000)
  elapsed_ms = current_ms - guild.starting
  completed_cyles = math.floor(elapsed_ms / COMPLETE_CYCLE_TIME_MS)
  cycle_time_ms = elapsed_ms - (completed_cyles * COMPLETE_CYCLE_TIME_MS) + guild.offset

  # The time thresholds for each stage.
  primary_docked_threshold = DOCK_TIME_MS
  primary_transit_threshold = primary_docked_threshold + TC_TO_SOLIS_TIME_MS
  secondary_docked_threshold = primary_transit_threshold + DOCK_TIME_MS
  secondary_transit_threshold = secondary_docked_threshold + SOLIS_TO_TC_TIME_MS

  # Return a status dict for the correct stage
  if (cycle_time_ms < primary_docked_threshold):
    return {
      'location': LOCATION_TC,
      'ratio': cycle_time_ms / DOCK_TIME_MS
    }
  elif (cycle_time_ms < primary_transit_threshold):
    return {
      'location': LOCATION_TC_SOLIS,
      'ratio': (cycle_time_ms - primary_docked_threshold) / (primary_transit_threshold - primary_docked_threshold)
    }
  elif (cycle_time_ms < secondary_docked_threshold):
    return {
      'location': LOCATION_SOLIS,
      'ratio': (cycle_time_ms - primary_transit_threshold) / (secondary_docked_threshold - primary_transit_threshold)
    }
  elif (cycle_time_ms < secondary_transit_threshold):
    return {
      'location': LOCATION_SOLIS_TC,
      'ratio': (cycle_time_ms - secondary_docked_threshold) / (secondary_transit_threshold - secondary_docked_threshold)
    }

#
# Determines the amount of time_ms into one cycle the boat has gone based on it's starting time docked at TC (T0).
# This function returns the number of time_ms that have occured since T0 and adds the appropriate time
# if the boat actually started in solis. Ie. The TC dock time + the TC->Solis transit time.
#
def compute_cycle_offset(location_id, timer):
  boat_timer_ms = compute_timer_ms(timer)

  # Guard: Negative boat timer.
  if (boat_timer_ms < 0):
    return -1 # fail

  # Guard: Boat timer larger that max docked time.
  if (boat_timer_ms > DOCK_TIME_MS):
    return -1 # fail

  if (location_id == LOCATION_TC):
    return DOCK_TIME_MS - boat_timer_ms
  elif (location_id == LOCATION_SOLIS):
    return (DOCK_TIME_MS - boat_timer_ms) + DOCK_TIME_MS + TC_TO_SOLIS_TIME_MS
  
  # Bad location
  return -1

#
# Splits a boat timer, such as "12:43" into minutes and seconds and returns the total time_ms.
#
def compute_timer_ms(timer):
  try:
    time_components = timer.split(":")
    return (int(time_components[0]) * 60000) + (int(time_components[1]) * 1000)
  except:
    return -1 # fail
