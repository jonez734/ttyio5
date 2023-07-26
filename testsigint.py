import os
import time
import signal

import ttyio5 as ttyio

def handlesigint(signum, frame):
    print(f"received: {signum}")
    if signum == signal.SIGINT:
        raise KeyboardInterrupt

signal.signal(signal.SIGINT, handlesigint)

ch = ttyio.inputchar("prompt: ", "ABCDE", "")
