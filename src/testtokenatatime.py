import ttyio5 as ttyio

buf = "{bell:3}{wait:50}"
for token in ttyio.interpretecho(buf):
    print(token, end="", flush=True)
print("** done **")
