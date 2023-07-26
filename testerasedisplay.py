import ttyio5 as ttyio
import bbsengine5 as bbsengine

# ttyio.echo("{cursordown:3}")

ttyio.echo("{f6:3}{cursorup:3}") # curpos:%d,0}" % (ttyio.getterminalheight()-3))
bbsengine.initscreen(bottommargin=1)
bbsengine.setarea("1st")

height = ttyio.getterminalheight()

loremipsum = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Amet consectetur adipiscing elit duis tristique sollicitudin nibh sit. Tortor aliquam nulla facilisi cras fermentum odio eu feugiat pretium. Vitae nunc sed velit dignissim sodales ut eu sem integer. Ac felis donec et odio pellentesque.
"""
for x in range(0, 20):
    ttyio.echo(loremipsum)
ttyio.inputboolean("ready?")
#ttyio.echo("{home}{cursordown:10}")
ttyio.echo("{home}{sc}{curpos:%d,1}{ed:totop}{rc}foo bar baz" % (height-1))
bbsengine.setarea("2nd")
