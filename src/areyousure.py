import sys
import ttyio5 as ttyio

res = ttyio.inputboolean("{var:promptcolor}are you sure? {var:optioncolor}[yN]{var:promptcolor}: {var:inputcolor}", "N")
ttyio.echo("{/all}")
if res is True:
    sys.exit(0)

sys.exit(1)
