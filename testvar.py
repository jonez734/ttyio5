import ttyio5 as ttyio

#ttyio.setvariable("foo", "{var:color}")
ttyio.setvariable("color", "{green}")
ttyio.setvariable("menu.test", "{var:color}eggs")
print(ttyio.getvariable("menu.test"))
buf = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. {var:menu.test}{/all}At elementum eu facilisis sed odio morbi. Interdum consectetur libero id faucibus nisl tincidunt eget nullam. Nunc mattis enim ut tellus. Faucibus purus in massa tempor nec feugiat. Diam phasellus vestibulum lorem sed risus ultricies tristique. Euismod quis viverra nibh cras. Amet massa vitae tortor condimentum lacinia. Eu scelerisque felis imperdiet proin. Mauris pellentesque pulvinar pellentesque habitant morbi tristique senectus. Eleifend quam adipiscing vitae proin sagittis. Mattis vulputate enim nulla aliquet porttitor lacus. Neque aliquam vestibulum morbi blandit. Nisi porta lorem mollis aliquam ut porttitor.
"""

ttyio.echo(buf, wordwrap=True)
