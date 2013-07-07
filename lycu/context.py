from gutter.dispatch import Signal

DEFAULT_CONTEXT = {
  "current_channel": None,
}

context_changed = Signal()

class Context(object):
  _data = {}

  @classmethod
  def get_default(cls):
    return cls(**DEFAULT_CONTEXT)

  def __init__(self, **kwargs):
    for key, val in kwargs.items():
      self._data[key] = val

  def __getattr__(self, name):
    try:
      return self._data[name]
    except KeyError:
      raise AttributeError(name)

  def __setattr__(self, name, value):
    if name in self._data:
      old_value = self._data[name]
      if old_value != value:
        self._data[name] = value
        context_changed.send(self)
    else:
      raise AttributeError(name)
