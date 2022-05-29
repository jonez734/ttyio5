import ttyio5 as ttyio
import bbsengine5 as bbsengine

ttyio.echo("{inviscursor}foo bar baz")
ttyio.inputchar("hit space: ", " ")
ttyio.echo("{viscursor}")
ttyio.inputchar("hit space: ", " ")


