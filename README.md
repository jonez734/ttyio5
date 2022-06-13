# ttyio5
# compatible w bbsengine5

- [non blocking read from stdin in python](https://repolinux.wordpress.com/2012/10/09/non-blocking-read-from-stdin-in-python/)
- [twisted how to close a blocking socket while it is waiting to receive data?](https://www.py4u.net/discuss/208507)
- [Timeout on subprocess readline in Python](https://stackoverflow.com/questions/10756383/timeout-on-subprocess-readline-in-python)
- {cursordown} is working, but if the cursor is on the last line of the screen, it is ignored. ref: https://sites.google.com/a/dee.ufcg.edu.br/rrbrandt/en/docs/ansi/cursor
- [x] ttyio.setvariable() is not working and/or echo() does not properly resolve vars.
- [x] add {darkgreen} and {bgdarkgreen}
- [x] add rgb()
- [x] add darken()
- [ ] add lighten()
- (prompt_toolkit)[https://github.com/prompt-toolkit/python-prompt-toolkit]
- (position of cursor)[https://stackoverflow.com/questions/8343250/how-can-i-get-position-of-cursor-in-terminal]
- (python prompt toolkit)[https://github.com/prompt-toolkit/python-prompt-toolkit]
- (asyncio eventloop scheduling callbacks)[https://docs.python.org/3/library/asyncio-eventloop.html#scheduling-callbacks]
- [ ] add REPAINT to inputstring()
- https://unicode-table.com/en/1F5DA/
- https://altcodeunicode.com/alt-codes-die-checkers-shogi-symbols/
- great that there are unicode chars for dice, but they are too small to be useful, and the "increase font size" unicode does not work.
- {var:engine.menu.*}
- {var:engine.title.*}
- readline
    * per my research into gnu readline, it has a way to do a cb_linehandler. python version does not in order to be usable with libedit (bsd).
    * https://tiswww.case.edu/php/chet/readline/readline.html
    * this might allow an 'idle timer' to be implemented
- in most cases, replace \n w a " " so word wrap works properly. key is to replace "some" \n w ""
- check for {f6} followed by a single space?
- paragraphs look wrong with a preceeding space
- \n is replaced with " "
- NONWHITESPACE (command or alpha numeric) followed by WHITESPACE followed by {f6} should be filtered
- skip optimizing {f6:2}{f6} for now
- optimize {nonwhitespace}{whitespace*n}{f6} to remove whitespace tokens
- [ ] add {engine.areacolor} to list of default variables (@since 20211123 @done 20211123)
- [ ] accept boolean values in inputboolean() (do not call upper()) (@since 20211126)
- [ ] ttyio.echo(": foo :") yields incorrect results. print() works. (@since 20211216)
- [ ] https://stackoverflow.com/questions/3065116/get-the-text-in-the-display-with-ncurses

```[~/<1>cmd2-2.3.3/cmd2] [7:52pm] [jam@cyclops] % python
Python 3.10.1 (main, Jan 10 2022, 00:00:00) [GCC 11.2.1 20211203 (Red Hat 11.2.1-7)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> readline_lib = ctypes.CDLL(readline.__file__)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'ctypes' is not defined. Did you mean: 'type'?
>>> import ctypes
>>> readline_lib = ctypes.CDLL(readline.__file__)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'readline' is not defined
>>> import readline
>>> readline_lib = ctypes.CDLL(readline.__file__)
>>> readline_lib
<CDLL '/usr/lib64/python3.10/lib-dynload/readline.cpython-310-x86_64-linux-gnu.so', handle 55930a5c0de0 at 0x7fb0c2f89c30>
>>> display_fixed = ctypes.c_int.in_dll(readline_lib, "rl_display_fixed")
>>> display_fixed
c_int(1)
>>> encoded_prompt = ctypes.c_char_p.in_dll(readline_lib, "rl_prompt").value
>>> encoded_prompt
b'>>> '
>>>
```
- [ ] make a way to idle out a port during inputstring(), inputchar(), etc (@since 20220124)
- [ ] send notify messages async during inputstring(), inputchar(), etc (@since 20220124)
- https://docs.python.org/3/library/asyncio-sync.html#asyncio-sync
- https://www.google.com/search?q=python3+ctypes&oq=python3+ctypes&aqs=chrome.0.0i512j0i10i433j0i10l8.3475j0j7&sourceid=chrome&ie=UTF-8
- https://pgi-jcns.fz-juelich.de/portal/pages/using-c-from-python.html
- https://stackoverflow.com/questions/5081875/ctypes-beginner
- https://docs.python.org/3/library/threading.html
- emoji: https://emojipedia.org/fire/
- https://emojipedia.org/bank/
- [ ] when stripping, replace emjois with a single space instead of empty (@since 20220222)
- [ ] some emojis take more space in others :ballot-box: leaves a gap on the right of 9 spaces, but :smile: only has 4 spaces. empyre works fine. (@since 20220302)
- move ljust() and center() from bbsengine5 (@since 20220303)
- https://www.google.com/search?q=python+how+to+center+a+unicode+string&oq=python+how+to+center+a+unicode+string&aqs=chrome..69i57j33i22i29i30l9.4948j0j7&sourceid=chrome&ie=UTF-8
- https://stackoverflow.com/questions/33140370/using-format-to-fill-and-justify-multi-byte-unicode-strings-in-python-2-7
- https://stackoverflow.com/questions/tagged/unicode
- https://bytes.com/topic/python/answers/518298-how-get-size-unicode-string-string-bytes
- https://bugs.python.org/issue3446 - center, ljust and rjust are inconsistent with unicode parameters
- https://localcoder.org/python-ctypes-pass-argument-by-reference-error
- to improve performance when using a mask, turn off echo of the tty and only print the mask char?
- https://eli.thegreenplace.net/2016/basics-of-using-the-readline-library/
- [ ] if a line consists only of \n, replace it w {f6} or {f6:2}?(@since 20220523)
- [ ] within a paragraph, replace \n with a space (@since 20220528)
- [x] if a level is specified to echo(), color changes at beginning and end work, with 'interpret=False' for the buf (@since 20220302 @done 20220523)
- https://blog.prototypr.io/basic-ui-color-guide-7612075cc71a
- (https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)[ANSI Escape Sequences]
- (https://stackoverflow.com/questions/52472435/why-doesnt-git-natively-support-utf-16)[Why doesn't Git natively support UTF-16?]
- https://stackoverflow.com/questions/17894168/python-input-and-output-threading
- https://stackoverflow.com/questions/46751725/input-and-print-thread-python
- [ ] cursorinvis: ESC[?25l cursorvis: ESC[?25h (@since 20220528)
- https://www.pythontutorial.net/advanced-python/python-threading/

- https://www.pythontutorial.net/advanced-python/python-threading/
- https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
- https://invisible-island.net/xterm/ctlseqs/ctlseqs.html#h3-X10-compatibility-mode
- https://bluesock.org/~willkg/dev/ansi.html
- https://blog.prototypr.io/basic-ui-color-guide-7612075cc71a
- [ ] fix recursion depth in {var} handling (@since 20220606)
