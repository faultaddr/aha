#coding:utf-8
from distutils.core import setup
import py2exe
import sys
includes = ["encodings", "encodings.*"]
sys.argv.append("py2exe")
#options = {"py2exe":   { "bundle_files": 1 }
   #             }
setup(
      console = [{"script":'parse.py'}])