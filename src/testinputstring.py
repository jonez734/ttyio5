import bbsengine5 as bbsengine
import ttyio5 as ttyio

def getchinputstring(prompt, originalvalue=42, **kw):
    mask = kw["mask"] if "mask" in kw else None

#    buf = str(originalvalue)
    buf = ""
    pos = len(buf)

    def display():
      curleft = f"{{cursorleft:{len(buf)-pos}}}"
      ttyio.echo(f"{{cursorhpos:1}}{{eraseline}}{prompt}{buf}{curleft}", flush=True, end="")
      bbsengine.setarea(f"pos: {pos} len(buf): {len(buf)} len(prompt): {len(prompt)}")

    loop = True
    while loop:
        if len(buf)-pos < 0:
          pos = 0

        display()
        ch = ttyio.getch()
        if ch == "KEY_ENTER":
            return buf
        elif ch == "KEY_CUTTOBOL": # ^U erase from point to bol, copy to clipboard
            buf = buf[pos:]
#            for x in range(0, pos):
#              ttyio.echo("X", flush=True, end="")
#              ttyio.echo(chr(8)+" "+chr(8), flush=True, end="")
            pos = 0
            continue
        elif ch == "KEY_BACKSPACE":
            if pos > 0:
#                ttyio.echo(chr(8)+" "+chr(8), flush=True, end="")
                buf = buf[:pos-1]+buf[pos:]
                pos -= 1

            else:
                ttyio.echo("{bell}", end="",flush=True)
                pos = 0
            continue
        elif ch == "KEY_LEFT":
            if pos == 0:
              ttyio.echo("{bell}", end="", flush=True)
            else:
              ttyio.echo("{cursorleft}", end="", flush=True)
              pos -= 1
            continue
        elif ch == "KEY_RIGHT":
            if pos < len(buf):
              pos += 1
              ttyio.echo("{cursorright}", end="", flush=True)
            else:
              ttyio.echo("{bell}", end="", flush=True)
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

        buf = buf[:pos] + ch + buf[pos:]
        pos += 1

bbsengine.initscreen()

originalvalue = 42
buf = getchinputstring("{var:promptcolor}prompt: {var:inputcolor}", originalvalue, multiple=True)
#buf = getchinputstring("prompt: ", originalvalue, multiple=True)
ttyio.echo("{/all}")
print(buf)
