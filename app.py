from PIL.Image import NONE
import cv2
import numpy as np
import mss
import threading
from core import *
from config import *

# making images into Objects
note = Object('objects/note.png')
note_missing = Object('objects/note_missing.png')
note_lightning2 = Object('objects/note_lightning2.png')
special_note = Object('objects/special_note3.png')
lightning_test = Object('objects/lightning_test_60height.png')
lightning_note = Object('objects/lightning_note.png')

with mss.mss() as sct:
    while True:
        img_o = sct.grab(monitor)
        img_o = np.array(img_o)
        img = cv2.cvtColor(img_o, cv2.COLOR_BGR2GRAY)

        # Match normal note and special note
        note_detected = note.match(img) or lightning_note.match(img) or note.match(img, scale=1.1) or note.match(img, scale=0.90) or note.match(img, scale=0.95) or note.match(img, scale=1.05) or note_missing.match(img, threshold=0.7) or note_missing.match(img, threshold=0.7, scale=0.95) or note_missing.match(img, threshold=0.7, scale=1.05) or note_lightning2.match(img, threshold=0.7) or note_lightning2.match(img, threshold=0.7, scale=0.95) or note_lightning2.match(img, threshold=0.7, scale=1.05)
        special_note_detected = special_note.match(img)
        lightning_detected = lightning_test.match(img)

        if lightning_detected:
            print("THUNDER!")
            lightningCounter += 1
            if lightningCounter == 2:
                press_and_release("space")


        # If regular note is detected, process all matches
        if note_detected:
            noteCounter += 1
            # if isSpecial and noteCounter < 30:
            #     addDelay = True
            # if isSpecial and noteCounter > 30:
            #     isSpecial = False
            #     addDelay = False
            for location in note.locations:  # Iterate over all detected notes
                cv2.rectangle(img_o, location[0], location[1], (0, 0, 255), 2)  # Draw rectangles for each note
                verticalDistance = location[0][1] - pressZone[0][1]
                if verticalDistance < distanceTrashhold:  # Check if note is in press zone
                    print(noteCounter)
                    if location[0][0] < notePP["gHorFinish"]:
                        threading.Thread(target=press_key, args=("a", delay, "Green", location[0][0], location[0][1], addDelay)).start()
                    elif location[0][0] > notePP["gHorFinish"] and location[0][0] < notePP["rHorFinish"]:
                        threading.Thread(target=press_key, args=("s", delay, "Red", location[0][0], location[0][1], addDelay)).start()
                    elif location[0][0] > notePP["rHorFinish"] and location[0][0] < notePP["yHorFinish"]:
                        threading.Thread(target=press_key, args=("j", delay, "Yellow", location[0][0], location[0][1], addDelay)).start()
                    elif location[0][0] > notePP["yHorFinish"] and location[0][0] < notePP["bHorFinish"]:
                        threading.Thread(target=press_key, args=("k", delay, "Blue", location[0][0], location[0][1], addDelay)).start()
                    elif location[0][0] > notePP["bHorFinish"]:
                        threading.Thread(target=press_key, args=("l", delay, "Orange", location[0][0], location[0][1], addDelay)).start()

        # Similarly, process special notes
        if special_note_detected:
            noteCounter = 0
            isSpecial = True
            for location in special_note.locations:
                cv2.rectangle(img_o, location[0], location[1], (0, 255, 0), 2)
                verticalDistance = location[0][1] - pressZone[0][1]
                if verticalDistance < specialDistanceTrashhold:  # Check if special note is in press zone
                    if location[0][0] < sNotePP["gHorFinish"]:
                        threading.Thread(target=press_key, args=("a", specialNoteDelay, "Green Star", location[0][0], location[0][1], addDelay)).start()
                    elif location[0][0] > sNotePP["gHorFinish"] and location[0][0] < sNotePP["rHorFinish"]:
                        threading.Thread(target=press_key, args=("s", specialNoteDelay, "Red Star", location[0][0], location[0][1], addDelay)).start()
                    elif location[0][0] > sNotePP["rHorFinish"] and location[0][0] < sNotePP["yHorFinish"]:
                        threading.Thread(target=press_key, args=("j", specialYellowNoteDelay, "Yellow Star", location[0][0], location[0][1], addDelay)).start()
                    elif location[0][0] > sNotePP["yHorFinish"] and location[0][0] < sNotePP["bHorFinish"]:
                        threading.Thread(target=press_key, args=("k", specialNoteDelay, "Blue Star", location[0][0], location[0][1], addDelay)).start()
                    elif location[0][0] > sNotePP["bHorFinish"]:
                        threading.Thread(target=press_key, args=("l", specialNoteDelay, "Orange Star", location[0][0], location[0][1], addDelay)).start()

        #Visual Debugging
        #PressZone cv2.rectangle(img, (35, 110), (460, 140), (0,255,0), 3)
        hitboxDrawing(img_o, "normal", drawNoteHitbox)

        # Display the screen with rectangles drawn
        cv2.imshow("Computer Vision", img_o)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) == ord('q'):
            break

#Adicionar indicador visual que a tecla está sendo apertada na tela para faciliatar o debug vídeo

#Ver de usar o screenGrab na classe ( talvez passar a usar o mss na classe? )


    # pegar tela branca quando ativa o especial (n funfou quando testei)
    # pixel_color = img_o[50, 151, :3]
    # if np.array_equal(pixel_color, [236,235,236]): remover se não usar
    #     print("@@@@@@@@@@@@@@@")