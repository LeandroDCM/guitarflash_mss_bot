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

def press_key(key, delay,note):
    time.sleep(delay)
    print(f"Pressing {note}")
    keyboard.press(key)
    keyboard.release(key)

monitor = {"mon": 0, "top": 870, "left": 700, "width": 500, "height": 50}
with mss.mss() as sct:
    while 1:
        # img = grabScreen(bbox=(*screenStart, *screenEnd))

        # cv2.imshow("Image", img)
        img_o = sct.grab(monitor)
        img_o = np.array(img_o)
        img = cv2.cvtColor(img_o, cv2.COLOR_BGR2GRAY)

        note_detected = note.match(img)
        special_note_detected = special_note.match(img)

        if note_detected:
            print('Note matched')
            detected_notes.append(("note", time.time(), note.location))
        
        if special_note_detected:
            print('Special note matched')
            detected_notes.append(("special_note", time.time(), special_note.location))
        
        #PressZone cv2.rectangle(img, (35, 110), (460, 140), (0,255,0), 3)
        cv2.rectangle(img_o, (80, 5), (150, 50), (0,255,0), 3) #Green
        cv2.rectangle(img_o, (150, 5), (220, 50), (0,0,255), 3) #Red
        cv2.rectangle(img_o, (220, 5), (290, 50), (0,255,0), 3) #Yellow
        cv2.rectangle(img_o, (290, 5), (350, 50), (255,0,0), 3) #Blue
        cv2.rectangle(img_o, (350, 5), (420, 50), (0,255,0), 3) #Orange

        current_time = time.time()
        for note_type, detected_time, location in detected_notes:
            if current_time - detected_time > press_delay:
                # Remove note from list after pressing
                detected_notes.remove((note_type, detected_time, location))
            print(location)
            cv2.rectangle(img_o, location[0], location[1], (0,0,255), 2)
            if note_type == "note":
                verticalDistance = location[0][1] - pressZone[0][1]
                if verticalDistance < distanceTrashhold:
                    if location[0][0] < 150:
                        threading.Thread(target=press_key, args=("a", note_delay, "Green")).start()
                    elif location[0][0] > 150 and location[0][0] < 220:
                        threading.Thread(target=press_key, args=("s", note_delay, "Red")).start()
                    elif location[0][0] > 220 and location[0][0] < 290:
                        threading.Thread(target=press_key, args=("j", note_delay, "Yellow")).start()
                    elif location[0][0] > 290 and location[0][0] < 350:
                        threading.Thread(target=press_key, args=("k", note_delay, "Blue")).start()
                    elif location[0][0] > 350:
                        threading.Thread(target=press_key, args=("l", note_delay, "Orange")).start()

        if special_note.location:
            print(special_note.location)
            cv2.rectangle(img_o, special_note.location[0], special_note.location[1], (0,0,255), 2)
    
            verticalDistance = special_note.location[0][1] - pressZone[0][1]
            if verticalDistance < specialDistanceTrashhold:
                if special_note.location[0][0] < 125:
                    threading.Thread(target=press_key, args=("a", special_note_delay, "Green Star")).start()
                elif special_note.location[0][0] > 125 and special_note.location[0][0] < 205:
                    threading.Thread(target=press_key, args=("s", special_note_delay, "Red Star")).start()
                elif special_note.location[0][0] > 205 and special_note.location[0][0] < 280:
                    threading.Thread(target=press_key, args=("j", 0.15, "Yellow Star")).start()
                elif special_note.location[0][0] > 280 and special_note.location[0][0] < 340:
                    threading.Thread(target=press_key, args=("k", special_note_delay, "Blue Star")).start()
                elif special_note.location[0][0] > 340:
                    threading.Thread(target=press_key, args=("l", special_note_delay, "Orange Star")).start()


        cv2.imshow("Computer Vision", img_o)
        if cv2.waitKey(1) == ord('q'):
            break



#Ver de usar o screenGrab na classe ( talvez passar a usar o mss na classe? )