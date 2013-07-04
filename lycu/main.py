import curses
from collections import namedtuple
from gutter.dispatch import receiver
from gutter.channel import post_sync, pre_sync

from . import lyre
from .ui import RootWindow
from .context import Context

root = None
context = Context.get_default()

@receiver(post_sync)
def on_sync(signal, sender, **kwargs):
  root.repaint(context)

def main(stdscr):
  global root
  root = RootWindow(stdscr)
  context.current_channel = lyre.client.channels[0].id

  for ch in lyre.client.channels:
    ch.start_sync()

  raw_input()

if __name__ == "__main__":
  curses.wrapper(main)
