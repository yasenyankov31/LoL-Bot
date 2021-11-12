from types import TracebackType
import cv2
from pytesseract import pytesseract
from pytesseract import Output
from multiprocessing import Queue
import pyautogui as p
import pydirectinput
import numpy as np
import time
import ctypes
import win32gui
from win32gui import FindWindow, GetWindowRect

import multiprocessing

 
user32 = ctypes.windll.user32

champions=['ivern','diana','jing,','malphite','master','mordekaicer','teemo','ee','tristana','seraphine','sona']
lol='League of Legends'
lol_client='League of Legends(TM) Client'

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
    while True:
        img = screenshot(lol)
        #img.save('D:\\Programirane\\LoL-Bot\\templates\\screnshot.png')
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        blur = cv2.pyrMeanShiftFiltering(img, 3, 3)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        image_data = pytesseract.image_to_data(thresh, output_type=Output.DICT)
        print('searching champ..')
        for i, word in enumerate(image_data['text']):
                for x in champions:
                    if word.lower()==x:
                            x, y, = image_data['left'][i], image_data['top'][i]
                            x1,y1=WindowsXandY()
                            p.moveTo(x+x1, y+y1)
                            p.click()
                                       
def LockIn(pqueue):
    while True:
        img = screenshot(lol)
        #img.save('D:\\Programirane\\LoL-Bot\\templates\\screnshot.png')
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
                pqueue.put("Locked") 
   
def Accept():
    while True:
        img = screenshot(lol)
        #img.save('D:\\screnshot.png')
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

def FindButton(name):
    xAndy_list=[]
    img = screenshot(lol)
    #img.save('D:\\Programirane\\LoL-Bot\\templates\\screnshot.png')
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    image_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    thresh, imageblack = cv2.threshold(
        image_greyscale, 130, 220, cv2.THRESH_BINARY)
    
    image_data = pytesseract.image_to_data(imageblack, output_type=Output.DICT)
    
    print('done')
    for i, word in enumerate(image_data['text']):
        if word.lower()==name:
            data = image_data['left'][i], image_data['top'][i]
            xAndy_list.append(data)
    for data in xAndy_list:
        x,y=data
        x1,y1=WindowsXandY()
        p.moveTo(x+x1, y+y1)
        p.click()
        break
                       
def GameStarted(pqueue):
    while True:
        try:
            if pqueue.get()=="Locked":
                img = screenshot(lol_client)
                img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                blur = cv2.pyrMeanShiftFiltering(img, 15, 15)
                gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

                image_data = pytesseract.image_to_data(thresh, output_type=Output.DICT)


                # Printing each word
                #for word in image_data['text']:
                    #print(word)
                
                pydirectinput.press("escape")
                time.sleep(4) 
                for i, word in enumerate(image_data['text']):
                    if word.lower() == 'defaults':
                        print("Game Started")

                time.sleep(10)
        except:
            time.sleep(4)  

def main():
    FindButton('play')
    time.sleep(3)
    FindButton('co-op')
    time.sleep(3)
    FindButton('beginner')
    time.sleep(3)
    FindButton('confirm')
    time.sleep(5)
    p.click()

    pqueue = Queue()

    p1 = multiprocessing.Process(target=Accept)
    p2 = multiprocessing.Process(target=FindChampion)
    p3 = multiprocessing.Process(target=LockIn, args=(pqueue,))
    p4 = multiprocessing.Process(target=GameStarted, args=(pqueue,))

    # starting our processes
    p1.start()
    p2.start()
    p3.start()
    p4.start() 

    if pqueue.get()=="Game started":
        p1.close()
        p2.close()
        p3.close()
        p4.close() 

    
if __name__ == "__main__":
    main()