import ttyio5 as ttyio

class Completer:
    def __init__(self, args=None):
        self.args = args
        self.results = []

    def build(self):
        return ["open", "done", "disco"]
    
    def complete(self, word, state):
        self.results = [x for x in self.build() if x is not None and x.startswith(word)]
#        ttyio.echo(f"self.results={self.results!r} state={state!r}", level="debug")
        return self.results

def main(args=None, **kw):
    print(repr(ttyio.inputstring("tab complete test: ", completerclass=Completer, style="ttyio")))

if __name__ == "__main__":
    main()
