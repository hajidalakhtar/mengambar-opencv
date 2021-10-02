import os
#import the opencv library
import cv2
import numpy as np
import time
from cvzone.HandTrackingModule import HandDetector
brushThickness = 15
eraserThickness = 50

folderPath = "Header"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)


header = overlayList[1]
drawColor = (255, 0, 255)


# define a video capture object
cap = cv2.VideoCapture(0)


detector = HandDetector(detectionCon=0.85)
xp,yp = 0,0

imgCanvas = np.zeros((480,640,3),np.uint8)
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img)
    if len(hands) == 1:

        lmList = hands[0]["lmList"]
        x1,y1 = lmList[8]
        fingers = detector.fingersUp(hands[0])

        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            l, _, _ = detector.findDistance(lmList[8], lmList[12], img)
            if l < 30:
                print(x1)
                if y1 < 70:
                    if 170 < x1 < 230:
                        # print("warna 1")
                        header = overlayList[1]
                        drawColor = (255, 0, 255)
                    if 280 < x1 < 380:
                        # print("warna 2")
                        header = overlayList[0]
                        drawColor = (0, 0, 255)
                    if 390 < x1 < 480:
                        # print("warna 3")
                        header = overlayList[2]
                        drawColor = (0, 255, 0)
                    if 500 < x1 < 640:
                        drawColor = (0,0,0)
                        header = overlayList[3]

                    # else:
            else:
                print("unselect")
        if fingers[1] and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0  :
            # print("Drwaing mode")
            if xp ==0 and yp ==0:
                xp, yp = x1,y1
            if drawColor == (0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp,yp = x1,y1


    imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray,50,266,cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)

    img[0:70, 0:640] = header
    # img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)