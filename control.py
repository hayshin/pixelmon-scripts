import random

import keyboard
import mouse
from time import sleep
rmb = "right"
lmb = "left"

def random_sleep(start, end):
    sleep(random.uniform(start, end))

def click(button):
    mouse.click(button)
    sleep(0.05)

def press(button):
    keyboard.send(button)
    random_sleep(0.05, 0.1)
