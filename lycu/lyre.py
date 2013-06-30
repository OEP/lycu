import os

from gutter.client import RainwaveClient
from lycu.conf import settings

client = RainwaveClient(
  user_id = int(settings.user_id),
  key = settings.key
)
