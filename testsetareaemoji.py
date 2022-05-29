# @since 20220329 for the moment, setarea() using emojis does not work
import re
import sys

import ttyio5 as ttyio
import bbsengine5 as bbsengine

#bbsengine.setarea(":smile: ballot box")

tests = ("grin", "sun", "ballot-box", "wood", "link", "anchor", "fire")

#bbsengine.initscreen(bottommargin=1)

#buf = ":fire: ballot box"
#v = ttyio.emoji["anchor"] if "anchor" in ttyio.emoji else ""
# v = ttyio.emoji["smile"] if "smile" in ttyio.emoji else ""
#terminalwidth = ttyio.getterminalwidth()-2

#buf = ":ballot-box: ballot box emoji"
#ttyio.echo(ttyio.center(buf, fillchar="*"), wordwrap=False)
#for t in tests:
#  v = ttyio.emoji[t] if t in ttyio.emoji else ""
#  enc = v.encode("UTF-8")
#  print("%s: %s %d" % (t, enc, len(enc)))
#  ttyio.echo("{bggray}"+ttyio.ljust(buf, terminalwidth)+"{/all}", wordwrap=False)
#  if ttyio.inputboolean("continue? [Yn]: ", "Y") is False:
#    break
#  buf = "%s %s" % (v, t)
#  if m is not None:
#	pass

#bbsengine.setarea(buf)
#bbsengine.title(buf)

#        if token.value in emoji:
#          if re.compile(r'[\U00010000-\U0001FFFF]').match(emoji[token.value]) is not None:
#            result += "*"

#print(ttyio.emoji)
#width = ttyio.getterminalwidth()-2

# rightbuf = ":person: jonez :anchor: 42 coins"
rightbuf = "login: jonez coins: 42!"

ttyio.echo("*warning*, cannot yet use emojis in setarea() calls", level="warn")

bbsengine.setarea("testing plain text rightbuf", rightbuf)
if ttyio.inputboolean("continue? [Yn]: ", "Y", "YN") is False:
    sys.exit(0)

for k, v in ttyio.emoji.items():
    print(k, v)
    # these items do not play well with ljust() and center()
    if k in ("sun", "ballot-box", "thunder-cloud-and-rain"):
        continue
    emoji = ttyio.emoji[k]
    if type(emoji) == tuple:
        buf = "%s%s-%s" % (emoji[0], emoji[1], k)
    else:
        buf = "%s-%s" % (emoji, k)
#    print(buf)
#    ttyio.ljust(buf, 80, fillchar="*")
#    ttyio.echo("{/all}{var:engine.title.hrcolor}{acs:ulcorner}{acs:hline:%s}{acs:urcorner}" % (width), wordwrap=False)
#    ttyio.echo("{var:engine.title.hrcolor}{acs:vline}{/all}{var:engine.title.color}%s{/all}{var:engine.title.hrcolor}{acs:vline}{/all}" % (ttyio.center(buf, width)), wordwrap=False)
#    ttyio.echo("{acs:vline}{bggray}"+ttyio.center(buf, 80, fillchar="*")+"{/all}{acs:vline}")
#    print(ttyio.center(buf, width=80, fillchar="*"))
    bbsengine.setarea(buf, rightbuf)
    if ttyio.inputboolean("continue? [Yn]: ", "Y", "YN") is False:
        break
