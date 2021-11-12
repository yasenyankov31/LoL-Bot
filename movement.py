import queue
from re import T
import time
import numpy as np
import cv2
import pyautogui
import pydirectinput
from multiprocessing import Queue
import multiprocessing

from pytesseract import pytesseract
from pytesseract import Output
import ctypes

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

maxHealth=0
user32 = ctypes.windll.user32
width = user32.GetSystemMetrics(0)
height=user32.GetSystemMetrics(1)

def MoveToLane():
    for x in range(6):
        pydirectinput.moveTo(width,int(height/2))
        pydirectinput.rightClick(button='right')
        time.sleep(5)
    pydirectinput.moveTo(int(width/2),-height)
    pydirectinput.doubleClick(button='right')
    time.sleep(3)
    pydirectinput.moveTo(int(width/2),int(height/2))
    pydirectinput.doubleClick(button='right')


def Back():
    for x in range(2):
        pydirectinput.moveTo(int(width/2),height)
        pydirectinput.doubleClick(button='right')
        time.sleep(3)
    pydirectinput.keyDown("b")
    time.sleep(15)
    MoveToLane()

#pyautogui.displayMousePosition()
def GetEnemy(queue):
    while True:
        print(queue.get())
        if queue.get()=="timeout":
            for x in range(30):
                time.sleep(1)
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
            for c in contours:
                x,y,w,h = cv2.boundingRect(c)
                if w>20 and h>20 and y<int(height/2):
                    pydirectinput.moveTo(x,y)
                    pydirectinput.rightClick()
                    break
                    
                    #cv2.rectangle(result, (x, y), (x+w-1, y+h-1), (0, 0, 255), 1)
                    #cv2.putText(result,str(h),(x,y-16),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            time.sleep(3)

        #cv2.imshow("result", result)
        #if cv2.waitKey(33) & 0xFF == ord('q'):
            #break
    #cv2.destroyAllWindows()

def GetHealth(queue):
    global maxHealth
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

        if w>maxHealth:
            maxHealth=w
        
        if w<maxHealth/2:
            queue.put('timeout')
            Back()
        else:
            queue.put('ok')
        #cv2.rectangle(original, (x, y), (x + w, y + h), (36,255,12), 2)
        """
        scale_percent = 60 # percent of original size
        width = int(original.shape[1] * scale_percent / 100)
        height = int(original.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(original, dim, interpolation = cv2.INTER_AREA)

        cv2.imshow("result", resized)
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()   
    """

def main():
    pqueue = Queue()
    #MoveToLane()
    p1 = multiprocessing.Process(target=GetHealth,args=(pqueue,))
    p2 = multiprocessing.Process(target=GetEnemy,args=(pqueue,))
    
    p1.start()
    p2.start()

if __name__ == "__main__":
    main()