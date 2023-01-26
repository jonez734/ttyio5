import re
import sys
import fcntl
import termios

from .constants import *

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

  print(CSI+"5n")

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
  if buf == CSI+"0n":
    return True
  elif buf == CSI+"3n":
    return False
  else:
    return None

def getcursorposition():
  fd = sys.stdin.fileno()
  oldtermios = termios.tcgetattr(fd)
  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)

  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)

  print(CSI+"6n", end="", flush=True)
  buf = ""
  try:
    for x in range(0,10):
      ch = sys.stdin.read(1)
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
  print(f"{ESC}]0;{name}\007", end="", flush=True)
  return
