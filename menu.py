from utils import *

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
