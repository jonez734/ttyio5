#!/usr/bin/env python3

# from setuptools import setup
from setuptools import setup

import sys
import time

#print("no.")
#sys.exit(-1)

r = 1
v = time.strftime("%Y%m%d%H%M")

projectname = "ttyio5"

setup(
  name=projectname,
  version=v,
  url="http://repo.zoidtechnologies.com/%s/" % (projectname),
  author="zoidtechnologies.com",
  author_email="%s@projects.zoidtechnologies.com" % (projectname),
  py_modules=["areyousure"],
  requires=[],
  scripts=["../bin/areyousure"],
  license="GPLv3",
  provides=[projectname],
  classifiers=[
    "Programming Language :: Python :: 3.9",
    "Environment :: Console",
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Operating System :: POSIX",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Terminals",
  ],
  long_description = """terminal input and output functions.""",
  packages=["ttyio5"],

  command_options = {
    "build_sphinx": {
      "project": projectname,
      "version": v,
      "release": r,
      "source_dir": ( "setup.py", "doc/" )
    }
  }
)
