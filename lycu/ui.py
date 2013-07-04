from collections import namedtuple

from .window import Window
from . import lyre

class RootWindow(Window):
  def __init__(self, win):
    super(RootWindow, self).__init__(win)
    self.channel_menu = ChannelWindow(self.subwin(1, self.width, 0, 0), self)

  def draw(self, context):
    self.channel_menu.repaint(context)

class ChannelWindow(Window):
  def __init__(self, win, parent):
    super(ChannelWindow, self).__init__(win)
    self.parent = parent

  def draw(self, context):
    self.move(0, 0)
    self.clrtoeol()
    for ch in lyre.client.channels:
      pad = " "
      if context.current_channel == ch.id:
        pad = "+"
      self.addstr(pad + ch.name + pad)
