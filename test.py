import random

import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time


#WEBCAM code
cap = cv2.VideoCapture(0)
cap.set(3,1920) #prop id number 3 which is width
cap.set(4,1080)  #prop id number 4 which is height


detector = HandDetector(detectionCon=0.8,maxHands=1)


x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x,y,2)

# Game Variables
cx, cy = 250, 250
color = (255,0,255)
counter = 0
score = 0
timeStart = time.time()  #time
totalTime = 60


#Loop
while True:
    success, img = cap.read()

    if time.time()-timeStart < totalTime:

        hands, img = detector.findHands(img, draw=False)

        if hands:
            lmList = hands[0]['lmList']
            x, y, w, h = hands[0]['bbox']

            x1, y1, _ = lmList[5]
            x2, y2, _ = lmList[17]

            distance = int(math.sqrt((y2-y1)**2 + (x2-x1)**2))
            A, B, C = coff
            distanceCM = A*distance**2 + B*distance + C

                #writing the code for pressing the button and making it green acuratly
            if distanceCM<50:
                if x < cx < x+w and y < cy < y+h:     #if the button comes inside the box
                    counter = 1

                # print(distanceCM, distance)
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)
            cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10))

            if counter:                             #here the color chnage to green and gain to purple
                counter +=1
                color = (0,255,0)  #green
                if counter == 3:
                    cx = random.randint(50,600)
                    cy = random.randint(50,300)
                    color = (255,0,255)
                    score +=1
                    counter = 0



        # Draw Button for the game
        cv2.circle(img, (cx, cy), 20, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 5, (255,255,255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255,255,255), 2)
        cv2.circle(img, (cx, cy), 20, (50,50,50), 2)

        #Game HUD
        cvzone.putTextRect(img,f'Time: {int(totalTime-(time.time()-timeStart))}',(510,30), scale=1.7)  #time countdown calculation
        cvzone.putTextRect(img,f'Score: {str(score).zfill(2)}',(10,30), scale=1.7)    #score field

    else:
        cvzone.putTextRect(img, f'Game Over', (200, 200), scale=3, offset=20, thickness=3)      #
        cvzone.putTextRect(img, f'Score: {score}', (225, 300), scale=2.5, offset=10, thickness=2)   #its shows the final score
        cvzone.putTextRect(img, f'Press R to restart', (235, 350), scale=2, offset=5, thickness=2)             #game reset button


    cv2.imshow("Image",img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        timeStart = time.time()
        score = 0
