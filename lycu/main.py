import curses
from gutter.dispatch import receiver
from gutter.channel import post_sync, pre_sync

from . import lyre

root = None

@receiver(post_sync)
def hello(signal, sender, raw_timeline={}):
  d = raw_timeline['sched_current']
  d = d['song_data']
  d = d[0]
  d = d['song_title']
  print sender, d

def main(stdscr):
  global root
  root = stdscr 

  for ch in lyre.client.channels:
    ch.start_sync()

  input()

if __name__ == "__main__":
  #curses.wrapper(main)
  main(3)
