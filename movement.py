import queue
import time
import numpy as np
import cv2
import pyautogui
import pydirectinput
from multiprocessing import Queue
import multiprocessing
from pynput.mouse import Button, Controller
import random
import keyboard

from pytesseract import pytesseract
from pytesseract import Output
import ctypes


pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


i=0
maxHealth=0
hp_x,hp_y=0,0

mouse = Controller()

user32 = ctypes.windll.user32

width = user32.GetSystemMetrics(0)
height=user32.GetSystemMetrics(1)

def sleep(x):
    for i in range(x):
        time.sleep(1)

def MoveToLane():
    for x in range(8):
        pydirectinput.moveTo(width,int(height/2))
        mouse.click(Button.right, 1)
        sleep(4)
    pydirectinput.moveTo(int(width/2),-int(height))
    mouse.click(Button.right, 1)
    sleep(4)
    pydirectinput.moveTo(width,int(height/2))
    mouse.click(Button.right, 1)

def Left():
    pydirectinput.moveTo(-width,int(height/2))
    mouse.click(Button.right, 1)

def Right():
    pydirectinput.moveTo(width,int(height/2))
    mouse.click(Button.right, 1)

def Back():
    for x in range(2):
        pydirectinput.moveTo(int(width/2),height)
        mouse.click(Button.right, 1)
        sleep(3)
    
    for x in range(30):
        keyboard.press("b")
        keyboard.release("b")
        time.sleep(1) 
    MoveToLane()

def FollowAlly(queue):
    hMin = 103 
    sMin = 146
    vMin = 179
    hMax = 104 
    sMax = 182
    vMax = 233
    while True:      
        if queue.get()=="timeout":
            sleep(80)
            while not queue.empty():
                queue.get()
        else:     
            image =pyautogui.screenshot()        
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            # Set minimum and max HSV values to display
            lower = np.array([hMin, sMin, vMin])
            upper = np.array([hMax, sMax, vMax])

            # Create HSV Image and threshold into a range.
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            output = cv2.bitwise_and(image,image, mask= mask)
            blue = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)

            result = output.copy()

            # threshold
            thresh = cv2.threshold(blue, 0, 255, cv2.THRESH_BINARY)[1]\

            # get contour bounding boxes and draw on copy of input
            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            a=0
            data=[]
            for c in contours:
                    a+=1    
                    d =cv2.boundingRect(c)
                    if w>20:
                        a+=1
                        data.append(d)        
            print(a)
            if a >2:
                x,y,w,h =data[random.randint(0,len(data)-1)] 
                pydirectinput.moveTo(x,y)
                mouse.click(Button.right, 1)

            sleep(4)

            while not queue.empty():
                queue.get()
        
def GetEnemy(queue):
    while True:      
        if queue.get()=="timeout":
            sleep(80)
            while not queue.empty():
                queue.get()
        else:
            #blurring and smoothin
            img1 = pyautogui.screenshot()
            img1 = cv2.cvtColor(np.array(img1), cv2.COLOR_RGB2BGR)

            hsv = cv2.cvtColor(img1,cv2.COLOR_BGR2HSV)

            #lower red
            lower_red = np.array([0,50,50])
            upper_red = np.array([10,255,255])


            #upper red
            lower_red2 = np.array([130,50,50])
            upper_red2 = np.array([180,255,255])

            mask = cv2.inRange(hsv, lower_red, upper_red)
            res = cv2.bitwise_and(img1,img1, mask= mask)


            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            res2 = cv2.bitwise_and(img1,img1, mask= mask2)



            imageFrame =res+res2
            red = cv2.cvtColor(imageFrame,cv2.COLOR_BGR2GRAY)

            # threshold
            thresh = cv2.threshold(red, 0, 255, cv2.THRESH_BINARY)[1]\

            # get contour bounding boxes and draw on copy of input
            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            result = imageFrame.copy()
            i=0
            data=[]
            for c in contours:    
                x,y,w,h =cv2.boundingRect(c)
                d=x,y,w,h
                if w>20 and h>20 and y<int(height/2):
                    i+=1
                    data.append(d)                    
                    #cv2.rectangle(result, (x, y), (x+w-1, y+h-1), (0, 0, 255), 1)
                    #cv2.putText(result,str(h),(x,y-16),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

            if i >3:
                x,y,w,h =data[random.randint(0,len(data)-1)] 
                pydirectinput.moveTo(x,y)
                mouse.click(Button.right, 1)
            sleep(3)
            while not queue.empty():
                queue.get()
        #cv2.imshow("result", result)
        #if cv2.waitKey(33) & 0xFF == ord('q'):
            #break
    #cv2.destroyAllWindows()

def GetHealth(queue):
    global maxHealth
    global hp_x
    global hp_y
    global i
    # Start a while loop 
    while(1):    
        image =pyautogui.screenshot()        
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        h,w=image.shape[0],image.shape[1]
        image=image[0:int(h/2), 0:w]

        original = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([22, 100, 220], dtype="uint8")
        upper = np.array([45, 255, 255], dtype="uint8")
        mask = cv2.inRange(image, lower, upper)

        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]


        rects={}
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            rects[w]=x,y,w,h
            
        max_key = max(rects, key=int)
        x,y,w,h=rects[max_key]
        

        del rects[max_key]
            
        max_key = max(rects, key=int)
        x1,y1,w1,h1=rects[max_key]
        if y1==y:
            w+=w1
            h+=h1
        '''
        cv2.rectangle(original, (x, y), (x + w, y + h), (36,255,12), 2)

        scale_percent = 60 # percent of original size
        width = int(original.shape[1] * scale_percent / 100)
        height = int(original.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(original, dim, interpolation = cv2.INTER_AREA)
        
        '''
        if w>maxHealth:
            maxHealth=w    
        if i==0:
            hp_x,hp_y=x,y
            i=1 
        else:
            if hp_x+100<x or hp_y+100<y or hp_x-100>x or hp_y-100>y:
                queue.put('timeout')
                sleep(20)          
                MoveToLane()
            elif w<maxHealth/2:
                queue.put('timeout')
                Back()
            else:
                queue.put('ok')
                    
def Timer(pqueue):
    i=0
    while True:
        i+=1
        time.sleep(1)
        if i==900:
            print("Move to lane changed!")

def main():
    pqueue = Queue()
    MoveToLane()
    sleep(60)
    print("start")
    p1 = multiprocessing.Process(target=GetHealth,args=(pqueue,))
    p2 = multiprocessing.Process(target=GetEnemy,args=(pqueue,))
    p3 = multiprocessing.Process(target=FollowAlly,args=(pqueue,))
    
    p1.start()
    p2.start()
    p3.start()



if __name__ == "__main__":
    main()