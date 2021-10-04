import cv2
from pytesseract import pytesseract
from pytesseract import Output
import pyautogui as p
import numpy as np
import time
import ctypes
import win32gui
from win32gui import FindWindow, GetWindowRect

import multiprocessing


user32 = ctypes.windll.user32
champions=['ivern','diana','jing,','malphite','master','mordekaicer','teemo','ee','tristana']
lol='League of Legends'

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def WindowsXandY():
        window_handle = FindWindow(None, lol)
        window_rect   = GetWindowRect(window_handle)
        return window_rect[0],window_rect[1]


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
            print('Window not found!')
    else:
        im = p.screenshot()
        return im

def FindChampion():
    img = screenshot(lol)
    img.save('D:\\Programirane\\LoL-Bot\\templates\\screnshot.png')
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    blur = cv2.pyrMeanShiftFiltering(img, 3, 3)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    image_data = pytesseract.image_to_data(thresh, output_type=Output.DICT)
    print('done')
    for i, word in enumerate(image_data['text']):
            for x in champions:
                if word.lower()==x:
                        x, y, = image_data['left'][i], image_data['top'][i]
                        x1,y1=WindowsXandY()
                        p.moveTo(x+x1, y+y1)
                        p.click()
                        
                
def LockIn():
    img = screenshot(lol)
    img.save('D:\\Programirane\\LoL-Bot\\templates\\screnshot.png')
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    image_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh, imageblack = cv2.threshold(
        image_greyscale, 130, 220, cv2.THRESH_BINARY)

    image_data = pytesseract.image_to_data(imageblack, output_type=Output.DICT)
    print('done')
    for i, word in enumerate(image_data['text']):
        if word.lower()=='lock':
            x, y, = image_data['left'][i], image_data['top'][i]
            x1,y1=WindowsXandY()
            p.moveTo(x+x1, y+y1)
            p.click() 

def FindButton(name):
    img = screenshot(lol)
    img.save('D:\\Programirane\\LoL-Bot\\templates\\screnshot.png')
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    image_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh, imageblack = cv2.threshold(
        image_greyscale, 130, 220, cv2.THRESH_BINARY)
    
    image_data = pytesseract.image_to_data(imageblack, output_type=Output.DICT)

    print('done')
    for i, word in enumerate(image_data['text']):
        word=word.lower()
        if word=='decline':
            x, y, = image_data['left'][i], image_data['top'][i]
            x1,y1=WindowsXandY()
            p.moveTo(x+x1, y+y1)
            p.click()
        elif word==name:
            x, y, = image_data['left'][i], image_data['top'][i]
            x1,y1=WindowsXandY()
            p.moveTo(x+x1, y+y1)
            p.click()
                   
def UiButtons():
    FindButton('play')
    time.sleep(3)
    FindButton('co-op')
    time.sleep(3)
    FindButton('beginner')
    time.sleep(3)
    FindButton('confirm')
    time.sleep(5)
    p.click()
    ans='q'
    while ans=='q': 
        img = screenshot(lol)
        img.save('D:\\screnshot.png')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        image_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thresh, imageblack = cv2.threshold(
            image_greyscale, 130, 220, cv2.THRESH_BINARY)

        image_data = pytesseract.image_to_data(imageblack, output_type=Output.DICT)
        for i, word in enumerate(image_data['text']):
            if word.lower()=='decline':
                x, y, = image_data['left'][i], image_data['top'][i]
                x1,y1=WindowsXandY()
                p.moveTo(x+x1, y+y1-55)
                p.click()
                ans='d' 

def main():
    UiButtons()
    FindChampion()             
    LockIn()

if __name__ == "__main__":
    main()