import asyncio
import ttyio5 as ttyio

def foo():
    ch = ttyio.inputchar("prompt: ", "YN", "")

def main():
    foo()

if __name__ == "__main__":
    try:
        main()
    except EOFError:
        ttyio.echo("EOF")
    except KeyboardInterrupt:
        ttyio.echo("INTR")


