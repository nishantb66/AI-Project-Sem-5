import random

import cv2
from cvzone.HandTrackingModule import HandDetector  #importing the hand detector module from cvzone
import math
import numpy as np
import cvzone
import time


#WEBCAM code
cap = cv2.VideoCapture(0)                            #capturing the video from the webcam
cap.set(3,1920) #prop id number 3 which is width    #setting the width of the video to 1920 pixels
cap.set(4,1080)  #prop id number 4 which is height   #setting the height of the video to 1080 pixels


detector = HandDetector(detectionCon=0.8,maxHands=1) #creating an object of the hand detector class and setting the detection confidence to 0.8 and max hands to 1


x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57] #x coordinates of the hand landmarks of the hand detector
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100] #y coordinates of the hand landmarks of the hand detector
coff = np.polyfit(x,y,2) #fitting a polynomial of degree 2 to the x and y coordinates of the hand landmarks of the hand detector

# Game Variables
cx, cy = 250, 250    #button coordinates
color = (255,0,255)   #button color
counter = 0           #counter variable to count the number of times the button is pressed
score = 0             #score variable to store the score of the game
timeStart = time.time()     #time variable to store the time when the game starts
totalTime = 15                #total time of the game in seconds



#Loop #this is the main loop of the program which runs continuously
while True:
    success, img = cap.read()  #reading the video from the webcam and storing it in img variable and success variable is used to check if the video is read successfully or not

    if time.time()-timeStart < totalTime:       #checking if the time is less than the total time of the game

        hands, img = detector.findHands(img, draw=False)      #finding the hands in the image and storing the image and the hands in the img and hands variable respectively

        if hands:   #checking if the hands are detected or not
            lmList = hands[0]['lmList']       #storing the landmarks of the hand in the lmList variable and landmarks means the points of the hand
            x, y, w, h = hands[0]['bbox']        #storing the bounding box of the hand in the x, y, w and h variable and bounding box means the rectangle around the hand
            if len(lmList) >= 21:             #checking if the number of landmarks is greater than or equal to 21 or not
                x1, y1, _ = lmList[5]         #storing the x and y coordinates of the index finger in x1 and y1 variable respectively
                x2, y2, _ = lmList[17]        #storing the x and y coordinates of the middle finger in x2 and y2 variable respectively


                distance = int(math.sqrt((y2-y1)**2 + (x2-x1)**2))   #calculating the distance between the index finger and the middle finger using the distance formula and storing it in the distance variable
                A, B, C = coff    #storing the coefficients of the polynomial in the A, B and C variable respectively
                distanceCM = A*distance**2 + B*distance + C      #calculating the distance in cm using the polynomial equation and storing it in the distanceCM variable and use of the polynomial is to convert the distance from pixels to cm

                #writing the code for pressing the button and making it green acuratly
                if distanceCM<50:
                    if x < cx < x+w and y < cy < y+h:     #if the button comes inside the box of the hand then the color of the button changes to green
                        counter = 1                         #counter variable is set to 1 to count the number of times the button is pressed

                # print(distanceCM, distance)
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),2)      #drawing the bounding box around the hand and the parameters are image, top left coordinates, bottom right coordinates, color and thickness
                cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10))   #writing the distance in cm on the image and the parameters are image, text, top left coordinates and scale

            if counter:                             #here the color chnage to green and again to purple
                counter +=1                         #counter variable is incremented by 1
                color = (0,255,0)                       #setting the color of the button to green
                if counter == 3:                            #if the counter is equal to 3 then the color of the button is changed to purple and the reason we used 3 is because the button changes to green and then to purple and then again to green
                    cx = random.randint(50,600)         #setting the x coordinate of the button to a random value between 50 and 600
                    cy = random.randint(50,300)     #setting the y coordinate of the button to a random value between 50 and 300
                    color = (255,0,255)                     #setting the color of the button to purple
                    score +=1                               #incrementing the score by 1
                    counter = 0                             #setting the counter to 0



        # Draw Button for the game
        cv2.circle(img, (cx, cy), 20, color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 5, (255,255,255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255,255,255), 2)
        cv2.circle(img, (cx, cy), 20, (50,50,50), 2)

        #Game HUD
        cvzone.putTextRect(img,f'Time: {int(totalTime-(time.time()-timeStart))}',(510,30), scale=1.7)  #time countdown calculation and display on the screen, parameters are image, text, top left coordinates and scale
        cvzone.putTextRect(img,f'Score: {str(score).zfill(2)}',(10,30), scale=1.7)    #score display on the screen

    else:
        cvzone.putTextRect(img, f'Game Over', (200, 200), scale=3, offset=20, thickness=3)             #game over text
        cvzone.putTextRect(img, f'Score: {score}', (225, 300), scale=2.5, offset=10, thickness=2)   #its shows the final score
        cvzone.putTextRect(img, f'Press R to restart', (235, 350), scale=2, offset=5, thickness=2)             #game reset button


    cv2.imshow("Image",img)    #displaying the image on the screen
    key = cv2.waitKey(1)    #waiting for the key to be pressed and the parameter is 1 which means 1 millisecond

    if key == ord('r'):       #if the key pressed is r then the game is restarted
        timeStart = time.time()     #setting the time when the game starts
        score = 0                       #setting the score to 0