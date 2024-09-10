import mss
import numpy as np
import cv2 as cv
import time

pixel_y = 80
green_note_pixel_x = 90
red_note_pixel_x = 170
yellow_note_pixel_x = 250
blue_note_pixel_x = 333
orange_note_pixel_x = 415

# Define the colors you're looking for in BGR format (OpenCV uses BGR, not RGB)
green_note_color = [0, 255, 0]  # Green note (in BGR)
red_note_color = [30, 26, 255]    # Red note (in BGR)

img = None
t0 = time.time()
n_frames = 1
# Define the area to capture (as in your base code)
monitor = {"mon": 0, "top": 810, "left": 700, "width": 500, "height": 211}

# Initialize MSS for screen capturing
with mss.mss() as sct:
    while True:
        # Capture the specified region of the screen
        img = sct.grab(monitor)
        img = np.array(img)  # Convert to NumPy array
        if img.shape[2] == 4:
            img[pixel_y,green_note_pixel_x] = [0, 255, 255, 255]
            img[pixel_y,red_note_pixel_x] = [0, 255, 255, 255]
            img[pixel_y,yellow_note_pixel_x] = [0, 255, 255, 255]
            img[pixel_y,blue_note_pixel_x] = [0, 255, 255, 255]
            img[pixel_y,orange_note_pixel_x] = [0, 255, 255, 255]  # Change the pixel color to yellow with alpha
        else:
            # If no alpha channel, use 3-channel color
            img[pixel_y,green_note_pixel_x] = [0, 255, 255, 255][:3]
            img[pixel_y,red_note_pixel_x] = [0, 255, 255, 255][:3]
            img[pixel_y,yellow_note_pixel_x] = [0, 255, 255, 255][:3]
            img[pixel_y,blue_note_pixel_x] = [0, 255, 255, 255][:3]
            img[pixel_y,orange_note_pixel_x] = [0, 255, 255, 255][:3]
        # Optionally resize the captured image for display purposes (this is not necessary for detection)
        small = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
        cv.imshow("Computer Vision", small)

        # Detect specific pixels or a small region (choose a pixel in the captured image)
        # In this example, we'll check pixel at (250, 105) within the captured 500x211 region
        pixel_color = img[80, 151, :3]  # Get BGR color values of pixel at (250, 105)
        print(pixel_color)


        # Check if the pixel matches the green note color
        if np.array_equal(pixel_color, green_note_color):
            print("Green note detected at (250, 105)!")

        # Check if the pixel matches the red note color
        elif np.array_equal(pixel_color, red_note_color):
            print("Red note detected at (250, 105)!")

        # Press 'q' to break the loop and stop the program
        key = cv.waitKey(1)
        if key == ord('q'):
            break

        # FPS Calculation (optional, just for performance tracking)
        elapsed_time = time.time() - t0
        avg_fps = (n_frames / elapsed_time)
        print("Average FPS: " + str(avg_fps))
        n_frames += 1

# Cleanup OpenCV windows
cv.destroyAllWindows()
