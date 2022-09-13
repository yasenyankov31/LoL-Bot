import cv2
from pytesseract import pytesseract
from pytesseract import Output
import pyautogui as p
import keyboard
import numpy as np
import time
import ctypes
import win32gui
from win32gui import FindWindow, GetWindowRect
import multiprocessing as mp
import autoit
import psutil


user32 = ctypes.windll.user32


lol_game='League of Legends (TM) Client'
lol_client='League of Legends'
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def screenshot(window_title=None):
    if window_title:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = p.screenshot(region=(x, y, x1, y1))
            return im
    else:
        im = p.screenshot()
        return im

def sleep(x):
    for i in range(x):
        time.sleep(1)

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

