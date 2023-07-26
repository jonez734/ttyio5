import ttyio5 as ttyio

buf = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur a tristique ante. Cras posuere augue orci, et porta massa feugiat ultricies. Proin at massa ac risus tempor volutpat. Morbi porttitor eu lectus mattis porta. Vestibulum pellentesque accumsan tellus eu semper. Vivamus accumsan pretium urna, varius elementum mauris sagittis at. Vestibulum eleifend, dolor id ultricies vehicula, quam ligula interdum diam, ut consectetur tortor orci sed nulla. Donec a urna vel magna consequat mattis et quis justo. Vestibulum suscipit tempus venenatis."

width = 80
indent = (ttyio.getterminalwidth()-width)/2
ttyio.echo(buf, width=width, indent="*"*int(indent))
