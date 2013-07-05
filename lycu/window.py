import threading

class Window(object):

  def __init__(self, win):
    self.win = win
    self.lock = threading.Lock()

  @property
  def size(self):
    return self.win.getmaxyx()

  @property
  def origin(self):
    return self.win.getbegyx()

  @property
  def width(self):
    return self.size[1]

  @property
  def height(self):
    return self.size[0]

  @property
  def cursor(self):
    return self.win.getyx()

  def add_line(self, s):
    self.win.addnstr(s.encode('ascii', 'ignore'), self.width)
    if len(s) < self.width:
      self.next_line()

  def reset_cursor(self):
    y, x = self.origin
    self.win.move(y, x)

  def next_line(self, dy=1):
    y, x = self.cursor
    y += dy
    self.win.move(y, 0)

  def repaint(self, context):
    self.lock.acquire()
    self.win.clear()
    self.draw(context)
    self.refresh()
    self.lock.release()

  def draw(self, context=None):
    pass 

  def __getattr__(self, name):
    return getattr(self.win, name)
