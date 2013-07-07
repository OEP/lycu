import shlex
from . import lyre

COMMANDS = {
  "channel": {
    "next": "next_channel",
    "previous": "previous_channel",
  }
}

class CommandError(Exception):
  pass

def find_command(cmdparts, context, d):
  if not cmdparts:
    raise CommandError("Expected command or subcommand. Try: {}".format(
      ", ".join(d.keys())))
  cmd = cmdparts[0]
  if not cmd:
    raise CommandError("Empty command given.")
  keys = [key for key in d.keys() if key.startswith(cmd)]
  if not keys:
    raise CommandError("No such command: '{}'".format(cmd))
  if len(keys) > 1:
    raise CommandError("Ambiguous prefix '{}'. Try: {}".format(
      cmd, ", ".join(keys)))
  key = keys[0]
  value = d[key]
  if isinstance(value, dict):
    return find_command(cmdparts[1:], context, value)
  fn = eval(value)
  return fn(context)

def execute(command, context):
  parts = shlex.split(command)
  if not parts:
    raise CommandError("No command specified.")
  return find_command(parts, context, COMMANDS) 

def next_channel(context):
  return change_channel(context, 1)

def previous_channel(context):
  return change_channel(context, -1)

def change_channel(context, direction=1):
  ch = [ch for ch in lyre.client.channels if ch.id == context.current_channel]
  ch = ch[0]
  idx = lyre.client.channels.index(ch)
  if 0 < idx + direction < len(lyre.client.channels):
    context.current_channel = lyre.client.channels[idx + direction].id
    return
  raise CommandError("No more channels.")
