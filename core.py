
import cv2
from PIL import ImageGrab
import numpy as np

class Object:
    def __init__(self, path):
        img = cv2.imread(path, 0)
        self.img = img
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.locations = []  # List of all matches

    def match(self, scr):
        res = cv2.matchTemplate(scr, self.img, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Set the threshold for a valid match
        match_locations = np.where(res >= threshold)  # Get all locations above threshold

        self.locations = []  # Clear previous locations
        for pt in zip(*match_locations[::-1]):  # Iterate through found locations
            startLoc = (pt[0], pt[1])
            endLoc = (startLoc[0] + self.width, startLoc[1] + self.height)
            self.locations.append((startLoc, endLoc))
        
        return len(self.locations) > 0

def grabScreen(bbox=None):
    img = ImageGrab.grab(bbox=(bbox))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


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