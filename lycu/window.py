

class Window(object):
  
  def __init__(self, win):
    self.win = win

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

  def repaint(self):
    self.draw()
    self.refresh()

  def draw(self):
    pass 

  def __getattr__(self, name):
    return getattr(self.win, name)
