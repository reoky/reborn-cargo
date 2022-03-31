'''
  The cargo bot keeps basic state information pertaining to each channel in a SQL database. This way if the bot has to be restarted
  it won't forget where the boat was.
  Author: reoky : 03 30 22
'''
import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Sequence
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from config import DEFAULT_NOTIFY_LEVEL

Base = declarative_base()

# List of people who wanted to be DM'd notifications. (Disabled because of Discord 50 message rate limit.)
class Subscriber(Base):
  __tablename__ = 'subscribers'
  sid     = Column(Integer, Sequence('sid_seq'), primary_key=True, nullable=False)
  handle  = Column(String(64), nullable=False)
  created = Column(Integer, nullable=False, default=datetime.datetime.utcnow)

  def to_dict(self):
    return {
      'sid': self.sid,
      'handle': self.handle,
      'created': self.created
    }

# Channels or people who have used the bot.
class Guild(Base):
  __tablename__ = 'guilds'
  id          = Column(String, primary_key=True, nullable=False)
  isuser     = Column(Boolean, nullable=False, default=False)
  name        = Column(String, nullable=False)
  active      = Column(Boolean, nullable=False, default=False)
  starting    = Column(Integer, nullable=False, default=0)
  offset      = Column(Integer, nullable=False, default=0)
  lastspoken  = Column(Integer, nullable=False, default=-1)
  happiness   = Column(Integer, nullable=False, default=0)
  notify      = Column(Integer, nullable=False, default=DEFAULT_NOTIFY_LEVEL)

  def to_dict(self):
    return {
      'id': self.id,
      'isuser': self.isuser,
      'name': self.name,
      'active': self.active,
      'starting': self.started,
      'offset': self.offset,
      'lastspoken': self.lastspoken,
      'happiness': self.happiness,
      'notify': self.notify
    }
