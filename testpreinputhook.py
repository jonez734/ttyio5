from ttyio5 import echo, inputstring

#oldvalue = [ 42, 10, 7704 ]
oldvalue = "thhgttg"
#echo(f"inputstring.preinputhook.100: oldvalue={oldvalue!r}", level="debug")
#if type(oldvalue) is list:
#  for i in range(len(oldvalue)):
#    oldvalue[i] = str(oldvalue[i])
#  oldvalue = ", ".join(oldvalue)
#echo(f"inputstring.preinputhook.120: oldvalue={oldvalue!r}", level="debug")

print(inputstring("prompt here: ", oldvalue, multiple=False))

