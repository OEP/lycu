import threading

class Window(object):

  def __init__(self, win):
    self.win = win
    self.lock = threading.Lock()
    self.children = {}

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

  def add_line(self, s, *attr):
    n = self.width - self.cursor[1]
    self.win.addnstr(s.encode('ascii', 'ignore'), n, *attr)
    if len(s) < n and self.cursor[0] < self.height-1:
      self.next_line()

  def add_child(self, window):
    self._children.add(window)

  def reset_cursor(self):
    self.win.move(0, 0)

  def next_line(self, dy=1):
    y, x = self.cursor
    y += dy
    self.win.move(y, 0)

  def repaint(self, context):
    self.lock.acquire()
    self.win.clear()
    self.draw(context)
    self.refresh()
    for child in self.children.values():
      child.repaint(context)
    self.lock.release()

  def dispatch_key(self, context, key):
    if self.on_key(context, key):
      return True

    for child in self.children.values():
      if child.dispatch_key(context, key):
        child.repaint(context)
        return True
    return False

  def on_key(self, context, key):
    return False

  def draw(self, context=None):
    pass 

  def __getattr__(self, name):
    return getattr(self.win, name)
