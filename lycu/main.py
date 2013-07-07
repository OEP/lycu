import curses
import sys
from gutter.dispatch import receiver
from gutter.channel import post_sync, pre_sync

from . import lyre, ui
from .ui import RootWindow
from .context import Context

root = None
context = Context.get_default()

@receiver(post_sync)
def on_sync(signal, sender, **kwargs):
  try:
    root.repaint(context)
  except Exception as e:
    with open('lycu.log', 'w') as fp:
      import traceback
      traceback.print_exc(None, fp)

def main(stdscr):
  global root
  ui.init_pairs()
  root = RootWindow(stdscr)
  context.current_channel = lyre.client.channels[0].id

  for ch in lyre.client.channels:
    ch.start_sync()

  while True:
    c = root.win.getch()
    root.dispatch_key(context, c)


if __name__ == "__main__":
  curses.wrapper(main)
