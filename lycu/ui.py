import curses
from collections import namedtuple

from .window import Window
from . import lyre
from .util import fixed_width_suffix

class RootWindow(Window):
  def __init__(self, win):
    super(RootWindow, self).__init__(win)

    self.children['channels'] = ChannelWindow(self.subwin(1, self.width, 0, 0))
    self.children['detail'] = ChannelDetail(
      self.subwin(self.height-2, self.width, 1, 0))
    self.children['command'] = CommandWindow(self.subwin(1, self.width,
      self.height-1, 0))

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

  def draw(self, context):
    channel = [ch
      for ch in lyre.client.channels 
      if ch.id == context.current_channel]
    channel = channel[0]

    self.children = {}
    y = 1
    height = int(self.height / len(channel.schedule_next))
    for i, sched in enumerate(channel.schedule_next):
      name = 'next{}'.format(i)
      w = ElectionWindow(self.subwin(height, 30, y, 0))
      w.election = sched
      self.children[name] = w
      w.repaint(context)
      y += 30

class CommandWindow(Window):
  def __init__(self, win):
    super(CommandWindow, self).__init__(win)
    self.buffer = ""
    self.target = 0

  @property
  def active(self):
    return len(self.buffer) and self.buffer[0] == ":"

  def on_key(self, context, key):
    #self.buffer = str(key)
    #return True
    if self.active and key == 10: ## ENTER
      self.buffer = ""
      ## TODO: Execute command
      return True
    elif self.active and key == 27: ## ESC
      self.buffer = ""
      return True
    elif self.active and key < 256:
      self.buffer += chr(key)
      return True
    elif self.active and key == curses.KEY_BACKSPACE:
      self.buffer = self.buffer[:-1]
      return True
    elif key == ord(":"):
      self.buffer = chr(key)
      return True
    return False

  def draw(self, context):
    self.reset_cursor()
    self.add_line(self.buffer)


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
