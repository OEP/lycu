from collections import namedtuple

from .window import Window
from . import lyre
from .util import fixed_width_suffix

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
    self.next_elections = []

  def draw(self, context):
    channel = [ch
      for ch in lyre.client.channels 
      if ch.id == context.current_channel]
    channel = channel[0]

    self.next_elections = []
    y = 1
    height = int(self.height / len(channel.schedule_next))
    for sched in channel.schedule_next:
      w = ElectionWindow(self.subwin(height, 30, y, 0))
      w.election = sched
      self.next_elections.append(w)
      w.repaint(context)
      y += 30

class ElectionWindow(Window):
  def __init__(self, win):
    super(ElectionWindow, self).__init__(win)
    self.election = None

  def draw(self, context):
    if not self.election:
      return
    self.reset_cursor()
    for song in self.election.songs:
      rating = " {}:{}".format(song.rating or 'N/A', song.rating_avg)
      line = fixed_width_suffix(song.title, rating, self.width)
      self.add_line("{}".format(line))
      rating = " {}:{}".format(song.album.rating_user or 'N/A',
        song.album.rating_avg)
      line = fixed_width_suffix(song.album.name, rating, self.width)
      self.add_line("{}".format(line))
      self.add_line(", ".join([x.name for x in song.artists]))
      self.next_line()
