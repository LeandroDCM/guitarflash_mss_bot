
import cv2
from PIL import ImageGrab
import numpy as np
import keyboard
import time
from config import *

class Object:
    def __init__(self, path):
        img = cv2.imread(path, 0)
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.locations = []  # To store all matched locations

    def match(self, scr, threshold = 0.8, scale=1.0):
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
    if (note == "Yellow Star"):
        time.sleep(0.2)
        print(f"Pressing {note} at location {location}")
        keyboard.press(key)
        time.sleep(0.1)
        keyboard.release(key)
        time.sleep(0.2)
    else:
        time.sleep(delay)
        print(f"Pressing {note} at location {location}")
        keyboard.press(key)
        keyboard.release(key)
    
def hitboxDrawing(img, noteType='normal', active=False ):
    if active and noteType == "normal":
        cv2.rectangle(img, (notePP["gHor"], notePP["v"]), (notePP["gHorFinish"], notePP["vFinish"]), colors['green'], 3) #Green
        cv2.rectangle(img, (notePP["rHor"], notePP["v"]), (notePP["rHorFinish"], notePP["vFinish"]), colors['red'], 3) #Red
        cv2.rectangle(img, (notePP["yHor"], notePP["v"]), (notePP["yHorFinish"], notePP["vFinish"]), colors['yellow'], 3) #Yellow
        cv2.rectangle(img, (notePP["bHor"], notePP["v"]), (notePP["bHorFinish"], notePP["vFinish"]), colors['blue'], 3) #Blue
        cv2.rectangle(img, (notePP["oHor"], notePP["v"]), (notePP["oHorFinish"], notePP["vFinish"]), colors['orange'], 3) #Orange

    if active and noteType == "special":
        cv2.rectangle(img, (sNotePP["gHor"], sNotePP["v"]), (sNotePP["gHorFinish"], sNotePP["vFinish"]), colors['green'], 3) #Green
        cv2.rectangle(img, (sNotePP["rHor"], sNotePP["v"]), (sNotePP["rHorFinish"], sNotePP["vFinish"]), colors['red'], 3) #Red
        cv2.rectangle(img, (sNotePP["yHor"], sNotePP["v"]), (sNotePP["yHorFinish"], sNotePP["vFinish"]), colors['yellow'], 3) #Yellow
        cv2.rectangle(img, (sNotePP["bHor"], sNotePP["v"]), (sNotePP["bHorFinish"], sNotePP["vFinish"]), colors['blue'], 3) #Blue
        cv2.rectangle(img, (sNotePP["oHor"], sNotePP["v"]), (sNotePP["oHorFinish"], sNotePP["vFinish"]), colors['orange'], 3) #Orange


# def pressDrawing(img, note, active=False):
#     print("here")
#     if active:
#         print("here2")
#         if note == "Green":
#             print("here3")
#             cv2.rectangle(img, (notePP["gHor"] - 20, notePP["v"]), (notePP["gHor"] - 10, notePP["vFinish"] - 40), (0,255,0), 5) #Green

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