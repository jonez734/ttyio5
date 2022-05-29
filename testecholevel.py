#!/usr/bin/env python

import ttyio5 as ttyio

ttyio.echo("{foo bar baz}", level="warn")
ttyio.echo("{foo bar baz}", level="error")
ttyio.echo("{blink}{foo bar baz}{/all}", level="debug")
ttyio.echo("{bold}bold!{/bold}", level="debug")
ttyio.echo("{bold}bold! 2{/bold}")



