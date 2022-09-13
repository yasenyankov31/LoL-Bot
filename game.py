from utils import *
import random

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

def DetectHealth(queue):
    red,green,blue=0,28,0
    red1,green1,blue1=19,255,16
    deadFlag=False
    prevHealthBar=0
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
            queue.put("dead")
            if deadFlag==False:
                BuyItems()
            deadFlag=True
        else:
            queue.put("alive")
            _,_,w,_=cv2.boundingRect(contours[0])
            if w<prevHealthBar:
                print("Took damage")
            prevHealthBar=w

            if deadFlag:
                deadFlag=False
                          
def DetectAllyTowers(side,height,width):
    red,green,blue=170,119,59
    red1,green1,blue1=170,123,61
    turret=0
    while True:
        image =screenshot(lol_game)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        original = image.copy()
        
        lower = np.array([red,green,blue], dtype="uint8")
        upper = np.array([red1,green1,blue1], dtype="uint8")
        mask = cv2.inRange(image, lower, upper)

        original = cv2.bitwise_and(original, original, mask=mask)
        
        gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
        
        edged = cv2.Canny(gray, 30, 200)

        contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        i=0
        
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if  w>10 and (side=="blue" and y<int(image.shape[0]/2) and x >int(image.shape[1]/2)) or (side=="red" and y>int(image.shape[0]/2) and x <int(image.shape[1]/2)):
                i=1
                
        if side=="red":               
            autoit.mouse_click("right",int(width/4),int(height/1.5), 1)
        else:
            autoit.mouse_click("right",int(width/1.5),int(height/4), 1)        
                

        if i!=0:
            turret+=1
            sleep(4)
        if turret>=3:
            break

def CheckSide():
    red,green,blue=16,165,156
    red1,green1,blue1=17,166,218

    image =screenshot(lol_game)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)
    width=image.shape[1]
    
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

    for c in cnts:
        x,_,_,_ =cv2.boundingRect(c)
        if x>int(width/2):
             return "blue"

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

def DetectEnemyTowers(image):
    red,green,blue=166,195,168
    red1,green1,blue1=170,201,169 

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
        x,y,w,_ = cv2.boundingRect(c)
        if w>10:
            return x,y+300
                
    return "Nothing",""
        
def DetectEnemyMinions(side,height,width,queue):
    red,green,blue=119,140,207
    red1,green1,blue1=122,140,211
    spells=["q","w","e"]
    while True:
        queueCommand=queue.get()
        if queueCommand!="dead":
            image =screenshot(lol_game)
            xT,yT=DetectEnemyTowers(image)
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
                _,_,w,_ =cv2.boundingRect(c)
                if w>10:
                    widths.append(w)
            
            #back off if there is only enemy  
            if len(widths)>allies:
                if side=="blue":               
                    autoit.mouse_click("right",int(width/4),int(height/1.5), 1)
                else:
                    autoit.mouse_click("right",int(width/1.5),int(height/4), 1)
                sleep(1)
            else:
                #navigate to enemy
                if len(widths)==0:
                    if side=="blue":               
                        autoit.mouse_click("right",int(width/1.5),int(height/4), 1)
                    else:
                        autoit.mouse_click("right",int(width/4),int(height/1.5), 1)
                    
                #attack
                if len(widths)>0:
                    if xT!="Nothing":
                        autoit.mouse_click("right",xT,yT, 1)
                    else:
                        x,y,_,_ =cv2.boundingRect(contours[widths.index(min(widths))])
                        spell=random.choice(spells)
                        press_key(spell)
                        autoit.mouse_click("right",x,y, 1)
                        press_key(spell)
                        autoit.mouse_click("left",x,y, 1)



        while not queue.empty():
            queue.get()

def LevelUp(spell):
    keyboard.press("ctrl")
    keyboard.press(spell)
    
    keyboard.release("ctrl")
    keyboard.release(spell)

def GetXp():    
    spells=["q","w","e"]
    pointer=-1
    while True:
        sleep(30)
        print("Level up")
        LevelUp("r")
        pointer+=1
        if pointer==3:
            pointer=0
        LevelUp(spells[pointer])
         
def PlayGame():
    print("start")
    queue=mp.Queue()
    press_key("y")
    image =screenshot(lol_game)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2HSV)
    height,width=image.shape[0],image.shape[1]
    autoit.mouse_click("right",int(width/2),int(height/2), 1)
    sleep(10)
    side=CheckSide()
    print(side)
    BuyItems()
    spells=["q","w","e"]
    sleep(1)
    for spell in spells:
        LevelUp(spell)

    sleep(3)
    if side=="blue":
        autoit.mouse_click("right",int(width/1.5),int(height/4), 1)
    else:
        autoit.mouse_click("right",int(width/4),int(height/1.5), 1)
    
    p1 = mp.Process(target=GetXp)
    p1.start()
    
    DetectAllyTowers(side,height,width)
    sleep(21)
    print("attack")
    
    p2 = mp.Process(target=DetectHealth, args=(queue,))
    p2.start()
    p3 = mp.Process(target=DetectEnemyMinions, args=(side,height,width,queue))
    p3.start()
    
    
def main():
    queue=mp.Queue()
    DetectHealth(queue)
        

   
if __name__ == '__main__':
    main()