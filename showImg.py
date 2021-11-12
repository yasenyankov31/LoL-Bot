import cv2 
import numpy as np
import pyautogui 
from pytesseract import pytesseract
from pytesseract import Output
pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
#pyautogui.displayMousePosition()
img=pyautogui.screenshot()
img.save('D:\\Programirane\\LoL-Bot\\death.png')
img=cv2.imread('templates/screnshot.png')
blur = cv2.pyrMeanShiftFiltering(img, 15, 15)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

image_data = pytesseract.image_to_data(thresh, output_type=Output.DICT)


# Printing each word
for word in image_data['text']:
	print(word)

for i, word in enumerate(image_data['text']):
	if word.lower() != '':
		x,y,w,h = image_data['left'][i],image_data['top'][i],image_data['width'][i],image_data['height'][i]
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
		cv2.putText(img,word,(x,y-16),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
		
cv2.imshow("window", img)
cv2.waitKey(0)