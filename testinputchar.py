import ttyio5 as ttyio

ch = ttyio.inputchar("testinputchar [ABCDEQ]: ", "ABCDEQ", "Q")
if ch == "A":
    ttyio.echo("alpha")
elif ch == "B":
    ttyio.echo("bravo")
else:
    print(ch)
