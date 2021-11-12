import time
from pynput.mouse import Button, Controller

time.sleep(4)
mouse = Controller()
mouse.click(Button.right, 1)