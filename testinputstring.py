import ttyio5 as ttyio

origvalue = 42
buf = ttyio.inputstring("prompt: ", origvalue, multiple=True)
print(buf)
