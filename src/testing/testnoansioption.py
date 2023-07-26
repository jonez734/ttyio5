import ttyio5

buf = ":smile: {acs:hline:10}{red}red fish {blue}blue fish {orange}1 fish{/all}{f6:4}--{cursorup:3}!!"

ttyio5.setoption("style", "noansi")
ttyio5.echo(buf)
