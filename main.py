import cv2
from pytesseract import pytesseract
from pytesseract import Output
import pyautogui as p
import numpy as np
import time

pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
def FindChampion(name):
    img = p.screenshot()
    img.save('D:\\Programirane\\LeagueBot\\templates\\screnshot.png')
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    blur = cv2.pyrMeanShiftFiltering(img, 11, 11)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    image_data = pytesseract.image_to_data(thresh, output_type=Output.DICT)
    print('done')
    for i, word in enumerate(image_data['text']):
        if word.lower() == name:
                x, y, = image_data['left'][i], image_data['top'][i]
                p.moveTo(x, y)
                p.click()

def FindButton(name):
    img = p.screenshot()
    img.save('D:\\Programirane\\LeagueBot\\templates\\screnshot.png')
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
            p.moveTo(x, y-55)
            p.click()
            ans='d'
        else :
            if word ==name:
                    x, y, = image_data['left'][i], image_data['top'][i]
                    p.moveTo(x, y)
                    p.click()
                      

    
def main():
    FindButton('play')
    time.sleep(3)
    FindButton('co-op')
    time.sleep(3)
    FindButton('beginner')
    time.sleep(3)
    FindButton('confirm')
    time.sleep(3)
    p.click()
    ans='q'
    while ans=='q': 
        img = p.screenshot()
        img.save('D:\\Programirane\\LeagueBot\\templates\\screnshot.png')
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
                p.moveTo(x, y-55)
                p.click()
                ans='d'
    time.sleep(3)
    FindChampion('teemo')
    FindChampion('lock')

if __name__ == "__main__":
    main()