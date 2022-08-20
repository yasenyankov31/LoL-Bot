from operator import le
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

def ScreenShotLeague():
    image =screenshot(lol_game)
    image.save("level.png")

def ShowSmallImg(original):
        scale_percent = 60 # percent of original size
        width = int(original.shape[1] * scale_percent / 100)
        height = int(original.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(original, dim, interpolation = cv2.INTER_AREA)

        cv2.imshow("result1", resized)

def sleep(x):
    for i in range(x):
        time.sleep(1)

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

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

def WindowsXandY(window_name):
        window_handle = FindWindow(None, window_name)
        window_rect   = GetWindowRect(window_handle)
        return window_rect[0],window_rect[1]

def FindButton(name):
    img = screenshot(lol_client)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    image_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, imageblack = cv2.threshold(
        image_greyscale, 130, 220, cv2.THRESH_BINARY)
    
    image_data = pytesseract.image_to_data(imageblack, output_type=Output.DICT)
    
    print('done')
    for i, word in enumerate(image_data['text']):
        if word.lower()==name:
            xScreen,yScreen=WindowsXandY(lol_client)
            x,y = image_data['left'][i], image_data['top'][i]
            p.moveTo(x+xScreen, y+yScreen)
            p.click()
            break

def Accept():
    while True:
        print("accept")
        img = screenshot(lol_client)
        if img!=None:
            img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            image_greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            _, imageblack = cv2.threshold(
                image_greyscale, 130, 220, cv2.THRESH_BINARY)

            image_data = pytesseract.image_to_data(imageblack, output_type=Output.DICT)
            for i, word in enumerate(image_data['text']):
                if word.lower()=='decline':
                    xScreen,yScreen=WindowsXandY(lol_client)
                    x, y, = image_data['left'][i], image_data['top'][i]
                    x,y = image_data['left'][i], image_data['top'][i]
                    p.moveTo(x+xScreen, y+yScreen)
                    p.click()
                    break

def StopAccept(queue):
    while True:
        if "League of Legends.exe" in (i.name() for i in psutil.process_iter()):
            queue.put("KILL ACCEPT")

def CheckIfGameStarted(queue):
    while True:
        
        press_key("escape")
        img = screenshot(lol_game)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        blur = cv2.pyrMeanShiftFiltering(img, 15, 15)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        image_data = pytesseract.image_to_data(thresh, output_type=Output.DICT)

        for i, word in enumerate(image_data['text']):
            if word.lower() == 'interface':
                queue.put("GAME STARTED")    
                press_key("escape")

def FindMenuWord(menu_word,clicks):
    img=screenshot(lol_game)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    red,green,blue=0,0,0
    red1,green1,blue1=127,255,255

    lower = np.array([red,green,blue], dtype="uint8")
    upper = np.array([red1,green1,blue1], dtype="uint8")
    mask = cv2.inRange(img, lower, upper)

    image_data = pytesseract.image_to_data(mask, output_type=Output.DICT)

    for i, word in enumerate(image_data['text']):
        if word.lower()==menu_word:
            print(menu_word)
            x,y = image_data['left'][i],image_data['top'][i]
            autoit.mouse_click("left", x, y, clicks)
            break

def BuyItems():
    press_key("p")
    sleep(2)
    FindMenuWord('recommended',1)
    sleep(3)
    FindMenuWord('generally',2)
    press_key("p")

def LaunchGame():
    buttons=['play','pvp','aram','confirm','find']
    for button in buttons:
        FindButton(button)
        sleep(3)
    queue=mp.Queue()

    p1 = mp.Process(target=Accept)
    p2 = mp.Process(target=StopAccept, args=(queue,))
    


    p1.start()
    p2.start()
    #terminate accept process
    while True:
        msg = queue.get()
        if msg=="KILL ACCEPT":
            print("killed")
            p1.terminate()
            p2.terminate()
            break

    #clear queue
    while not queue.empty():
        queue.get()

    p3 = mp.Process(target=CheckIfGameStarted, args=(queue,))
    p3.start()

    #terminate gameifstarted process
    while True:
        msg = queue.get()
        if msg=="GAME STARTED":
            p3.terminate()
            break

def DetectHealth():
    red,green,blue=0,28,0
    red1,green1,blue1=19,255,16
    while True:
        image=screenshot(lol_game)
        
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        lower = np.array([red,green,blue])
        upper = np.array([red1,green1,blue1])
        mask = cv2.inRange(image, lower, upper)

                #define kernel size  
        kernel = np.ones((10,10),np.uint8)
        # Remove unnecessary noise from mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        image = cv2.blur(image, (50,50))

        output = cv2.bitwise_and(image,image, mask= mask)

        

        gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)


        # threshold
        edged = cv2.Canny(gray, 50, 200)

        # get contour bounding boxes and draw on copy of input
        contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        
        if len(contours)==0:
            print("dead")
        else:
            print("alive")
              
def DetectAllyTowers(queue):
    red,green,blue=165,116,58
    red1,green1,blue1=168,119,59
    checker=True
    healthbars=0
    while True:
        image =screenshot(lol_game)
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

        if i==0 and checker:
            checker=False
            healthbars+=1      
        else:
            checker=True
        
        if healthbars>=2:
             queue.put("stop")
        else:
            queue.put("nothing")

def CheckSide():
    red,green,blue=16,165,156
    red1,green1,blue1=17,166,218

    image =screenshot(lol_game)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)
    
    image = cv2.blur(image, (3,3)) 

    lower = np.array([red,green,blue], dtype="uint8")
    upper = np.array([red1,green1,blue1], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)

    #define kernel size  
    
    # Remove unnecessary noise from mask
    kernel = np.ones((7,7),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    if len(cnts)!=0:
        return "blue"
    else:
        return "red"

def DetectAllyMinions(image):
    red,green,blue=16,159,208
    red1,green1,blue1=17,161,211

    lower = np.array([red,green,blue], dtype="uint8")
    upper = np.array([red1,green1,blue1], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)

    output = cv2.bitwise_and(image, image, mask=mask)

    gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)
            # threshold
    edged = cv2.Canny(gray, 30, 200)

    # get contour bounding boxes and draw on copy of input
    contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    #ShowSmallImg(mask)

    return len(contours)

def DetectEnemyTowers():
    red,green,blue=166,195,168
    red1,green1,blue1=170,201,169 
    while True:
        if cv2.waitKey(1) == 27:
            break
        image =p.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV_FULL)
        original=image.copy()
        


        lower = np.array([red,green,blue], dtype="uint8")
        upper = np.array([red1,green1,blue1], dtype="uint8")
        mask = cv2.inRange(image, lower, upper)

        #define kernel size  
        kernel = np.ones((12,12),np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        original = cv2.bitwise_and(original, original, mask=mask)
        gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)

        # threshold

        
        edged = cv2.Canny(gray, 30, 200)

        # get contour bounding boxes and draw on copy of input
        contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if w>10:
                print(w)
                

        
        

        scale_percent = 60 # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(mask, dim, interpolation = cv2.INTER_AREA)

        cv2.imshow("result1", resized)   

def DetectEnemyMinions():
    red,green,blue=119,140,207
    red1,green1,blue1=122,140,211

    while True:   
        if cv2.waitKey(1) == 27:
            break
        image =screenshot(lol_game)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)
        allies=DetectAllyMinions(image)


        lower = np.array([red,green,blue], dtype="uint8")
        upper = np.array([red1,green1,blue1], dtype="uint8")
        mask = cv2.inRange(image, lower, upper)

        output = cv2.bitwise_and(image,image, mask= mask)

        gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)


        # threshold
        edged = cv2.Canny(gray, 30, 200)

        # get contour bounding boxes and draw on copy of input
        contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = contours[0] if len(contours) == 2 else contours[1]
        


        widths=[]
        for c in contours:    
            _,_,w,h =cv2.boundingRect(c)
            if w>10:
                widths.append(w)

        
        
        if len(contours)>allies:
            print("red")
        if len(contours)>0:
            x,y,_,_ =cv2.boundingRect(contours[widths.index(min(widths))])
            autoit.mouse_click("right",x,y, 1)

def LevelUp(spell):
    keyboard.press("ctrl")
    keyboard.press(spell)
    
    keyboard.release("ctrl")
    keyboard.release(spell)

def DetectXp():
    red,green,blue=92,99,255
    red1,green1,blue1=92,104,255

    image=screenshot(lol_game)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)
    original=image.copy()
    

    
    
    lower = np.array([red,green,blue], dtype="uint8")
    upper = np.array([red1,green1,blue1], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)
        

    original = cv2.bitwise_and(original, original, mask=mask)
    gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)


    
    edged = cv2.Canny(gray, 30, 200)

    # get contour bounding boxes and draw on copy of input
    contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    return len(contours)

def GetXp(pixels):
    level=3
    spells=["q","w","e"]
    pointer=-1
    while True:
        pixelsnow=DetectXp()
        print(level) 
        if pixelsnow>=pixels or pixelsnow>=pixels-10:
            level+=1
            if level==6 or level==11 or level==16:
                LevelUp("r")
            else:
                pointer+=1
                if pointer==3:
                    pointer=0
                LevelUp(spells[pointer])

            sleep(1)
          
def PlayGame():
    print("start")
    press_key("y")
    side=CheckSide()
    XPpixels=DetectXp()
    BuyItems()
    spells=["q","w","e"]
    sleep(1)
    for spell in spells:
        LevelUp(spell)
    
    image =screenshot(lol_game)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)
    height,width=image.shape[0],image.shape[1]
    q=mp.Queue()
    sleep(3)
    if side=="blue":
        autoit.mouse_click("right",int(width/1.5),int(height/4), 1)
    else:
        autoit.mouse_click("right",int(width/4),int(height/1.5), 1)
    
    p1 = mp.Process(target=DetectAllyTowers, args=(q,))
    p2 = mp.Process(target=GetXp, args=(XPpixels,))
    p1.start()
    p2.start()
    while True:
        msg = q.get()
        if msg =="stop":
            p1.terminate()
            break
        if side=="blue":
            autoit.mouse_click("right",int(width/1.5),int(height/4), 1)
        else:
            autoit.mouse_click("right",int(width/4),int(height/1.5), 1)
    
    p3 = mp.Process(target=DetectEnemyMinions)
    p3.start()
    
    

def main():
    PlayGame()
        

   
if __name__ == '__main__':
    main()