from PIL.Image import NONE
import cv2
from PIL import ImageGrab
import numpy as np
import mss
import keyboard
import pyautogui as pag
import time
import threading

from core import Object, grabScreen

distanceTrashhold = 27
specialDistanceTrashhold = 27
pressZone = (35, 110), (460, 140)
max_presses_per_second = 15
interval = 1 / max_presses_per_second
press_delay = 0
detected_notes = []

note_delay = 0.1
special_note_delay = 0.1
note = Object('objects/test_note.png')
special_note = Object('objects/special_note3.png')

def press_key(key, delay,note,location):
    time.sleep(delay)
    print(f"Pressing {note} at location {location}")
    if (note == "Yellow Star"):
        keyboard.press(key)
        time.sleep(0.1)
        keyboard.release(key)
    else:
        keyboard.press(key)
        keyboard.release(key)

monitor = {"mon": 0, "top": 870, "left": 700, "width": 500, "height": 50}
with mss.mss() as sct:
    while True:
        img_o = sct.grab(monitor)
        img_o = np.array(img_o)
        img = cv2.cvtColor(img_o, cv2.COLOR_BGR2GRAY)

        # Match normal note and special note
        note_detected = note.match(img)
        special_note_detected = special_note.match(img)

        # If regular note is detected, process all matches
        if note_detected:
            for location in note.locations:  # Iterate over all detected notes
                cv2.rectangle(img_o, location[0], location[1], (0, 0, 255), 2)  # Draw rectangles for each note
                verticalDistance = location[0][1] - pressZone[0][1]
                if verticalDistance < distanceTrashhold:  # Check if note is in press zone
                    if location[0][0] < 150:
                        threading.Thread(target=press_key, args=("a", note_delay, "Green", location[0][0])).start()
                    elif location[0][0] > 150 and location[0][0] < 220:
                        threading.Thread(target=press_key, args=("s", note_delay, "Red", location[0][0])).start()
                    elif location[0][0] > 220 and location[0][0] < 290:
                        threading.Thread(target=press_key, args=("j", note_delay, "Yellow", location[0][0])).start()
                    elif location[0][0] > 290 and location[0][0] < 350:
                        threading.Thread(target=press_key, args=("k", note_delay, "Blue", location[0][0])).start()
                    elif location[0][0] > 350:
                        threading.Thread(target=press_key, args=("l", note_delay, "Orange", location[0][0])).start()

        #PressZone cv2.rectangle(img, (35, 110), (460, 140), (0,255,0), 3)
        cv2.rectangle(img_o, (80, 5), (145, 50), (0,255,0), 3) #Green
        cv2.rectangle(img_o, (145, 5), (215, 50), (0,0,255), 3) #Red
        cv2.rectangle(img_o, (215, 5), (280, 50), (0,255,0), 3) #Yellow
        cv2.rectangle(img_o, (280, 5), (350, 50), (255,0,0), 3) #Blue
        cv2.rectangle(img_o, (350, 5), (420, 50), (0,255,0), 3) #Orange

        # Similarly, process special notes
        if special_note_detected:
            for location in special_note.locations:
                cv2.rectangle(img_o, location[0], location[1], (0, 255, 0), 2)
                verticalDistance = location[0][1] - pressZone[0][1]
                if verticalDistance < specialDistanceTrashhold:  # Check if special note is in press zone
                    if location[0][0] < 145:
                        threading.Thread(target=press_key, args=("a", special_note_delay, "Green Star", location[0][0])).start()
                    elif location[0][0] > 145 and location[0][0] < 215:
                        threading.Thread(target=press_key, args=("s", special_note_delay, "Red Star", location[0][0])).start()
                    elif location[0][0] > 215 and location[0][0] < 280:
                        threading.Thread(target=press_key, args=("j", 0.2, "Yellow Star", location[0][0])).start()
                    elif location[0][0] > 280 and location[0][0] < 350:
                        threading.Thread(target=press_key, args=("k", special_note_delay, "Blue Star", location[0][0])).start()
                    elif location[0][0] > 350:
                        threading.Thread(target=press_key, args=("l", special_note_delay, "Orange Star", location[0][0])).start()

        # Display the screen with rectangles drawn
        cv2.imshow("Computer Vision", img_o)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break



#Ver de usar o screenGrab na classe ( talvez passar a usar o mss na classe? )