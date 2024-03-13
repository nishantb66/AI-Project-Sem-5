import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone

#WEBCAM code
cap = cv2.VideoCapture(0)
cap.set(3,1280) #prop id number 3 which is width
cap.set(4,720)  #prop id number 4 which is height

#HAND DECTECTOR
detector = HandDetector(detectionCon=0.8,maxHands=1)  #here we have used handdetector with 0.8 i.e is 80% sure and number hands detect is 1

#Find function
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x,y,2) #y = Ax^2 + Bx + C


#Loop
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img,draw=False)   #passing image in detector

    #lets check if hand is there and we are using lmlist
    if hands:
        lmList = hands[0]['lmList']  #lmList will give us the list of all points that appears in the cam
        x, y, w, h = hands[0]['bbox']  #hands under a bounding box
        # print(lmList)
        #To find the distance between palm we need distance between point 5 and point 17
        # Check if lmList contains at least 2 values
        # if len(lmList) >= 17:
        #     x1, y1 = lmList[8][1], lmList[8][2]  # Index finger tip (point 8)
        #     x2, y2 = lmList[0][1], lmList[0][2]  # Palm base (point 0)
        #     print(abs(x2 - x1))
        if len(lmList) >= 21:
            x1, y1, _ = lmList[5]
            x2, y2, _ = lmList[17]

            distance = int(math.sqrt((y2-y1)**2 + (x2-x1)**2))  #this is to fix the distnace reduction when we rotate the hand.
            A, B, C = coff
            distanceCM = A*distance**2 + B*distance + C  #Ax^2 + Bx + C

            # print(distanceCM, distance)
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),3)
            cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10))  #distance of the hand from camera


            #as we move our hand way from the cam the difference is not linearly changing, to solve this and obtain more acurate vallue we have to make the relation linear which can be done by second degree polynomial.



    cv2.imshow("Image",img)
    cv2.waitKey(1)