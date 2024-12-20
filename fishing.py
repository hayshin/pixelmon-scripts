from control import *
from system import get_minecraft_window
from counter import count

fishing_window = {"top": 700, "left": 1400, "width": 200, "height": 150}

def lure():
    get_minecraft_window().set_focus()
    click(rmb)

def cancel_lure():
    get_minecraft_window().set_focus()
    press("2")
    press("1")
    click(rmb)
    sleep(0.3)

def handle_lure(lure_quality):
    if lure_quality > 0:
        print(lure_quality)
    if lure_quality == 3:
        lure()
        cancel_lure()
        count("3")
    elif lure_quality == 2:
        cancel_lure()
        count("2")
    elif lure_quality == 1:
        cancel_lure()
        count("1")