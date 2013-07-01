from .window import Window
from . import lyre

class RootWindow(Window):
  def __init__(self, *args, **kwargs):
    super(RootWindow, self).__init__(*args, **kwargs)

    self.channel_menu = ChannelWindow(self.subwin(1, self.width, 0, 0))

  def draw(self):
    self.channel_menu.repaint()

class ChannelWindow(Window):

  def draw(self):
    for ch in lyre.client.channels:
      self.addstr(" " + ch.name + " ")
