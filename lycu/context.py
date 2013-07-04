DEFAULT_CONTEXT = {
  "current_channel": None,
}

class Context(object):
  @classmethod
  def get_default(cls):
    return cls(**DEFAULT_CONTEXT)

  def __init__(self, **kwargs):
    for key, value in kwargs.items():
      setattr(self, key, value)
