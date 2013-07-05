
def fixed_width_suffix(base, suffix, width):
  extra = max(0, len(base) - width)
  pad = max(0, width - len(base))
  if extra:
    base = base[:-extra]
  base += " " * pad
  if len(suffix):
    base = base[:-len(suffix)] + suffix
  return base
