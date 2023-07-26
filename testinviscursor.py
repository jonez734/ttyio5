import ttyio5 as ttyio
import bbsengine5 as bbsengine

ttyio.echo("{hidecursor}foo bar baz")
ttyio.inputchar("hit space: ", " ")
ttyio.echo("{showcursor}")
ttyio.inputchar("hit space: ", " ")


