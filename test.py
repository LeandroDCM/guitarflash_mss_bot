import mss
import numpy as np
import cv2 as cv
import time

# Define the colors you're looking for in BGR format
green_note_color = [0, 255, 0]  # Green note (in BGR)
red_note_color = [0, 0, 255]    # Red note (in BGR)
highlight_color = [0, 255, 255, 255] # Yellow with full alpha (BGRA)

img = None
t0 = time.time()
n_frames = 1

# Define the area to capture
monitor = {"mon": 0, "top": 810, "left": 700, "width": 500, "height": 211}

# Initialize MSS for screen capturing
with mss.mss() as sct:
    while True:
        # Capture the specified region of the screen
        img = sct.grab(monitor)
        img = np.array(img)  # Convert to NumPy array

        # Print the shape of the image to check the number of channels
        # print(f"Image shape: {img.shape}")

        # Highlight the pixel you want to visualize (for example, (80, 150))
        pixel_x, pixel_y = 80, 150

        # Check if image has an alpha channel (4 channels)
        if img.shape[2] == 4:
            img[pixel_y, pixel_x] = highlight_color  # Change the pixel color to yellow with alpha
        else:
            # If no alpha channel, use 3-channel color
            img[pixel_y, pixel_x, :3] = highlight_color[:3]  # Change the pixel color to yellow

        # Optionally resize the captured image for display purposes
        small = cv.resize(img, (0, 0), fx=0.5, fy=0.5)
        cv.imshow("Computer Vision", small)

        # Detect specific pixels or a small region (choose a pixel in the captured image)
        pixel_color = img[pixel_y, pixel_x, :3]  # Get BGR color values of pixel at (80, 150)
        print(pixel_color)

        # Check if the pixel matches the green note color
        if np.array_equal(pixel_color, green_note_color):
            print("Green note detected at (80, 150)!")

        # Check if the pixel matches the red note color
        elif np.array_equal(pixel_color, red_note_color):
            print("Red note detected at (80, 150)!")

        # Press 'q' to break the loop and stop the program
        key = cv.waitKey(1)
        if key == ord('q'):
            break

        # FPS Calculation (optional)
        # elapsed_time = time.time() - t0
        # avg_fps = (n_frames / elapsed_time)
        # print("Average FPS: " + str(avg_fps))
        # n_frames += 1

# Cleanup OpenCV windows
cv.destroyAllWindows()
