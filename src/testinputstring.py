import ttyio5 as ttyio

def inputstring(prompt, originalvalue=42, **kw):
    mask = kw["mask"] if "mask" in kw else None

    buf = ""
    pos = 0
    
    ttyio.echo(prompt, flush=True, end="")

    loop = True
    while loop:
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
              ttyio.echo("key_left bell", end="")
            else:
              ttyio.echo("{cursorleft}", end="", flush=True)
              pos -= 1
            continue
        elif ch == "KEY_RIGHT":
            if pos <= len(buf):
              pos += 1
              ttyio.echo("{cursorright}", end="", flush=True)
            else:
              ttyio.echo("cursorright bell", end="", flush=True)
            continue
        elif ch == "KEY_HOME":
            ttyio.echo("{cursorleft:%d}" % (pos), end="", flush=True)
            pos = 0
            continue
        elif ch == "KEY_END":
            if pos < len(buf):
              z = len(buf) - pos
              ttyio.echo("{cursorright:%d}" % (z), end="", flush=True)
              pos = len(buf)
            continue
        elif ch[:4] == "KEY_":
            ttyio.echo("key=%r" % (ch), level="debug")
            continue

        if mask is not None:
          ttyio.echo(mask, flush=True, end="")
        else:
          # ttyio5.echo(ch.decode("utf-8"), flush=True, end="")
          ttyio.echo(ch, flush=True, end="")

        buf += ch
        pos += 1
    
originalvalue = 42
buf = inputstring("{var:promptcolor}prompt: {var:inputcolor}", originalvalue, multiple=True)
ttyio.echo("{/all}")
print(buf)
