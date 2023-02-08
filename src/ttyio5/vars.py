variables = {}
variables["theanswer"] = 42 # @see https://en.wikipedia.org/wiki/42
variables["engine.title.color"] = "{bggray}{white}"
variables["engine.title.hrcolor"] = "{darkgreen}"
variables["optioncolor"] = "{white}{bggray}"
variables["currentoptioncolor"] = "{bgwhite}{gray}"
variables["areacolor"] = "{bggray}{white}"
variables["engine.areacolor"] = "{bggray}{white}"
variables["promptcolor"] = "{/bgcolor}{lightgray}"
variables["inputcolor"] = "{/bgcolor}{green}"
variables["normalcolor"] = "{/bgcolor}{lightgray}"
variables["highlightcolor"] = "{green}"
variables["labelcolor"] = "{/bgcolor}{lightgray}"
variables["valuecolor"] = "{/bgcolor}{green}"
variables["hrcolor"] = "{/bgcolor}{gray}"
variables["acscolor"] = "{/bgcolor}{gray}" # @since 20220916
variables["sepcolor"] = "{lightgray}" # @since 20220924
# add 'engine.menu.resultfailedcolor'?

def setvariable(name:str, value):
#  print("setvariable.100: name=%r value=%r" % (name, value))
  variables[name] = value
  return

def getvariable(name:str):
#  print("getvariable.100: variables=%r" % (variables))
  if name in variables:
    return variables[name]
  return "NOTFOUND:%r" % (name)

def clearvariables():
  variables = {}
  return
