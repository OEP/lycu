import shlex
from . import lyre

COMMANDS = {
  "channel": {
    "next": "next_channel",
    "goto": "goto_channel",
    "previous": "previous_channel",
  },
  "help": "command_help",
}

class CommandError(Exception):
  pass

def find_command(cmdparts, d):
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
    return find_command(cmdparts[1:], value)
  return eval(value), cmdparts[1:]

def execute(command, context):
  parts = shlex.split(command)
  if not parts:
    raise CommandError("No command specified.")
  fn, args = find_command(parts, COMMANDS)
  return fn(context, *args)

def command_help(context, *args):
  if args:
    fn, args = find_command(args, COMMANDS)
    help(fn)
  else:
    help(command_help)

def goto_channel(context, *args):
  if len(args) != 1:
    raise CommandError("Try :channel go <name>")
  names = [x.name.lower() for x in lyre.client.channels]
  name = args[0]
  chs = [ch for ch in lyre.client.channels
    if ch.name.lower().startswith(name.lower())]
  if not chs:
    raise CommandError("No channel '{}'. Try: {}".format(
      name, ", ".join(names)))
  if len(chs) > 1:
    names = [ch.name.lower() for ch in chs]
    raise CommandError("Ambiguous prefix '{}'. Try: {}".format(
      name, ", ".join(names)))
  ch = chs[0]
  context.current_channel = ch.id

def next_channel(context, *args):
  return change_channel(context, 1)

def previous_channel(context, *args):
  return change_channel(context, -1)

def change_channel(context, direction=1, *args):
  if args:
    raise CommandError("Command takes no arguments.")
  ch = [ch for ch in lyre.client.channels if ch.id == context.current_channel]
  ch = ch[0]
  idx = lyre.client.channels.index(ch)
  if 0 <= idx + direction < len(lyre.client.channels):
    context.current_channel = lyre.client.channels[idx + direction].id
    return
  raise CommandError("No more channels.")
