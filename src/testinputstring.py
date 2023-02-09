import bbsengine5 as bbsengine
import ttyio5 as ttyio

def inputstring(prompt, originalvalue=42, **kw):
  mask = kw["mask"] if "mask" in kw else None

  buf = ""
  pos = 0

  ttyio.echo(prompt, flush=True, end="")

  mode_insert = True

  loop = True
  while loop:
    bottombar = f"pos={pos:03d}"
    if mode_insert is True:
      bottombar += " INS"
    else:
      bottombar += " OVR"
    bbsengine.setarea(bottombar)
    ch = ttyio.getch()
    if ch == "\n":
        return buf
    if ch == "KEY_CUTTOBOL": # ^U erase from point to bol, copy to clipboard
        ttyio.echo("CTRL-U")
        continue
    elif ch == "KEY_BACKSPACE":
        if pos > 0:
            pos -= 1
            ttyio.echo(chr(8)+" "+chr(8), flush=True, end="")
            buf = buf[pos:len(buf)-1]
        else:
            ttyio.echo("{bell}", end="",flush=True)
            pos = 0
        continue
    elif ch == "KEY_LEFT":
        if pos == 0:
          ttyio.echo("{bell}", end="")
        else:
          ttyio.echo("{cursorleft}", end="", flush=True)
          pos -= 1
        continue
    elif ch == "KEY_RIGHT":
        if pos <= len(buf):
          pos += 1
          ttyio.echo("{cursorright}", end="", flush=True)
        else:
          ttyio.echo("{bell}", end="", flush=True)
        continue
    elif ch == "KEY_HOME":
      if pos == 0:
        ttyio.echo("{bell}", end="", flush=True)
      else:
        ttyio.echo(f"{{cursorleft:{pos}}}", end="", flush=True)
        pos = 0
      continue
    elif ch == "KEY_END":
        if pos < len(buf):
          z = len(buf) - pos
          ttyio.echo(f"{{cursorright:{z}}}", end="", flush=True)
          pos = len(buf)
        continue
    elif ch == "KEY_INS":
        mode_insert = True - mode_insert
        continue
    elif ch[:4] == "KEY_":
        ttyio.echo("key=%r" % (ch), level="debug")
        continue

    if mask is not None:
      ttyio.echo(mask, flush=True, end="")
    else:
      # ttyio5.echo(ch.decode("utf-8"), flush=True, end="")
      ttyio.echo(ch, flush=True, end="")

    buf = buf[:pos] + ch + buf[pos:] # [pos] = ch
    pos += 1
  return buf

def main(args=None, **kw):
  originalvalue = 42
  buf = inputstring("{var:promptcolor}prompt: {var:inputcolor}", originalvalue, multiple=True)
  ttyio.echo("{/all}")
  print(buf)

if __name__ == "__main__":
  bbsengine.initscreen()
  main()
  ttyio.echo("{reset}")
