import ttyio5 as ttyio

buf = "ogun's links"
width = ttyio.getterminalwidth()-2
#print("buf=%r" % (buf))
ttyio.echo("%r" % (buf.center(width, "%")), wordwrap=False)

