import re
import sys
from typing import Any, List, NamedTuple
from argparse import Namespace

from .vars import *
from .terminal import getterminalwidth
from .constants import *
from .lib import *

class Token(NamedTuple):
    type: str
    value: str

token_specification = [
    ("ACS",        r'\{ACS:([a-z\d]+)(:([\d]{,3}))?\}'),
    ("OPENBRACE",  r'\{\{'),
    ("CLOSEBRACE", r'\}\}'),
    ("RESETCOLOR", r'\{/ALL\}'),
    ("RESET",      r'\{RESET\}'), # reset color+margins
    ("F6",         r'\{F6(:(\d{,2}))?\}'), # force a carriage return
    ("CURPOS",     r'\{CURPOS:(\d{,3})(,(\d{,3}))?\}'), # NOTE! this is y,x (ala ncurses) @see https://regex101.com/r/6Ww6sg/1
    ("WHITESPACE", r'[ \t\n]+'), # iswhitespace()
    ("CHA",	       r'\{CHA(:(\d{,3}))?\}'), # Moves the cursor to column n (default 1). 
    ("ERASELINE",  r'\{(ERASELINE|EL)(:(\d))?\}'), # erase line
    ("DECSC",      r'\{DECSC\}'), # save cursor position and current attributes
    ("DECRC",      r'\{DECRC\}'), # restore cursor position and attributes
    ("DECSTBM",    r'\{DECSTBM(:(\d{,3})(,(\d{,3}))?)?\}'),  # Set Top, Bottom Margin
    ("BELL",       r'\{BELL(:(\d{,2}))?\}'),
    ("VAR",	       r'\{VAR:([\w.-]+)\}'),
    ("CURSORUP",   r'\{CURSORUP(:(\d{,3}))?\}'),
    ("CURSORRIGHT",r'\{CURSORRIGHT(:(\d{,3}))?\}'), # {cursorright:4}
    ("CURSORLEFT", r'\{CURSORLEFT(:(\d{,3}))?\}'),
    ("CURSORDOWN", r'\{CURSORDOWN(:(\d{,3}))?\}'),
    ("WAIT",       r'\{WAIT:(\d{,4})\}'),
    ("UNICODE",    r'\{(U|UNICODE):([a-z]+)(:([0-9]{,3}))?\}'),
    ("EMOJI",      r':([a-zA-Z0-9_-]+):'),
    ("HIDECURSOR", r'\{(INVISCURSOR|HIDECURSOR)\}'),
    ("SHOWCURSOR", r'\{(VISCURSOR|SHOWCURSOR)\}'),
    ("ERASEDISPLAY", r'\{(ERASEDISPLAY|ED)(:(tobottom|totop|all))?\}' ), # 0 (or ommitted) - clear all of display; 1 = cursor to beginning of screen; 2 = cursor to end of screen
    ("CURSORHPOS",   r'\{(CURSORHPOS)(:(\d{,3}))\}'),
    ("RGB",          r'\{rgb:#?((?:[\da-fA-F]{2}){3})\}'),
    ("COMMAND",    r'\{[^\}]+\}'),     # {red}, {brightyellow}, etc
    ("WORD",       r'[^ \t\n\{\}]+'),
    ("MISMATCH",   r'.')            # Any other pattern
]

# @see https://docs.python.org/3/library/re.html#writing-a-tokenizer
def __tokenizeecho(buf:str, args:object=Namespace()):
    global tok_regex_c

    if type(buf) is not str:
      return buf

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    buf = buf.replace("\n", " ") # why?
    for mo in re.finditer(tok_regex, buf, re.IGNORECASE):
        kind = mo.lastgroup
##        print("kind=%r mo.groups()=%r" % (kind, mo.groups()))

#        print("%r: " % (kind))
#        for g in range(1, len(mo.groups())+1):
#          print("%d: %s" % (g, mo.group(g)))

#        if include is not [] and kind.upper() not in include:
#          continue
        value = mo.group()
        if kind == "WHITESPACE":
          if value == "\n":
            value = " "
          # print("whitespace. value=%r" % (value))
#        elif kind == "COMMAND":
#            pass
#        elif kind == "WORD":
#            pass
        elif kind == "F6":
          value = mo.group(11) or 1
        elif kind == "MISMATCH":
            pass
            # raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        elif kind == "OPENBRACE":
          value = "{"
        elif kind == "CLOSEBRACE":
          value = "}"
        elif kind == "BELL":
          value = mo.group(33) or 1
        elif kind == "DECSTBM":
          top = mo.group(28) or 0
          bot = mo.group(30) or 0
          value = (int(top), int(bot))
        elif kind == "CURPOS":
          y = mo.group(13)
          x = mo.group(15) or 0
          value = (int(y), int(x))
        elif kind == "DECSC":
          pass
        elif kind == "DECRC":
          pass
        elif kind == "CHA":
          value = mo.group(2) or 1
        elif kind == "ERASELINE":
          value = mo.group(3) or 0
        elif kind == "ACS":
          # print(mo.groups())
          # @FIX: why the huge offset?
          command = mo.group(2)
          repeat = mo.group(4) or 1
          value = (command, repeat)
          # print("value.command=%r, value.repeat=%r" % (command, repeat))
        elif kind == "VAR":
#          print("var! mo.groups=%r" % (repr(mo.groups())))
          try:
            var = mo.group(35)
            value = getvariable(var)
          except RecursionError:
            echo("too much recursion")
#            continue
#          print("var=%r value=%r" % (var, value))
          for t in __tokenizeecho(str(value)):
            # print("{var} yielding token %r" % (t,))
            yield t
          # print("__tokenizemci.100: var=%r value=%r" % (var, value))
        elif kind == "CURSORUP":
          value = mo.group(38) or 1 # \x1b[<repeat>A
        elif kind == "CURSORRIGHT":
          value = mo.group(41) or 1
        elif kind == "CURSORLEFT":
          value = mo.group(44) or 1
        elif kind == "CURSORDOWN":
          value = mo.group(47) or 1
        elif kind == "WAIT":
          value = int(mo.group(49) or 1)
        elif kind == "UNICODE":
          name = mo.group(52)
          repeat = mo.group(54) or 1
#          print("unicode.100: name=%s repeat=%r" % (name, repeat))
          value = (name, int(repeat))
        elif kind == "EMOJI":
          value = mo.group(56)
        elif kind == "EMICH":
          value = mo.group(58)
        elif kind == "HIDECURSOR":
          pass
        elif kind == "SHOWCURSOR":
          pass
        elif kind == "ERASEDISPLAY":
          value = mo.group(64)
          if value == "tobottom":
            value = 1
          elif value == "totop":
            value = 2
          else:
            value = 0
        elif kind == "CURSORHPOS":
          value = int(mo.group(68))
        elif kind == "RGB":
          g = mo.group(70)
          if g is not None:
            value = tuple(bytes.fromhex(g))
          else:
            value = g

        t = Token(kind, value)
        # print("yielding token %r" % (t,))
        yield t

def interpretecho(buf:str, **kw) -> str: #wordwrap:bool=True, end:str="\n", args=Namespace(), indent:str="---") -> str:
  width = kw["width"] if "width" in kw else None
  strip = kw["strip"] if "strip" in kw else False
  wordwrap = kw["wordwrap"] if "wordwrap" in kw else True
  end = kw["end"] if "end" in kw else "\n"
  args = kw["args"] if "args" in kw else Namespace()
  indent = kw["indent"] if "indent" in kw else ""

  result = indent
  def handlecommand(table, value):
    for item in table:
      command = item["command"]
      if value == command:
        return CSI+item["ansi"] # "\033[%s" % (item["ansi"])
    return False

  if buf is None or buf == "":
    return ""

  if strip is True:
    result = ""
    for token in __tokenizeecho(buf):
      if token.type == "WORD" or token.type == "WHITESPACE":
        result += token.value
#      elif token.type == "EMOJI":
#        result += "    " # emoji[token.value]
    return result

  if width is None:
    width = getterminalwidth()

  pos = 0
  for token in __tokenizeecho(buf):
      if token.type == "F6":
          v = token.value if token.value is not None else 1
          result += "\n"*int(v)# +indent
          pos = 0
      elif token.type == "WHITESPACE":
          result += token.value
          pos += len(token.value)
      elif token.type == "BELL":
        result += "\007"*int(token.value)
      elif token.type == "COMMAND":
        if strip is False:
          value = token.value.lower()
          res = False
          for t in [echocommands, colors, bgcolors]:
            res = handlecommand(t, value)
            if type(res) == str:
              result += res
              break
          if res is False:
            result += value
            #print("syntax error: %r" % (value))
            #raise ValueError
      elif token.type == "DECSC":
        result += CSI+"s"
      elif token.type == "DECRC":
        result += CSI+"u"
      elif token.type == "CURPOS":
        y, x = token.value
        result += CSI+"%d;%dH" % (y, x)
      elif token.type == "DECSTBM":
        top, bot = token.value
        if bot == 0:
          result += CSI+"%dr" % (top)
        else:
          result += CSI+"%d;%dr" % (top, bot)
      elif token.type == "RESETCOLOR":
        result += CSI+"0;39;49m"
      elif token.type == "RESET":
        result += CSI+"0;39;49m\033[s\033[0;0r\033[u"
      elif token.type == "CHA": # Moves the cursor to column n (default 1)
        result += CSI+"%dG" % (token.value)
      elif token.type == "ERASELINE": # Erases part of the line. If n is 0 (or missing), clear from cursor to the end of the line. If n is 1, clear from cursor to beginning of the line. If n is 2, clear entire line. Cursor position does not change. 
        result += CSI+"%dK" % (token.value)
      elif token.type == "ACS": # use alternate character set
        # print("acs. value=%s" % (str(token.value)))
        command, repeat = token.value
        # print("command=%r, repeat=%r" % (command, repeat))
        if command is not None and command.upper() in acs:
          char = acs[command.upper()]
          result += "\033(0%s\033(B" % (char*int(repeat))
          pos += len(char*int(repeat))
      elif token.type == "CURSORUP": # {cursorup:10}
        repeat = int(token.value)
        result += CSI+"%dA" % (repeat)
      elif token.type == "CURSORDOWN":
        repeat = int(token.value)
        result += CSI+"%dB" % (repeat)
#        print("result=%r" % (result))
      elif token.type == "CURSORRIGHT":
        repeat = int(token.value)
        result += CSI+"%dC" % (repeat)
      elif token.type == "CURSORLEFT":
        repeat = int(token.value)
        result += CSI+"%dD" % (repeat)
      elif token.type == "WAIT":
        duration = int(token.value)
#        echo("duration=%r" % (duration))
#        time.sleep(duration*0.250)
      elif token.type == "UNICODE":
        (name, repeat) = token.value
        name = name.upper()
#        print("name=%s repeat=%s" % (name, repeat))
        if name in unicode:
          result += unicode[name]*repeat
      elif token.type == "EMOJI":
        name = token.value # :smile:
        if name in emoji:
          result += emoji[name]
      elif token.type == "WORD":
        if wordwrap is True:
          if pos+len(token.value) >= width-1:
            result += "\n"
            pos = len(token.value) # len(indent)+len(token.value)
            result += token.value # indent+token.value
          else:
            result += token.value
            pos += len(token.value)
        else:
          result += token.value
      elif token.type == "OPENBRACE" or token.type == "CLOSEBRACE":
        result += token.value
        pos += 1
      elif token.type == "HIDECURSOR":
        result += CSI+"?25l"
      elif token.type == "SHOWCURSOR":
        result += CSI+"?25h"
      # @see https://en.wikipedia.org/wiki/ANSI_escape_code
      # 0 = entire display (default)
      # 1 = cursor to end of display
      # 2 = cursor to top of display
      elif token.type == "ERASEDISPLAY":
        result += f"{CSI}{token.value}J" # CSI+"%dJ" % (token.value)
      elif token.type == "CURSORHPOS":
        result += CSI+"%dG" % (token.value)
      elif token.type == "RGB":
        result += CSI+rgb(38, token.value) # (255, 255, 255))}, # )"38;2;255;255;255m", "rgb": (255,255,255) }, # 37m
        result += ""

#  print("result=%s" % (result))
  return result

def echo(buf:str="", **kw):
  width = kw["width"] if "width" in kw else getterminalwidth()
  level = kw["level"] if "level" in kw else None
  strip = kw["strip"] if "strip" in kw else False
  wordwrap = kw["wordwrap"] if "wordwrap" in kw else True
  flush = kw["flush"] if "flush" in kw else True
  end = kw["end"] if "end" in kw else "\n"
  indent = kw["indent"] if "indent" in kw else ""
  args = kw["args"] if "args" in kw else Namespace()
  interpret = kw["interpret"] if "interpret" in kw else True
  datestamp = kw["datestamp"] if "datestamp" in kw else False
  file = kw["file"] if "file" in kw else sys.stdout
  if datestamp is True:
    now = datetime.now(tzlocal())
    stamp = strftime("%Y-%b-%d %I:%M:%S%P %Z (%a)", now.timetuple())
    buf = "%s %s" % (stamp, buf)

  prefix = ""
  if level is not None:
    if level == "debug":
      prefix = "{bglightblue}{blue}"
    if level == "warn" or level == "warning":
      prefix = "{bgyellow}{black}"
    elif level == "error":
      prefix = "{bgred}{black}"
    elif level == "success" or level == "ok":
      prefix = "{bggreen}{black}"
    elif level == "info":
      prefix = "{bgwhite}{blue}"

#    buf = f"{prefix}{buf}{{var:normalcolor}}"
    buf = "%s %s %s" % (interpretecho(prefix), buf, interpretecho("{/all}"))
    interpret = False

  if interpret is True:
    try:
      buf = interpretecho(buf, strip=strip, width=width, end=end, wordwrap=wordwrap, args=args, indent=indent)
    except RecursionError:
      print("recursion error!")

  print(buf, end=end, file=file, flush=flush)
  return
