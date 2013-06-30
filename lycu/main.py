import curses
from gutter.dispatch import receiver
from gutter.channel import post_sync, pre_sync

from . import lyre

@receiver(post_sync)
def hello(signal, sender, **kwargs):
  print "Hello!"

def main(stdscr):
  from gutter.client import RainwaveClient
  ch = client.channels[0]
  ch.start_sync()
#  stdscr.addstr("Hello, world! ")
#  stdscr.addstr("FOO")
#  stdscr.refresh()
  input()

if __name__ == "__main__":
  #curses.wrapper(main)
  print lyre.client.user_id, lyre.client.key
