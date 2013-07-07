import curses
from collections import namedtuple

from .window import Window
from . import lyre, commands
from .util import fixed_width_suffix

PAIR_NORMAL = 0
PAIR_ERROR = 1

COLOR_PAIRS = (
  (PAIR_ERROR, curses.COLOR_WHITE, curses.COLOR_RED),
)

def init_pairs():
  for code, fgc, bgc in COLOR_PAIRS:
    curses.init_pair(code, fgc, bgc)

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
    self.children['election'] = ElectionWindow(
      self.subwin(self.height, 30, 1, 0))

  def draw(self, context):
    channel = [ch
      for ch in lyre.client.channels 
      if ch.id == context.current_channel]
    channel = channel[0]

    sched = channel.schedule_next[0]
    self.children['election'].election = sched

class CommandWindow(Window):
  def __init__(self, win):
    super(CommandWindow, self).__init__(win)
    self.buffer = ""
    self.error = ""

  @property
  def active(self):
    return len(self.buffer) and self.buffer[0] == ":"

  @property
  def has_error(self):
    return len(self.error) > 0

  def on_key(self, context, key):
    #self.buffer = str(key)
    #return True
    if self.active and key == 10: ## ENTER
      try:
        cmd = self.buffer[1:]
        self.buffer = ""
        commands.execute(cmd, context)
      except commands.CommandError as e:
        self.error = e.message
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
      self.error = ""
      self.buffer = chr(key)
      return True
    return False

  def draw(self, context):
    self.reset_cursor()
    if self.active:
      self.add_line(self.buffer, curses.color_pair(PAIR_NORMAL))
    elif self.has_error:
      self.add_line(self.error, curses.color_pair(PAIR_ERROR))

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
