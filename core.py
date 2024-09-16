import cv2
from PIL import ImageGrab
import numpy as np
import keyboard
import time
import threading
from config import *

class Object:
    def __init__(self, path):
        img = cv2.imread(path, 0)
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.locations = []  # To store all matched locations

    def match(self, scr, threshold=0.8, scale=1.0):
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

# Dictionary to track the last press time for each key
last_press_times = {
    "a": 0,  # Green
    "s": 0,  # Red
    "j": 0,  # Yellow
    "k": 0,  # Blue
    "l": 0   # Orange
}

# Define the cooldown period (in seconds)
cooldown_period = 0.02  # Adjust this value as needed

# Lock for thread safety
cooldown_lock = threading.Lock()

def press_key(key, delay, note, locationH, locationV, addDelay=False):
    global last_press_times
    
    current_time = time.time()

    with cooldown_lock:
        # Calculate the time since the last press for this key
        time_since_last_press = current_time - last_press_times[key]

        # Check if enough time has passed (cooldown)
        if time_since_last_press < cooldown_period:
            print(f"Skipped pressing {note} ({key}) due to cooldown. Last press was {time_since_last_press:.3f} seconds ago.")
            return

        # Update the last press time for the key
        last_press_times[key] = current_time

    if addDelay:
        delay += 0.2
    if locationV < 10:
        delay += 0.05

    # Print the delay and time interval between presses for debugging
    print(f"Delay {delay:.3f} seconds | Time since last {note} ({key}) press: {time_since_last_press:.3f} seconds")
    
    # Simulate key press
    if note == "Yellow Star":
        time.sleep(0.2)
        print(f"{Color.YELLOW}Pressing {note} at location H & V {locationH} & {locationV} with delay {delay:.3f} and addDelay {addDelay}{Color.RESET}")
        keyboard.press(key)
        time.sleep(0.1)
        keyboard.release(key)
        time.sleep(0.2)
    else:
        time.sleep(delay)
        if (note == "Green" or note == "Green Star"):
            print(f"{Color.GREEN}Pressing {note} at location H & V {locationH} & {locationV} with delay {delay:.3f} and addDelay {addDelay}{Color.RESET}")
        if (note == "Red" or note == "Red Star"):
            print(f"{Color.RED}Pressing {note} at location H & V {locationH} & {locationV} with delay {delay:.3f} and addDelay {addDelay}{Color.RESET}")
        if (note == "Yellow"):
            print(f"{Color.YELLOW}Pressing {note} at location H & V {locationH} & {locationV} with delay {delay:.3f} and addDelay {addDelay}{Color.RESET}")
        if (note == "Blue" or note == "Blue Star"):
            print(f"{Color.BLUE}Pressing {note} at location H & V {locationH} & {locationV} with delay {delay:.3f} and addDelay {addDelay}{Color.RESET}")
        if (note == "Orange" or note == "Orange Star"):
            print(f"{Color.ORANGE}Pressing {note} at location H & V {locationH} & {locationV} with delay {delay:.3f} and addDelay {addDelay}{Color.RESET}")
        keyboard.press(key)
        keyboard.release(key)

def press_and_release(key):
    keyboard.press_and_release(key)

def hitboxDrawing(img, noteType='normal', active=False):
    if active and noteType == "normal":
        cv2.rectangle(img, (notePP["gHor"], notePP["v"]), (notePP["gHorFinish"], notePP["vFinish"]), colors['green'], 3) # Green
        cv2.rectangle(img, (notePP["rHor"], notePP["v"]), (notePP["rHorFinish"], notePP["vFinish"]), colors['red'], 3) # Red
        cv2.rectangle(img, (notePP["yHor"], notePP["v"]), (notePP["yHorFinish"], notePP["vFinish"]), colors['yellow'], 3) # Yellow
        cv2.rectangle(img, (notePP["bHor"], notePP["v"]), (notePP["bHorFinish"], notePP["vFinish"]), colors['blue'], 3) # Blue
        cv2.rectangle(img, (notePP["oHor"], notePP["v"]), (notePP["oHorFinish"], notePP["vFinish"]), colors['orange'], 3) # Orange

    if active and noteType == "special":
        cv2.rectangle(img, (sNotePP["gHor"], sNotePP["v"]), (sNotePP["gHorFinish"], sNotePP["vFinish"]), colors['green'], 3) # Green
        cv2.rectangle(img, (sNotePP["rHor"], sNotePP["v"]), (sNotePP["rHorFinish"], sNotePP["vFinish"]), colors['red'], 3) # Red
        cv2.rectangle(img, (sNotePP["yHor"], sNotePP["v"]), (sNotePP["yHorFinish"], sNotePP["vFinish"]), colors['yellow'], 3) # Yellow
        cv2.rectangle(img, (sNotePP["bHor"], sNotePP["v"]), (sNotePP["bHorFinish"], sNotePP["vFinish"]), colors['blue'], 3) # Blue
        cv2.rectangle(img, (sNotePP["oHor"], sNotePP["v"]), (sNotePP["oHorFinish"], sNotePP["vFinish"]), colors['orange'], 3) # Orange
