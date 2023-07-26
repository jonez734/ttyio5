import argparse

import ttyio5 as ttyio
import bbsengine5 as bbsengine

def init(args=None, **kw):
    return True

def buildargs(args=None, **kw):
    parser = argparse.ArgumentParser("ttyio5.testnocolor")
    parser.add_argument("--verbose", action="store_true", dest="verbose")
    parser.add_argument("--debug", action="store_true", dest="debug")
    parser.add_argument("--no-color", action="store_false", dest="color")

    return parser
    
def main(args, **kw):
    if args is not None and "debug" in args and args.debug is True:
        ttyio.echo(f"empyre.main.100: args={args!r}", level="debug")

    ttyio.setechoarg("color", False)
#    ttyio.echo("{yellow}no color{/all}")
    bbsengine.title("test title here")

if __name__ == "__main__":
    parser = buildargs()
    args = parser.parse_args()

    init(args)

    try:
        main(args)
    except KeyboardInterrupt:
        ttyio.echo("{/all}{bold}INTR{bold}")
    except EOFError:
        ttyio.echo("{/all}{bold}EOF{/bold}")
    finally:
        ttyio.echo("{decsc}{curpos:%d,0}{el}{decrc}{reset}{/all}" % (ttyio.getterminalheight()))
