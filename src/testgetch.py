import ttyio5 as ttyio

loop = True
while loop:
    ch = ttyio.getch()
    if ch == "KEY_ENTER":
        loop = False
    else:
        print(repr(ch))

