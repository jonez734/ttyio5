import bbsengine5 as bbsengine
import ttyio5 as ttyio

for k, v in ttyio.emoji.items():
    label = k
    if type(v) == tuple:
        value = v[0]
        spaces = v[1]
    elif type(v) == str:
        value = v
        spaces = ""
    buf = "%s: %s %d" % (label, value, len(spaces))
#    ttyio.echo(buf)
    ttyio.echo(ttyio.ljust(buf, fillchar="*"))
