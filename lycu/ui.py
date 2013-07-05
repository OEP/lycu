from collections import namedtuple

from .window import Window
from . import lyre

class RootWindow(Window):
  def __init__(self, win):
    super(RootWindow, self).__init__(win)
    self.channel_menu = ChannelWindow(self.subwin(1, self.width, 0, 0))
    self.channel_detail = ChannelDetail(
      self.subwin(self.height-1, self.width, 1, 0))

  def draw(self, context):
    self.channel_menu.repaint(context)
    self.channel_detail.repaint(context)

class ChannelWindow(Window):
  
  def draw(self, context):
    self.move(0, 0)
    self.clrtoeol()
    for ch in lyre.client.channels:
      pad = " "
      if context.current_channel == ch.id:
        pad = "+"
      self.addstr(pad + ch.name + pad)

class ChannelDetail(Window):
  def __init__(self, win):
    super(ChannelDetail, self).__init__(win)
    self.current_election = ElectionWindow(self.subwin(self.height, 20, 1, 0))

  def draw(self, context):
    channel = [ch
      for ch in lyre.client.channels 
      if ch.id == context.current_channel]
    channel = channel[0]

    self.current_election.election = channel.schedule_current
    self.current_election.repaint(context)

class ElectionWindow(Window):
  def __init__(self, win):
    super(ElectionWindow, self).__init__(win)
    self.election = None

  def draw(self, context):
    y, x = self.getbegyx()
    if not self.election:
      return
    for song in self.election.songs:
      self.move(y, 0)
      self.addstr(str(song.title))
      y += 1
