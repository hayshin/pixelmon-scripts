
import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def crop_image(np_image, left, top, width, height):
    return np_image[top:top+height, left:left+width]

def filter_image_for_gray(np_image):
    pixels = (np_image[:, :, 0] < 10) & \
             (np_image[:, :, 1] < 10) & \
             (np_image[:, :, 2] < 10)
    result_image = np.full_like(np_image, [255, 255, 255])  #
    result_image[pixels] = [0, 0, 0]

    return result_image

def filter_image_for_white(np_image):
    pixels = (np_image[:, :, 0] > 200) & \
             (np_image[:, :, 1] > 200) & \
             (np_image[:, :, 2] > 200)
    result_image = np.full_like(np_image, [255, 255, 255])  #
    result_image[pixels] = [0, 0, 0]

    return result_image

def filter_image_for_green(np_image):
    pixels = (np_image[:, :, 0] < 5) & \
             (np_image[:, :, 1] > 100) & \
             (np_image[:, :, 2] < 5)
    result_image = np.zeros_like(np_image)

    result_image[pixels] = [255, 255, 255]

    return result_image


def decrease_size_of_image(np_image, scale):
    height, width = np_image.shape[0], np_image.shape[1]
    return cv2.resize(np_image, (width // scale, height // scale), interpolation=cv2.INTER_NEAREST)
def increase_size_of_image(np_image, scale):
    height, width = np_image.shape[0], np_image.shape[1]
    return cv2.resize(np_image, (width * scale, height * scale), interpolation=cv2.INTER_NEAREST)

def get_text_from_image(np_image):
    text = pytesseract.image_to_string(np_image)
    return text

def transform_np_array_to_bits(np_array):
    height, width, channels = np_array.shape
    new_array = np.zeros((height, width), dtype=np.uint8)
    for y in range(0, height):
        for x in range(0, width):
            if np_array[0, 0].any():
                new_array[y, x] = 1  # Set the pixel in the new image to 1
            else:
                new_array[y, x] = 0  # Set it to 0 if the block is not uniform
    return new_array