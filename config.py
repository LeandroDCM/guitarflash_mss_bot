notePP = { 
    #Note Pixel Position
    "gHor": 80,
    "rHor": 152,
    "yHor": 220,
    "bHor": 280,
    "oHor": 345,

    "gHorFinish": 152,
    "rHorFinish": 220,
    "yHorFinish": 280,
    "bHorFinish": 345,
    "oHorFinish": 420,

    "v": 5,
    "vFinish": 50
}
sNotePP = { 
    #Special Note Pixel Position
    "gHor": 80,
    "rHor": 145,
    "yHor": 215,
    "bHor": 280,
    "oHor": 345,

    "gHorFinish": 145,
    "rHorFinish": 215,
    "yHorFinish": 280,
    "bHorFinish": 345,
    "oHorFinish": 420,

    "v": 5,
    "vFinish": 50
}

# Miscellaneous values
distanceTrashhold = 27
specialDistanceTrashhold = 27
pressZone = (35, 110), (460, 140)
lightningCounter = 0
noteCounter = 0
addDelay = False
isSpecial = False

# Screen drawing
drawNoteHitbox = True
drawSpecialHitbox = False
drawNotePress = True

# note delays
noteDelay = 0.13
delay = 0.13
specialNoteDelay = 0.1
specialYellowNoteDelay = 0.2


# screen region
monitor = {"mon": 0, "top": 865, "left": 700, "width": 500, "height": 60}

# colors
colors = {
"green" : (0,255,0),
"red" : (0,0,255),
"yellow" : (86,255,255),
"blue" : (255,0,0),
"orange" : (0,127,255)
}

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ORANGE = '\033[33m'
    RESET = '\033[0m'
