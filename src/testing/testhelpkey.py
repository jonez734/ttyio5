import ttyio5 as ttyio

#def help():
#    ttyio.echo("help text {f6}here")

help = "static help text"

ch = ttyio.inputchar("test help key (F1): ", "ABC", noneok=True, help=help)
ttyio.echo("{/all}")

