import curses
from gutter.dispatch import receiver
from gutter.channel import post_sync, pre_sync

from . import lyre
from .window import Window

root = None

@receiver(post_sync)
def on_sync(signal, sender, raw_timeline={}):
  d = raw_timeline['sched_current']
  d = d['song_data']
  d = d[0]
  song_title = d['song_title']
  album_name = d['album_name']
  label = "%s - %s" % (song_title, album_name)
  y, x = sender.id, 0
  line = "%s:\t%s" % (sender.name, label)

  root.move(y, x)
  root.clrtoeol()
  root.addstr(sender.id, 0, line)
  root.refresh()

def main(stdscr):
  global root
  root = Window(stdscr)

  for ch in lyre.client.channels:
    ch.start_sync()

  input()

if __name__ == "__main__":
  curses.wrapper(main)
