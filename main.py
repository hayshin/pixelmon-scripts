import enum
from collections import deque
from typing import List

import cv2
from control import *
import numpy as np
from mss import mss
from fishing import lure, handle_lure

# monitor = {"top": 400, "left": 860, "width": 200, "height": 150} # по середине


def num_of_islands(grid: List[List[bool]]) -> int:
    if not grid:
        return 0

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    num_islands = 0

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]:
                num_islands += 1
                queue = deque([(i, j)])
                while queue:
                    x, y = queue.popleft()
                    if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y]:
                        grid[x][y] = False
                        for dx, dy in directions:
                            queue.append((x + dx, y + dy))

    return num_islands


class Color(enum.Enum):
    BLUE = 0
    GREEN = 1
    RED = 2


def filter_image(np_image, color_to_filter):
    pixels = np_image[:, :, color_to_filter.value] > 10
    for color in Color:
        if color != color_to_filter:
            pixels &= (np_image[:, :, color.value] == 0)



def get_number_of_red_squares_and_image(np_image, red_threshold=100, green_threshold=1, blue_threshold=1):
    red_pixels = (np_image[:, :, 2] > 100) & \
                 (np_image[:, :, 1] == 0) & \
                 (np_image[:, :, 0] == 0)

    num_of_squares = num_of_islands(red_pixels.tolist())

    # Create an output image where red pixels are highlighted in bright red
    gray_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2GRAY)

    # Convert the grayscale image back to BGR so it can be combined with the red pixels
    gray_bgr_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
    # Combine the red pixels with the grayscale image
    combined_image = np.where(np.expand_dims(red_pixels, axis=-1), np_image, gray_bgr_image)
    return num_of_squares, combined_image


isWorking = False


def on_right_shift(key):
    global isWorking
    isWorking ^= True
    print(f"Switching to {isWorking}")
    lure()


keyboard.on_release_key('right shift', on_right_shift)

size_for_fishing = (1400, 700, 1400 + 200, 700 + 150)
size_of_minecraft = ()

while True:
    with mss() as sct:
        while isWorking:
            screenshot = sct.grab(monitor)

            np_image = np.array(screenshot)
            if np_image.shape[2] == 4:  # Check if image has 4 channels (RGBA)
                np_image = cv2.cvtColor(np_image, cv2.COLOR_BGRA2BGR)

            # image = image.crop(box = (   1400,700, 1400+200, 700+150))

            num_of_squares, processed_image = get_number_of_red_squares_and_image(np_image)

            cv2.imshow('Red Pixels Highlighted - Others Gray', processed_image)
            handle_lure(num_of_squares)

            sleep(0.05)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
