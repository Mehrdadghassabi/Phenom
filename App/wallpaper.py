from gi.repository import Gio
import glob
from random import randint
import os

directory=os.path.dirname(os.path.realpath(__file__))
wallpapers=glob.glob("wallpapers/*")
x=randint(0,len(wallpapers)-1)

SCHEMA='org.gnome.desktop.background'
KEY='picture-uri'
gsetting=Gio.Settings.new(SCHEMA)
background=directory+"/"+wallpapers[x]
gsetting.set_string(KEY,"file://"+background)