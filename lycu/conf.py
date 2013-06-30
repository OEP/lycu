import os

DEFAULT_SETTINGS = {
  'user_id': '0',
  'key': '',
}

RCFILES = (
  os.path.join(os.environ.get('HOME'), '.lycurc')
)

class Settings(object):
  
  @classmethod
  def load_rcfile(cls, path):
    pass

  def __init__(self, data={}):
    self._data = dict(data)
   
  def __getattr__(self, name):
    try:
      return self._data[name]
    except KeyError as e:
      raise AttributeError("No such attribute: %s" % name)

  def update(self, d):
    self._data.update(d)

  def update_from_rcfile(self, path):
    d = {}
    with open(path) as fp:
      for line in fp:
        lhs, rhs = (x.strip() for x in line.split("="))
        d[lhs] = rhs
    self.update(d)

settings = Settings(DEFAULT_SETTINGS)

for rcfile in RCFILES:
  try:
    settings.update_from_rcfile(rcfile)
  except IOError:
    pass
