import cv2
import dlib
import time
from datetime import datetime
import os
import numpy as np

#CLASSIFIER FOR DETECTING CARS--------------------------------------------------
carCascade = cv2.CascadeClassifier('cars.xml')


#TAKE VIDEO---------------------------------------------------------------------
video = cv2.VideoCapture('highway12.mp4')

WIDTH = 1280 #WIDTH OF VIDEO FRAME
HEIGHT = 720 #HEIGHT OF VIDEO FRAME
cropBegin = 240 #CROP VIDEO FRAME FROM THIS POINT
mark1 = 120 #MARK TO START TIMER
mark2 = 360 #MARK TO END TIMER
markGap = 25 #DISTANCE IN METRES BETWEEN THE MARKERS
fpsFactor = 3 #TO COMPENSATE FOR SLOW PROCESSING
speedLimit = 35 #SPEEDLIMIT
startTracker = {} #STORE STARTING TIME OF CARS
endTracker = {} #STORE ENDING TIME OF CARS
font = cv2.FONT_HERSHEY_PLAIN

#result = cv2.VideoWriter('speed_detection_1.mp4', cv2.VideoWriter_fourcc('M','J','P','G'),5, (1280, 720))  # write video

#FUNCTION TO CALCULATE SPEED----------------------------------------------------
def estimateSpeed(carID):
    timeDiff = endTracker[carID]-startTracker[carID]
    speed = round(markGap/timeDiff*fpsFactor*1,2)
    return speed

#FUNCTION TO TRACK CARS---------------------------------------------------------
def trackMultipleObjects():
    rectangleColor = (0, 255, 0)
    changeColor = (255,48,255)
    frameCounter = 0
    currentCarID = 0
    carTracker = {}
    displayspeed=0
    lawbroken=False
    getID =0
    grantID = False

    while True:
        rc, image = video.read()
        if type(image) == type(None):
            break

        frameTime = time.time()
        image = cv2.resize(image, (WIDTH, HEIGHT))
        resultImage = image
        cv2.line(resultImage,(450,mark1),(750,mark1),(0,0,255),2)
        cv2.line(resultImage,(280,mark2),(850,mark2),(0,0,255),2)

        frameCounter = frameCounter + 1

        #DELETE CARIDs NOT IN FRAME---------------------------------------------
        carIDtoDelete = []

        for carID in carTracker.keys():
            trackingQuality = carTracker[carID].update(image)

            if trackingQuality < 7:
                carIDtoDelete.append(carID)

        for carID in carIDtoDelete:
            carTracker.pop(carID, None)

        #MAIN PROGRAM-----------------------------------------------------------
        if (frameCounter%20 == 0):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24)) #DETECT CARS IN FRAME

            for (_x, _y, _w, _h) in cars:
                #GET POSITION OF A CAR
                x = int(_x)
                y = int(_y)
                w = int(_w)
                h = int(_h)

                xbar = x + 0.5*w
                ybar = y + 0.5*h

                matchCarID = None

                #IF CENTROID OF CURRENT CAR NEAR THE CENTROID OF ANOTHER CAR IN PREVIOUS FRAME THEN THEY ARE THE SAME
                for carID in carTracker.keys():
                    trackedPosition = carTracker[carID].get_position()

                    tx = int(trackedPosition.left())
                    ty = int(trackedPosition.top())
                    tw = int(trackedPosition.width())
                    th = int(trackedPosition.height())

                    txbar = tx + 0.5 * tw
                    tybar = ty + 0.5 * th
                    print("txbar = ",txbar)
                    print("tybar = ",tybar)

                    if ((tx <= xbar <= (tx + tw)) and (ty <= ybar <= (ty + th)) and (x <= txbar <= (x + w)) and (y <= tybar <= (y + h))):
                        matchCarID = carID


                if matchCarID is None:
                    tracker = dlib.correlation_tracker()
                    tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))

                    carTracker[currentCarID] = tracker

                    currentCarID = currentCarID + 1
                    
        ##displayspeed=0


        for carID in carTracker.keys():
            trackedPosition = carTracker[carID].get_position()
          
            
            tx = int(trackedPosition.left())
            ty = int(trackedPosition.top())
            tw = int(trackedPosition.width())
            th = int(trackedPosition.height())

            #PUT BOUNDING BOXES-------------------------------------------------
            cv2.rectangle(resultImage, (tx, ty), (tx + tw, ty + th), rectangleColor, 2)
            cv2.putText(resultImage, str(carID), (tx,ty-5), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 1)
            
           

            #ESTIMATE SPEED-----------------------------------------------------
            if carID not in startTracker and mark1 < ty+th < mark2 and ty+th < mark2 and (tx>=455 and tx<=850):
                startTracker[carID] = frameTime
                cv2.line(resultImage,(280,mark2),(850,mark2),(0,255,0),2)
                cv2.rectangle( resultImage, (tx, ty), (tx + tw, ty + th), changeColor, 2)

               
            elif carID in startTracker and carID not in endTracker and mark1 > ty+th and (tx>=450 and tx<=750):
                endTracker[carID] = frameTime
                speed = estimateSpeed(carID)
                getID = carID
                displayspeed=speed
                cv2.line(resultImage,(450,mark1),(750,mark1),(0,255,0),2)
                cv2.rectangle( resultImage, (tx, ty), (tx + tw, ty + th), changeColor, 2)
                if speed > speedLimit:
                    print('CAR-ID : {} : {} kmph - OVERSPEED'.format(carID, speed))
                    lawbroken=True
                else:
                    print('CAR-ID : {} : {} kmph'.format(carID, speed))
                    lawbroken=False
                    grantID = True
                   
                    
        if(lawbroken==True):
            cv2.putText(resultImage,'Last known OVERSPEED CAR-ID : {} : {} kmph'.format(getID, speed),(50,250),font,fontScale=1.5, color=(0,255,0),thickness=1)
        if(grantID==True and lawbroken==False):
            cv2.putText( resultImage,'Last known CAR-ID : {} : {} kmph'.format(getID,displayspeed),(50,300),font,fontScale=1.5, color=(0,255,0),thickness=1)
        cv2.putText(resultImage,"Speed limit in (kmph):"+str(speedLimit),(50,200),font,fontScale=1.5, color=(0,255,0),thickness=1) 
                    
            
    

        #DISPLAY EACH FRAME
        cv2.imshow('result', resultImage)
        ##result.write(resultImage)
       


        if cv2.waitKey(33) == 27:
            break
            
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    trackMultipleObjects()
