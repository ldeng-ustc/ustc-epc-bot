import os
import inspect
import json
import shutil
from argparse import ArgumentParser
from time import sleep
from bot import EPCBot

parser = ArgumentParser()
parser.add_argument('--no_graphic', action='store_true', help="run without graphic")
args = parser.parse_args()

if not args.no_graphic:
    from tkinter import *
    from gui import *
    root = Tk()
    GUI(root)
    root.mainloop()
else:
    work_dir = os.path.realpath(os.path.abspath(
            os.path.split(inspect.getfile(inspect.currentframe()))[0]
        ))
    config_dir = os.path.join(work_dir, "config.json")
    if not os.path.exists(config_dir):
        shutil.copy("config.template.json", "config.json")
    with open(config_dir, "r", encoding="utf-8") as config:
        config = json.load(config)
    bot = EPCBot(config)
    bot.start()
    while True:
        sleep(10)