import pydirectinput
import cv2
import time
time.sleep(3)
while True:
    pydirectinput.click(button='right')
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

