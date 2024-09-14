
import cv2
from PIL import ImageGrab
import numpy as np
import keyboard
import time

class Object:
    def __init__(self, path):
        img = cv2.imread(path, 0)
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.locations = []  # To store all matched locations

    def match(self, scr, scale=1.0):
        if scale != 1.0:
            resized_img = cv2.resize(self.img, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
            res = cv2.matchTemplate(scr, resized_img, cv2.TM_CCOEFF_NORMED)
            template_width = resized_img.shape[1]
            template_height = resized_img.shape[0]
        else:
            res = cv2.matchTemplate(scr, self.img, cv2.TM_CCOEFF_NORMED)
            template_width = self.width
            template_height = self.height

        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        self.locations = []  # Clear previous locations

        # Store multiple matches if the value is greater than the threshold
        threshold = 0.8
        locs = np.where(res >= threshold)
        for pt in zip(*locs[::-1]):  # Switch x and y axis
            startLoc = pt
            endLoc = (startLoc[0] + template_width, startLoc[1] + template_height)
            self.locations.append((startLoc, endLoc))

        return len(self.locations) > 0

def grabScreen(bbox=None):
    img = ImageGrab.grab(bbox=(bbox))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def press_key(key, delay,note,location):
    print(f"Pressing {note} at location {location}")
    if (note == "Yellow Star"):
        time.sleep(0.2)
        keyboard.press(key)
        time.sleep(0.1)
        keyboard.release(key)
        time.sleep(0.2)
    else:
        time.sleep(delay)
        keyboard.press(key)
        keyboard.release(key)

# while 1:
#     img = grabScreen()
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     if note.match(img):
#         topleft_x = int(note.location[0][0] - note.width)
#         topleft_y = int(note.location[0][1] - 3 * note.height)
#         bottomRight_x = int(note.location[1][0] + 14 * note.width)
#         bottomRight_y = int(note.location[1][1] + 0.5 * note.height)
#         screenStart = (810, 700)
#         screenEnd = (500, 211)
#         print(topleft_x, topleft_y, bottomRight_x, bottomRight_y)
#         break