#
# Copyright (C) 2022 zoidtechnologies.com. All Rights Reserved.
#

import re
import os
import sys
import tty
import time
import termios
import fcntl
import select
import signal
import socket
import threading

from datetime import datetime
from time import strftime

from dateutil.tz import *

from typing import Any, List, NamedTuple
from argparse import Namespace

ESC = b"\033"
#CSI = ESC+"["
CSI = "\x9b"

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

unicode = {
  "HEART":           "\u2665",
  "DIAMOND":         "\u2666",
  "CLUB":            "\u2663",
  "SPADE":           "\u2660",
  "LIGHTSHADE":      "\u2591",
  "MEDIUMSHADE":     "\u2592",
  "DARKSHADE":       "\u2593",
  "SOLIDBLOCK":      "\u2588",
  "BLOCKUPPERHALF":  "\u2580",
  "BLOCKLEFTHALF":   "\u258C",
  "BLOCKCORNER":     "\u25A0",
  "SV":              "\u2502",
  "SVSL":            "\u2524",
  "DVDL":            "\u2563",
  "DVDR":	     "\u2560",
  "DV":              "\u2551",
  "DRDVCORNER":      "\u2554",
  "DHLINE":          "\u2550",
  "DLDVCORNER":      "\u2557",
  "DVLINE":          "\u2551",
  "DVDRCORNER":	     "\u255a",
  "DVDLCORNER":  "\u255d",
  "DVDHRTEE":    "\u2560",
  "DVDHLTEE":    "\u2563",
  "DVSHRTEE":    "\u255F",
  "DVSHLTEE":	 "\u2562",
  "SVDHCROSS":   "\u256A",
  "SVSHCROSS":   "\u253C",
  "DVSHCROSS":   "\u256B",
  "DVDHCROSS":   "\u256C", # double vertical double horizontal cross
  "DIEONE":      "\u2680",
  "DIETWO":      "\u2681",
  "DIETHREE":    "\u2682",
  "DIEFOUR":     "\u2683",
  "DIEFIVE":     "\u2684",
  "DIESIX":      "\u2685",
}

# https://stackoverflow.com/questions/3220031/how-to-filter-or-replace-unicode-characters-that-would-take-more-than-3-bytes
# https://medium.com/analytics-vidhya/how-to-print-emojis-using-python-2e4f93443f7e
emoji = {
  "grin":                   "\U0001F600",
  "smile":                  "\U0001f642",
  "rofl":                   "\U0001f923",
  "wink":                   "\U0001f609",
  "thinking":               "\U0001f914",
  "sunglasses":             "\U0001f60e",
  "100":                    "\U0001f4af",
  "thumbup":                "\U0001f44d",
  "thumbdown":              "\U0001f44e",
  "vulcan":                 "\U0001f596",
  "spiral":                 "\U0001f4ab",
  "fire":                   "\U0001f525",
  "bank":                   "\U0001f3e6",
  "house":                  "\U0001f3e0",
  "military-helmet":        "\U0001fa96",
  "door":                   "\U0001f6aa",
  "receipt":                "\U0001f9fe",
  "newspaper":              "\U0001f4f0",
  "prince":                 "\U0001f934",
  "princess":               "\U0001f478",
  "thread":                 "\U0001f9f5",
  "ice":                    "\U0001f9ca",
  "moneybag":               "\U0001f4b0",
  "person":                 "\U0001f9d1",
  "sun":                    "\U00002600", # @see https://emojipedia.org/sun/
  "thunder-cloud-and-rain": "\U000026C8", # @see https://emojipedia.org/cloud-with-lightning-and-rain/
  "crop":                   "\U0001F33E", # @see https://emojipedia.org/sheaf-of-rice/
  "horse":                  "\U0001F40E", # @see https://emojipedia.org/horse/
  "cactus":                 "\U0001F335", # @see https://emojipedia.org/cactus/
  "ship":                   "\U0001F6A2", # @see https://emojipedia.org/ship/
  "wood":                   "\U0001FAB5", # @see https://emojipedia.org/wood/
  "link":                   "\U0001F517", # @see https://emojipedia.org/link/
  "anchor":                 "\U00002693", # @see https://emojipedia.org/anchor/
  "ballot-box":             "\U0001F5F3", # @see https://emojipedia.org/ballot-box-with-ballot/ @blacklist breaks monospace font
  "building":               "\U0001F3DB", # @see https://emojipedia.org/classical-building/
  "envelope":               "\U00002709", # @see https://emojipedia.org/envelope/
  "dolphin":                "\U0001F42C", # @see https://emojipedia.org/dolphin/
  "bellhop-bell":           "\U0001F6CE", # @see https://emojipedia.org/bellhop-bell/
  "hotel":                  "\U0001F3E8", # @see https://emojipedia.org/hotel/

  "waninggibbousmoon":      "\U0001F316",
  "waxinggibbousmoon":      "\U0001F314",
  "waningcrescentmoon":     "\U0001F318",
  "waxingcrescentmoon":     "\U0001F312",
  "lastquartermoon":        "\U0001F317",
  "firstquartermoon":       "\U0001F313",
  "newmoon":                "\U0001F311",
  "fullmoon":               "\U0001F315",

  "sco":                    "\U0000264F", # @see https://emojipedia.org/search/?q=zodiac
  "sag":                    "\U00002650",
  "cap":                    "\U00002651",
  "aqu":                    "\U00002652",
  "pic":                    "\U00002653",
  "ari":                    "\U00002648",
  "tau":                    "\U00002649",
  "gem":                    "\U0000264A",
  "can":                    "\U0000264B",
  "leo":                    "\U0000264C",
  "vir":                    "\U0000264D",
  "lib":                    "\U0000264E",

  "package":                "\U0001F4E6", # @since 20220907 @see https://emojipedia.org/package/
  "compass":                "\U0001F9ED", # @since 20220907
  "worldmap":               "\U0001F5FA", # @since 20220916

  "wolf":                   "\U0001F43A", # @since 20221002
  "person":                 "\U0001F9D1",
  
  "supervillian":           "\U0001F9B9", # @since 20221016
  "joker":                  "\U0001F0CF", # @since 20221127

  "warning":                "\U000026A0",
  "stopsign":               "\U0001F6D1",
}

terinallock = None

#
# @see https://stackoverflow.com/a/1052115
#
#def _getch(timeout=0.0):
#    fd = sys.stdin.fileno()
#    old_settings = termios.tcgetattr(fd)
#    try:
#        tty.setraw(fd)
#        (r, w, e) = select.select([sys.stdin], [], [], timeout)
#        if r == []:
#            return None
#        ch = sys.stdin.read(1)
#    finally:
#        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#    return ch

# @see http://www.python.org/doc/faq/library.html#how-do-i-get-a-single-keypress-at-a-time
# @see http://craftsman-hambs.blogspot.com/2009/11/getch-in-python-read-character-without.html
# def getch(noneok:bool=False, timeout=0.000125, echoch=False) -> str:
#   fd = sys.stdin.fileno()
#
#   oldterm = termios.tcgetattr(fd)
#
#   newattr = termios.tcgetattr(fd)
#
#   newattr[3] = newattr[3] & ~termios.ICANON
#
#   if echoch is False:
#     newattr[3] = newattr[3] & ~termios.ECHO
#
#   termios.tcsetattr(fd, termios.TCSANOW, newattr)
#
#   oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
#   # fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
#   try:
# #      echo("ttyio4.getch.220: before while true")
#       buf = ""
#       flag = False
#       while True:
# #        echo("ttyio4.getch.200: flag=%r" % (flag), level="debug")
#         try:
#           r, w, x = select.select([fd], [], [], timeout)
#         except socket.error as e:
#           echo("%r: %r" % (e.code, e.msg), level="error")
#           if e.args[0] == 4:
#             echo("interupted system call (tab switch?)", level="warning")
#             continue
#
#         if len(r) == 0 and noneok is True:
#           break
#
#        echo("ttyio4.getch.120: flag=%r, buf=%r" % (flag, buf))
#         ch = sys.stdin.read(1)
# #        return ch
#
#         if ch == chr(1): # ctrl-a
#           return "KEY_HOME"
#         elif ch == chr(5): # ctrl-e
#           return "KEY_END"
#         elif ch == chr(27):
#           flag = True
#           buf = ""
# #          timeout = 0.00125
#         elif flag is True:
#           buf += ch
#           if buf in keys:
#             return keys[buf]
#           else:
#             if len(buf) >= 4:
#               echo("{bell}", end="", flush=True)
#               # echo("buf=%r, len=%d" % (buf, len(buf)), level="debug")
#               flag = False
#               buf = ""
#         else:
#           return ch
#   finally:
#         termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
#         fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
#       # echo("{/all}", end="") # print ("\033[0m", end="")
#
# #  return ch

def inittermios():
  fd = sys.stdin.fileno()

  old_settings = termios.tcgetattr(fd)

  new_settings = termios.tcgetattr(fd)
  new_settings[3] = new_settings[3] & ~termios.ICANON
  new_settings[3] = new_settings[3] & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
  os.set_blocking(fd, False)
  return old_settings

def getch(timeout=1, init=True, noneok=False, echoch=False):
  def handlesigint(_, __):
    print("^C")
    raise KeyboardInterrupt

  if init is True:
    old_settings = inittermios()
#    signal.signal(signal.SIGINT, handlesigint)

  ch = None
  fd = sys.stdin.fileno()

  try:
    buf = ""
    esc = False
    loop = True
    while loop:
      
      (r, w, e) = select.select([sys.stdin], [], [], timeout)
      if r == []:# and noneok is True:
        loop = False
        ch = None
        buf = b""
        break

      ch = os.read(sys.stdin.fileno(), 1)
#      ttyio.echo("inputkey.60: ch=%r" % (ch), level="debug")
      if ch == b"\x01":
        ch = "KEY_HOME"
        break
      elif ch == b"\x04":
        raise EOFError
      elif ch == b"\x05":
        ch = "KEY_END"
        break
      elif ch == b"\x15": # ^U
        ch = "KEY_ERASETOBOL"
        break
      elif ch == ESC:
        esc = True
        buf = b""
        continue
      elif ch == b"\x7f":
        ch = "KEY_BACKSPACE"
        break

      if esc is True:
        buf += ch
        if buf in keys:
          ch = keys[buf]
          loop = False
          esc = False
          buf = b""
          break
      else:
        break
  except EOFError:
    raise
  except Exception:
    import traceback
    traceback.print_exc()
  finally:
    if init is True:
      fd = sys.stdin.fileno()
      termios.tcsetattr(fd, termios.TCSAFLUSH, old_settings)
    if type(ch) is bytes:
      return ch.decode("utf-8")
    return ch

# @since 20201105
def inputchar(prompt:str, options:str, default:str="", args:object=Namespace(), noneok:bool=False, helpcallback=None) -> str:
#  if "debug" in args and args.debug is True:
#    echo("ttyio4.inputchar.100: options=%s" % (options), level="debug")

  default = default.upper() if default is not None else ""

  options = options.upper()
  options = "".join(sorted(options))
#  echo(f"options={options!r}", level="debug")

  echo(prompt, end="", flush=True)

  if "?" not in options and callable(helpcallback) is True:
    options += "?"

#  signal.signal(signal.SIG_INT, signal.SIG_DFL)
  loop = True
  while loop:
    try:
      # getch returns bytes
      ch = getch(noneok=False) # .decode("UTF-8")
#      if type(ch) is str:
#        ch = bytes(ch, "utf-8")
#    except KeyboardInterrupt:
#      raise
    except Exception:
      import traceback
      traceback.print_exc()
      break

    if ch is not None:
      ch = ch.upper()

    if ch == "\n":
      if noneok is True:
        # echo("inputchar.110: noneok is true, returning none.")
        return None
      elif default is not None and default != "":
        # echo("inputchar.120: returning default %r" % (default))
        return default
      else:
        echo("{bell}", end="", flush=True)
        continue
    elif ch == "\004":
      raise EOFError
    elif (ch == "?" or ch == "KEY_F1") and callable(helpcallback) is True:
      echo("help")
      helpcallback()
      echo(prompt, end="", flush=True)

    elif (ch is not None) and (ch[:4] == "KEY_" or ch in options):
      break
    elif ch is not None:
      echo("{bell}", end="", flush=True)
      continue

  if type(ch) is bytes:
    return ch.decode("utf-8")
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

def darken(prefix, rgb, percentage):
  if len(rgb) == 3:
    (r, g, b) = rgb
    a = 1
  elif len(rgb) == 4:
    (r, g, b, a) = rgb
  r *= 1-percentage
  g *= 1-percentage
  b *= 1-percentage
  return "%s;2;%d;%d;%d;%dm" % (prefix, r, g, b, a)

def rgb(prefix, rgb):
  if len(rgb) == 3:
    (r, g, b) = rgb
    a = 1
  elif len(rgb) == 4:
    (r, g, b, a) = rgb
  ansi = "%s;2;%s;%s;%s;%sm" % (prefix, r, g, b, a)
  return ansi

# c64 color palette
colors = (
{ "command": "{white}",      "ansi": rgb(38, (255, 255, 255))}, # )"38;2;255;255;255m", "rgb": (255,255,255) }, # 37m
{ "command": "{red}",        "ansi": rgb(38, (136, 0, 0))}, # "38;2;136;0;0m"},
{ "command": "{cyan}",       "ansi": rgb(38, (170, 255, 238))}, # "38;2;170;255;238m"},
{ "command": "{purple}",     "ansi": rgb(38, (204, 68, 204))}, #"38;2;204;68;204m"},
{ "command": "{green}",      "ansi": rgb(38, (0, 204, 85))},#"38;2;0;204;85m"},
{ "command": "{blue}",       "ansi": rgb(38, (0, 0, 170))},#"38;2;0;0;170m"},
{ "command": "{yellow}",     "ansi": rgb(38, (238, 238, 119))},#"38;2;238;238;119m"},
{ "command": "{orange}",     "ansi": rgb(38, (221, 136, 85))},#"38;2;221;136;85m"},
{ "command": "{brown}",      "ansi": rgb(38, (102, 68, 0))},#"38;2;102;68;0m"},
{ "command": "{lightred}",   "ansi": rgb(38, (255, 119, 119))},#"38;2;255;119;119m"},
{ "command": "{darkgray}",   "ansi": rgb(38, (51, 51, 51))},#"38;2;51;51;51m"},
{ "command": "{gray}",       "ansi": rgb(38, (119, 119,119))}, # "38;2;119;119;119m"},
{ "command": "{lightgreen}", "ansi": rgb(38, (170, 255, 102))},#"38;2;170;255;102m"},
{ "command": "{lightblue}",  "ansi": rgb(38, (0, 136, 255))},#"38;2;0;136;255m"},
{ "command": "{lightgray}",  "ansi": rgb(38, (187, 187, 187))},#"38;2;187;187;187m"},
{ "command": "{black}",      "ansi": rgb(38, (0,0,0))}, # "38;2;0;0;0m"},
{ "command": "{darkgreen}",  "ansi": darken(38, (0, 204, 85), 0.20)},#  "rgb": (0,183,76) } # darken("green", 0.10)
)

bgcolors = (
{ "command": "{bgwhite}",      "ansi": rgb(48, (255, 255, 255))},#"48;2;255;255;255m", "rgb": (255,255,255) }, # 37m
{ "command": "{bgred}",        "ansi": rgb(48, (136, 0, 0))},#"48;2;136;0;0m",     "rgb": (136,0,0) }, # 31m
{ "command": "{bgcyan}",       "ansi": rgb(48, (170, 255, 238))},#"48;2;170;255;238m", "rgb": (170,255,238) }, # 36m
{ "command": "{bgpurple}",     "ansi": rgb(48, (204, 68, 204))},#"48;2;204;68;204m",  "rgb": (204, 68, 204) }, # 35m
{ "command": "{bggreen}",      "ansi": rgb(48, (0, 204, 85))},#"48;2;0;204;85m",    "rgb": (0,204,85) }, # 32m
{ "command": "{bgblue}",       "ansi": rgb(48, (0, 0, 170))},#"48;2;0;0;170m",     "rgb": (0,0,170) }, # 34m
{ "command": "{bgyellow}",     "ansi": rgb(48, (238, 238, 119))},#"48;2;238;238;119m", "rgb": (238,238,119) }, # 33m
{ "command": "{bgorange}",     "ansi": rgb(48, (221, 136, 85))},#"48;2;221;136;85m",  "rgb": (221,136,85) },
{ "command": "{bgbrown}",      "ansi": rgb(48, (102, 68, 0))},#"48;2;102;68;0m",    "rgb": (102,68,0) },
{ "command": "{bglightred}",   "ansi": rgb(48, (255, 119, 119))},#"48;2;255;119;119m", "rgb": (255, 119, 119) },
{ "command": "{bgdarkgray}",   "ansi": rgb(48, (51, 51, 51))},#"48;2;51;51;51m",    "rgb": (51, 51, 51) },
{ "command": "{bggray}",       "ansi": rgb(48, (119, 119, 119))},#"48;2;119;119;119m", "rgb": (119, 119, 119) },
{ "command": "{bglightgreen}", "ansi": rgb(48, (170, 255, 102))},#"48;2;170;255;102m", "rgb": (170, 255, 102) },
{ "command": "{bglightblue}",  "ansi": rgb(48, (0, 136, 255))},#"48;2;0;136;255m",   "rgb": (0, 136, 255) },
{ "command": "{bglightgray}",  "ansi": rgb(48, (187, 187, 187))},#"48;2;187;187;187m", "rgb": (187, 187, 187) },
{ "command": "{bgblack}",      "ansi": rgb(48, (0,0,0)) }, # "48;2;0;0;0m",       "rgb": (0,0,0) }, # 30m
{ "command": "{bgdarkgreen}",  "ansi": darken(48, (0, 204, 85), 0.20) }, # "48;2;0;183;76m",  "rgb": (0,183,76) } # darken("green", 0.10)

)

# https://www.c64-wiki.com/wiki/Color
# https://en.wikipedia.org/wiki/ANSI_escape_code
echocommands = (
{ "command": "{clear}",      "ansi": "2J" },
{ "command": "{home}",       "ansi": "0;0H" },
# { "command": "{clreol}",     "ansi": "K" },
# { "command": "{/all}",       "ansi": "0;39;49m" },
{ "command": "{/fgcolor}",   "ansi": "39m" },
{ "command": "{/bgcolor}",   "ansi": "49m" },

#{ "command": "{savecursor}", "ansi": "s" },
#{ "command": "{restorecursor}", "ansi": "u" },

{ "command": "{bold}",       "ansi": "1m" },
{ "command": "{/bold}",      "ansi": "22m" },
{ "command": "{faint}",      "ansi": "2m" },
{ "command": "{italic}",     "ansi": "3m" },
{ "command": "{/italic}",    "ansi": "23m" },
{ "command": "{underline}",  "ansi": "4m" },
{ "command": "{/underline}", "ansi": "24m" },
{ "command": "{blink}",      "ansi": "5m" },
{ "command": "{/blink}",     "ansi": "25m" },

{ "command": "{strike}",     "ansi": "9m" },
{ "command": "{/strike}",    "ansi": "29m" },

{ "command": "{magenta}",    "ansi": "35m" },

{ "command": "{reverse}",    "ansi": "7m" },
{ "command": "{/reverse}",   "ansi": "27m" },

#{ "command": "{autowhite}",    "alias": "{bold}{white}"},
#{ "command": "{autored}",      "alias": "{bold}{red}"},
#{ "command": "{autocyan}",     "alias": "{bold}{cyan}"},
#{ "command": "{autopurple}",   "alias": "{bold}{purple}"},
#{ "command": "{autogreen}",    "alias": "{bold}{green}"},
#{ "command": "{autoblue}",     "alias": "{bold}{blue}"},
#{ "command": "{autoyellow}",   "alias": "{bold}{yellow}"},
#{ "command": "{autoorange}",   "alias": "{bold}{orange}"},
#{ "command": "{autobrown}",    "alias": "{bold}{brown}"},
#{ "command": "{autogray}",     "alias": "{bold}{gray}"}
# { "command": "{autoblack}",      "alias": "{gray}"}
)

acs = {
  "ULCORNER":"l",
  "LLCORNER":"m",
  "URCORNER":"k",
  "LRCORNER":"j",
  "LTEE":    "t",
  "RTEE":    "u",
  "BTEE":    "v",
  "TTEE":    "w",
  "HLINE":   "q",
  "VLINE":   "x",
  "PLUS":    "n",
  "S1":      "o",
  "S9":      "s",
  "DIAMOND": "`",
  "CKBOARD": "a",
  "DEGREE":  "f",
  "PLMINUS": "g",
  "BULLET":  "~",
  "LARROW":  ",",
  "RARROW":  "+",
  "DARROW":  ".",
  "UARROW":  "-",
  "BOARD":   "h",
  "LANTERN": "i",
#  "BLOCK":   "0",
}

variables = {}
variables["theanswer"] = 42 # @see https://hitchhikers.fandom.com/f/p/4400000000000039797
variables["engine.title.color"] = "{bggray}{white}"
variables["engine.title.hrcolor"] = "{darkgreen}"
variables["optioncolor"] = "{white}{bggray}"
variables["currentoptioncolor"] = "{bgwhite}{gray}"
variables["areacolor"] = "{bggray}{white}"
variables["engine.areacolor"] = "{bggray}{white}"
variables["promptcolor"] = "{/bgcolor}{lightgray}"
variables["inputcolor"] = "{/bgcolor}{green}"
variables["normalcolor"] = "{/bgcolor}{lightgray}"
variables["highlightcolor"] = "{green}"
variables["labelcolor"] = "{/bgcolor}{lightgray}"
variables["valuecolor"] = "{/bgcolor}{green}"
variables["hrcolor"] = "{/bgcolor}{gray}"
variables["acscolor"] = "{/bgcolor}{gray}" # @since 20220916
variables["sepcolor"] = "{lightgray}" # @since 20220924
# add 'engine.menu.resultfailedcolor'?

def setvariable(name:str, value):
#  print("setvariable.100: name=%r value=%r" % (name, value))
  variables[name] = value
  return

def getvariable(name:str):
#  print("getvariable.100: variables=%r" % (variables))
  if name in variables:
    return variables[name]
  return "NOTFOUND:%r" % (name)

def clearvariables():
  variables = {}
  return

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
    ("DECSTBM",    r'\{DECSTBM(:(\d{,3})(,(\d{,3}))?)?\}'),  # set top, bottom margin
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
#        print("kind=%r mo.groups()=%r" % (kind, mo.groups()))
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

        t = Token(kind, value)
        # print("yielding token %r" % (t,))
        yield t

def interpretecho(buf:str, width:int=None, strip:bool=False, wordwrap:bool=True, end:str="\n", args=Namespace(), indent:str="---") -> str:
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
          result += "\n"*int(v)+indent
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
            print("syntax error: %r" % (value))
            raise ValueError
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
            pos = len(indent)+len(token.value)
            result += indent+token.value
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
        result += CSI+"%dJ" % (token.value)
      elif token.type == "CURSORHPOS":
        result += CSI+"%dG" % (token.value)
#  print("result=%s" % (result))
  return result

# copied from bbsengine.py
def echo(buf:str="", interpret:bool=True, strip:bool=False, level:str=None, datestamp=False, end:str="\n", width:int=None, wordwrap=True, flush=False, args:object=Namespace(), indent=0, **kw):
  if width is None:
    width = getterminalwidth()

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

    buf = "%s %s %s" % (interpretecho(prefix), buf, interpretecho("{/all}"))
    interpret = False

  if interpret is True:
    try:
      buf = interpretecho(buf, strip=strip, width=width, end=end, wordwrap=wordwrap, args=args)
    except RecursionError:
      print("recursion error!")

  print(buf, end=end)

  if flush is True:
    sys.stdout.flush()

  return

def getcursorposition():
  fd = sys.stdin.fileno()
  oldtermios = termios.tcgetattr(fd)
  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)

  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  echo(CSI+"6n", end="", flush=True)
  buf = ""
  try:
    for x in range(0,10):
      ch = sys.stdin.read(1)
#      echo("ch=%r" % (ch))
      buf += ch
      if ch == "R":
        break
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldtermios)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

  m = re.search(r'\033\[(?P<row>\d{,4});(?P<col>\d{,4})R', buf)
  row, column = m.group("row"), m.group("col")
  return (int(row), int(column))

# @since 20210411
def getterminalsize():
  import shutil
  return shutil.get_terminal_size()

# http://www.brandonrubin.me/2014/03/18/python-snippet-get-terminal-width/
# https://www.programcreek.com/python/example/1922/termios.TIOCGWINSZ
def getterminalwidth():
  return getterminalsize().columns
  #try:
  #  res = os.get_terminal_size()
  #except:
  #  return 80
  #else:
  #  return res.columns
#  import subprocess
#
#  command = ['tput', 'cols']
#
#  if sys.stdout.isatty() is False:
#    return False

#  try:
#    width = int(subprocess.check_output(command))
#  except OSError as e:
#    print("Invalid Command '{0}': exit status ({1})".format(command[0], e.errno))
#    return False
#  except subprocess.CalledProcessError as e:
#    print("Command '{0}' returned non-zero exit status: ({1})".format(command, e.returncode))
#    return False
#  else:
#    return width

def getterminalheight():
  return getterminalsize().lines
#  if sys.stdout.isatty() is False:
#    return False
#
#  res = os.get_terminal_size()
#  return res.lines


# @see https://tldp.org/HOWTO/Xterm-Title-3.html
def xtname(name):
  if sys.stdout.isatty() is False:
    return False
  echo("\033]0;%s\007" % (name))
  return

# @see https://stackoverflow.com/questions/9043551/regex-that-matches-integers-only
def inputinteger(prompt, oldvalue=None, **kw) -> int:
  oldvalue = int(oldvalue) if oldvalue is not None else ""
  mask = kw["mask"] if "mask" in kw else r"^([+-]?[1-9]\d*|0)[ ,]?$"
  buf = inputstring(prompt, oldvalue, mask=mask, **kw)

  if buf is None or buf == "":
    return None
  
  print(f"type(buf)={type(buf)!r}")
  if type(buf) is list:
    res = []
    for b in buf:
      try:
        res.append(int(b))
      except:
        return
    echo("res={}".format(res))
    return res
  else:
    print("inputinteger.100: plain int, not a list")
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
def inputstring(prompt:str, oldvalue:str=None, **kw) -> str:
  import readline
  def preinputhook():
    # echo("preinputhook.100: trace")
    readline.insert_text(str(oldvalue))
    readline.redisplay()

  # echo("inputstring.100: oldvalue=%r" % (oldvalue))
  if oldvalue is not None:
    readline.set_pre_input_hook(preinputhook)

  inputfunc = input
  
  args = kw["args"] if "args" in kw else Namespace()

  mask = kw["mask"] if "mask" in kw else None

  returnseq = kw["returnseq"] if "returnseq" in kw else False

  multiple = kw["multiple"] if "multiple" in kw else None

  oldcompleter = readline.get_completer()
  completer = kw["completer"] if "completer" in kw else oldcompleter

  oldcompleterdelims = readline.get_completer_delims()

  completerdelims = kw["completerdelims"] if "completerdelims" in kw else readline.get_completer_delims()
  
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
    buf = inputfunc(interpretecho(prompt))

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


#    if callable(verify):
#      foo = [verify(args, f) for f in foo]

#    return foo
#    if multiple is True:
#      return foo
#    return completerdelims.join(foo)

# @see https://stackoverflow.com/a/53981846
# @deprecated
# moved to bbsengine5
def oxfordcomma(seq: List[Any], sepcolor:str="", itemcolor:str="") -> str:
    """Return a grammatically correct human readable string (with an Oxford comma)."""
    seq = [str(s) for s in seq]

    if len(seq) < 3:
      buf = "%s and %s" % (sepcolor, itemcolor)
      return itemcolor+buf.join(seq) # " and ".join(seq)

    buf = "%s, %s" % (sepcolor, itemcolor)
    return itemcolor+buf.join(seq[:-1]) + '%s, and %s' % (sepcolor, itemcolor) + seq[-1]
readablelist = oxfordcomma

# @since 20200917
def detectansi():
  if sys.stdout.isatty() is False:
    return False

  stdinfd = sys.stdin.fileno()
  stdoutfd = sys.stdout.fileno()

  oldtermios = termios.tcgetattr(stdinfd)
  oldflags = fcntl.fcntl(stdinfd, fcntl.F_GETFL)

  newattr = termios.tcgetattr(stdinfd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(stdinfd, termios.TCSANOW, newattr)

  # fcntl.fcntl(stdinfd, fcntl.F_SETFL, oldflags)

  echo(CSI+"5n")

  buf = ""
  try:
    for x in range(0, 4):
      ch = sys.stdin.read(1)
      buf += ch
      if ch == "n":
        break
  finally:
    termios.tcsetattr(stdinfd, termios.TCSAFLUSH, oldtermios)
    fcntl.fcntl(stdinfd, fcntl.F_SETFL, oldflags)
#  echo("buf=%r" % (buf))
  if buf == CSI+"0n":
    return True
  elif buf == CSI+"3n":
    return False
  else:
    return None


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

def ljust(buf, width, fillchar=" "):
  bufstripped = interpretecho(buf, strip=True)
  result = bufstripped.ljust(width, fillchar)
  result = result.replace(bufstripped, buf)
  return result

#def center(buf, width:int=None, fillchar:str=" "):
#  if width is None:
#    width = getterminalwidth()
#
#  buflen = len(interpretmci(buf, strip=True, width=width))
#  half = (width-buflen)//2 # ttyio.getterminalwidth()-2-l)//2
##  echo("ttyio5.center.100: buflen=%d half=%d width=%d" % (buflen, half, width))
#  if (width - buflen) % 2 == 0:
#    space = ""
#  else:
#    space = fillchar
#  return fillchar*half+buf+space+fillchar*half
#
#def ljust(buf:str, width:int=None, fillchar:str="*"):
#  if width is None:
#    width = getterminalwidth()
#  echo("width=%d" % (width), level="debug")
#  buflen = len(interpretmci(buf, strip=True))
#  echo("ttyio5.ljust.100: buflen=%d len(buf)=%d" % (buflen, len(buf)), level="debug")
#  buf += fillchar * (width - buflen)
#  echo("%r" % (buf))
#  return buf

if __name__ == "__main__":
  print(inputchar("[A, B, C, D]", "ABCD", None))
