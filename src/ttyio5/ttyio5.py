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

# @since 20230101
# copied from cmd2, removed handling other than GNU readline
def rl_escape_prompt(prompt: str) -> str:
    """Overcome bug in GNU Readline in relation to calculation of prompt length in presence of ANSI escape codes

    :param prompt: original prompt
    :return: prompt safe to pass to GNU Readline
    """
    # start code to tell GNU Readline about beginning of invisible characters
    escape_start = "\x01"

    # end code to tell GNU Readline about end of invisible characters
    escape_end = "\x02"

    escaped = False
    result = ""

    for c in prompt:
        if c == "\x1b" and not escaped:
            result += escape_start + c
            escaped = True
        elif c.isalpha() and escaped:
            result += c + escape_end
            escaped = False
        else:
            result += c

        return result

# @since 20230101
# copied from cmd2
def rl_unescape_prompt(prompt: str) -> str:
    """Remove escape characters from a Readline prompt"""
    escape_start = "\x01"
    escape_end = "\x02"
    prompt = prompt.replace(escape_start, "").replace(escape_end, "")
    return prompt

if __name__ == "__main__":
  print(inputchar("[A, B, C, D]", "ABCD", None))
