import os
import tty
import time
import termios
import fcntl

from .output import *

keys = {
  b"[A":   "KEY_UP",
  b"[B":   "KEY_DOWN",
  b"[C":   "KEY_RIGHT",
  b"[D":   "KEY_LEFT",
  b"[H":   "KEY_HOME",
  b"[F":   "KEY_END",
  b"[5~":  "KEY_PAGEUP",
  b"[6~":  "KEY_PAGEDOWN",
  b"[2~":  "KEY_INS",
  b"[3~":  "KEY_DEL",
  b"OP":   "KEY_F1",
  b"OQ":   "KEY_F2",
  b"OR":   "KEY_F3",
  b"OS":   "KEY_F4",
  b"[15~": "KEY_F5"
}

# @see https://stackoverflow.com/questions/9043551/regex-that-matches-integers-only
def inputinteger(prompt, oldvalue=None, **kw) -> int:
  oldvalue = int(oldvalue) if oldvalue is not None else ""
  mask = kw["mask"] if "mask" in kw else r"^([+-]?[1-9]\d*|0)[ ,]?$"
  buf = inputstring(prompt, oldvalue, mask=mask, **kw)

  if buf is None or buf == "":
    return None
  
#  print(f"type(buf)={type(buf)!r}")
  if type(buf) is list:
    res = []
    for b in buf:
      try:
        res.append(int(b))
      except:
        return
#    echo(f"res={res!r}", level="debug")
    return res
  else:
#    echo("inputinteger.100: plain int, not a list", level="debug")
    try:
      res = int(buf)
    except:
      return
    else:
      return res

# @since 20110323
# @since 20190913
# @since 20200626
# @since 20200729
# @since 20200901
def inputstring(prompt:str, oldvalue=None, **kw) -> str:
  import readline
  args = kw["args"] if "args" in kw else {}
  debug = args.debug if "debug" in args else False
  def preinputhook():
    if debug is True:
      echo("inputstring.preinputhook.80: trace")

    multiple = kw["multiple"] if "multiple" in kw else False
    if debug is True:
      echo(f"inputstring.preinputhook.100: oldvalue={oldvalue!r}", level="debug")
    if type(oldvalue) is list:
      if debug is True:
        echo("inputstring.preinputhook.140: oldvalue is list", level="debug")
      for i in range(len(oldvalue)):
        oldvalue[i] = str(oldvalue[i])
      val = ", ".join(oldvalue)
    else:
      if debug is True:
        echo("inputstring.preinputhook.160: oldvalue is not list", level="debug")
      val = oldvalue
    if debug is True:
      echo(f"inputstring.preinputhook.120: oldvalue={oldvalue!r}", level="debug")
    readline.insert_text(str(val))
    readline.redisplay()

  echo(f"inputstring.100: oldvalue={oldvalue!r}", level="debug")
  if oldvalue is not None:
    readline.set_pre_input_hook(preinputhook)
#    echo("inputstring.120: pre_input_hook set", level="debug")

  inputfunc = input
  
  args = kw["args"] if "args" in kw else Namespace()

  mask = kw["mask"] if "mask" in kw else None

  returnseq = kw["returnseq"] if "returnseq" in kw else False

  multiple = kw["multiple"] if "multiple" in kw else None

  oldcompleter = readline.get_completer()
  completer = kw["completer"] if "completer" in kw else oldcompleter

  oldcompleterdelims = readline.get_completer_delims()
  completerdelims = kw["completerdelims"] if "completerdelims" in kw else oldcompleterdelims
  
  verify = kw["verify"] if "verify" in kw else None

#  if args is not None and "debug" in args and args.debug is True:
#    echo("inputstring.100: completerdelims=%r" % (completerdelims), interpret=False)
#    echo("completer is %r" % (completer))

  readline.parse_and_bind("tab: complete")
  if completer is not None and hasattr(completer, "complete") and callable(completer.complete) is True:
    if args is not None and "debug" in args and args.debug is True:
      echo("setting completer function", level="debug")
    readline.set_completer(completer.complete)
    if multiple is True:
      completerdelims += ", "
    readline.set_completer_delims(completerdelims)
  else:
    if args is not None and "debug" in args and args.debug is True:
      echo("completer is none or is not callable.")

  loop = True
  while loop:
    prompt = interpretecho(prompt)
#    prompt = rl_escape_prompt(prompt)
    buf = inputfunc(prompt) # interpretecho(prompt))

    if oldvalue is not None:
      readline.set_pre_input_hook(None)

    if buf is None or buf == "":
      if "noneok" in kw and kw["noneok"] is True:
        return None
      else:
        return oldvalue

    if mask is not None:
      if args is not None and "debug" in args and args.debug is True:
        echo(re.match(mask, buf), level="debug")

      if re.match(mask, buf) is None:
        echo("invalid input", level="error")
        continue

    if multiple is True:
#      echo("completerdelims=%r" % (completerdelims), interpret=False)
      foo = re.split("|".join(", "), buf)
      foo = [f.strip() for f in foo] # strip whitespace from items
      foo = [f for f in foo if f] # remove empty items
    else:
      foo = str(buf)
    
    if callable(verify) is True and verify(foo, **kw) is False:
      echo("verify is callable, verify() returned false", level="debug")
      loop = True
      continue

    break

  readline.set_completer(oldcompleter)
  readline.set_completer_delims(oldcompleterdelims)

  return foo

# @since 20230105 backported from ttyio6 (bugfix)
# @see https://ballingt.com/nonblocking-stdin-in-python-3/
def inputchar(prompt:str, options:str, default="", **kwargs): #default:str="", args:object=Namespace(), noneok:bool=False, helpcallback=None) -> str:
  args = kwargs["args"] if "args" in kwargs else None # Namespace()
  noneok = kwargs["noneok"] if "noneok" in kwargs else False
  helpcallback = kwargs["helpcallback"] if "helpcallback" in kwargs else None

  default = default.upper() if default is not None else ""

  options = options.upper()
  options = "".join(sorted(options))

  echo(prompt, end="", flush=True)

  if "?" not in options and callable(helpcallback) is True:
    options += "?"

  loop = True
  while loop:
    ch = getch(noneok=True) # .decode("UTF-8")
    if ch is not None:
      ch = ch.upper()

    if ch == "\n":
      if noneok is True:
        return None
      elif default is not None and default != "":
        return default
      else:
        echo("{bell}", end="", flush=True)
        continue
    elif (ch == "?" or ch == "KEY_F1") and callable(helpcallback) is True:
      echo("help")
      helpcallback()
      echo(prompt, end="", flush=True)
    elif ch is not None:
        if ch[:4] == "KEY_" or ch in options:
            break
        echo("{bell}", end="", flush=True)
        continue
     
  return ch

# @since 20210203
def inputboolean(prompt:str, default:str=None, options="YN") -> bool:
  ch = inputchar(prompt, options, default)
  if ch is not None:
    ch = ch.upper()
  if ch == "Y":
          echo("Yes")
          return True
  elif ch == "T":
          echo("True")
          return True
  elif ch == "N":
          echo("No")
          return False
  elif ch == "F":
          echo("False")
          return False
  return


terinallock = None

def getch(*args, **kwargs):
    noneok = kwargs["noneok"] if "noneok" in kwargs else False
    file = kwargs["file"] if "file" in kwargs else sys.stdin

    esc = False
    buf = ""

    class raw(object):
        def __init__(self, stream):
            self.stream = stream
            self.fd = self.stream.fileno()
        def __enter__(self):
            self.original_stty = termios.tcgetattr(self.stream)

            newattr = termios.tcgetattr(self.fd)

            self.new_stty = termios.tcgetattr(self.stream)
            tty.setcbreak(self.stream)
#            self.new_stty[3] = self.new_stty[3] & ~termios.ECHO
#            termios.tcsetattr(self.fd, termios.TCSANOW, self.new_stty)

        def __exit__(self, type, value, traceback):
            termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)

    class nonblocking(object):
        def __init__(self, stream):
            self.stream = stream
            self.fd = self.stream.fileno()
        def __enter__(self):
            self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)
        def __exit__(self, *args):
            fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)

    loop = True
    with raw(sys.stdin):
        with nonblocking(sys.stdin):
            while loop:
                try:
                    ch = sys.stdin.read(1)
#                    print(f"ch={ch!r} type(ch)={type(ch)!r}")
                    if ch == ESC:
                        esc = True
                        buf = ""
                        continue

                    if ch == "\x01":
                        ch = "KEY_HOME"
                        break
                    elif ch == "\x04":
                        raise EOFError
                    elif ch == "\x05":
                        ch = "KEY_END"
                        break
                    elif ch == "\x15": # ^U
                        ch = "KEY_ERASETOBOL"
                        break
                    elif ch == "\x7f":
                        ch = "KEY_BACKSPACE"
                        break
                    if esc is True:
                        buf += ch # bytes(ch, "utf-8")
                        if buf in keys:
                          ch = keys[buf]
                          loop = False
                          esc = False
                          buf = ""
                          break
                        elif len(buf) > 3:
                          echo(f"buf={buf!r}", flush=True, level="debug")
                          esc = False
                          buf = ""
                    else:
                        if len(ch) > 0:
                            break
                finally:
                    if ch is not None and len(ch) > 1:
                        break
                    if ch is None and noneok is True:
                        break

                    time.sleep(0.042)
    return ch


def accept(prompt:str, options:str, default:str="", debug:bool=False) -> str:
#  if debug is True:
#    echo("ttyio4.accept.100: options=%s" % (options), level="debug")
        
  default = default.upper() if default is not None else ""
  options = options.upper()
  echo(prompt, end="", flush=True)

  while 1:
    ch = getch().upper()

    if ch == "\n":
      return default
      if default is not None:
        return default
      else:
        return ch
    elif ch in options:
      return ch
