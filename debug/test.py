from utils import *

def DetectAllyTowers(side):
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

        original = cv2.bitwise_and(original, original, mask=mask)
        
        gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
        

        
        edged = cv2.Canny(gray, 30, 200)

        contours = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        i=0
        if side=="blue":
            for c in contours:
                x,y,w,h = cv2.boundingRect(c)
                if w>10 and y<int(image.shape[0]/2):
                    i+=1
                    break
        else:
            for c in contours:
                x,y,w,h = cv2.boundingRect(c)
                if w>10 and y>int(image.shape[0]/2):
                    i+=1
                    break

        if i==0 and checker:
            checker=False
            healthbars+=1
            sleep(1)      
        else:
            checker=True
        
        print(healthbars)

DetectAllyTowers("blue")
