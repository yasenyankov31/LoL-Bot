# Python program to create RGB color  
# palette with trackbars 
  
# importing libraries
from turtle import pu
import cv2
import numpy as np
import pyautogui
   
# empty function called when
# any trackbar moves
def emptyFunction(x):
    pass
   
def main():
      
    # blackwindow having 3 color chanels
    windowName ="Open CV Color Palette"
    # window name
    cv2.namedWindow(windowName) 
    cv2.resizeWindow(windowName,800, 640)
       
    # there trackbars which have the name
    # of trackbars min and max value 
    cv2.createTrackbar('Blue', windowName, 0, 255, emptyFunction)
    cv2.createTrackbar('Green', windowName, 0, 255, emptyFunction)
    cv2.createTrackbar('Red', windowName, 0, 255, emptyFunction)

    cv2.createTrackbar('Blue1', windowName, 0, 255, emptyFunction)
    cv2.createTrackbar('Green1', windowName, 0, 255, emptyFunction)
    cv2.createTrackbar('Red1', windowName, 0, 255, emptyFunction)


    
       
    # Used to open the window
    # till press the ESC key
    while(True):
          
        if cv2.waitKey(1) == 27:
            break
          
        # values of blue, green, red
        blue = cv2.getTrackbarPos('Blue', windowName)
        green = cv2.getTrackbarPos('Green', windowName)
        red = cv2.getTrackbarPos('Red', windowName)

        blue1 = cv2.getTrackbarPos('Blue1', windowName)
        green1 = cv2.getTrackbarPos('Green1', windowName)
        red1 = cv2.getTrackbarPos('Red1', windowName)

          
        image = pyautogui.screenshot()
        
        #image=cv2.imread("level.png")
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        original = image.copy()
        
        lower = np.array([red,green,blue], dtype="uint8")
        upper = np.array([red1,green1,blue1], dtype="uint8")
        mask = cv2.inRange(image, lower, upper)

        kernel = np.ones((12,12),np.uint8)
        #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    

        
        original = cv2.bitwise_and(original, original, mask=mask)
        
        gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)


        
        edged = cv2.Canny(gray, 30, 200)

        contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        i=0

        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if w>10 and y<=int(image.shape[0]/2):
                i+=1
        
        print(i)
        scale_percent = 60 # percent of original size
        width = int(original.shape[1] * scale_percent / 100)
        height = int(original.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(mask, dim, interpolation = cv2.INTER_AREA)

        cv2.imshow("result1", resized)

# Calling main()         
if __name__=="__main__":
    main()