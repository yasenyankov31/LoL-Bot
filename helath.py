import time
import numpy as np
import cv2
import pyautogui

i=0
maxHealth=0
hp_x,hp_y=0,0

while True:
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

    cv2.rectangle(original, (x, y), (x + w, y + h), (36,255,12), 2)

    scale_percent = 60 # percent of original size
    width = int(original.shape[1] * scale_percent / 100)
    height = int(original.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized = cv2.resize(original, dim, interpolation = cv2.INTER_AREA)
    if w>maxHealth:
        maxHealth=w

     
    if i==0:
        hp_x,hp_y=x,y
        i=1 
    else:
        if hp_x+100<x or hp_y+100<y or hp_x-100>x or hp_y-100>y:
            print('dead')
        else:
            print('alive')  

    #cv2.imshow("result", resized)
    #if cv2.waitKey(33) & 0xFF == ord('q'):
        #break

  
