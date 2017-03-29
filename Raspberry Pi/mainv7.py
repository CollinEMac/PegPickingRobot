# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import time
import serial
import numpy as np
import cv2

###########COMMUNICATION KEY##############
##MOTOR SHIELD COMMUNICATION:
#a = RightTurn
#b = LeftTurn
#c = RightWall
#d = LeftWall
#e = FrontAdj
#f = Forward
#g = RightAdj
#h = LeftAdj
#i = Stop
#j = Neutral
#k = ArmUp
#l = ArmDown
#m = GripperOpen
#n = GripperClose
#o = gripperOpenSlightly
#p = reverse
#q = Turf Front ADJ
#r = Turf Left ADJ
#s = Turf Right ADJ
#Z = reset Arduino
##SENSOR COMMUNICATION:
#a = Read Sensor1 (front driver side)
#b = Read Sensor2 (rear driver side)
#c = Read Sensor3 (front passenger side)
#d = Read Sensor4 (read passenger side)
#e = Read Sensor5 (front)
#f = Blink LED
#Z = reset Arduino
###########COMMUNICATION KEY##############

#Initialize Serial Communication to Arduino Boards
serMotor = serial.Serial('/dev/ttyUSB0', 9600)
serSensor = serial.Serial('/dev/ttyACM0', 9600)

#Initialize camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(640, 480))

#IMPORTANT CAMERA SETTINGS
camera.awb_mode = 'off'
camera.awb_gains = (0.9, 1.9)

time.sleep (0.1)

# create NumPy array thresholds
###
#H: 0-180
#S: 0-255
#V: 0-255
###

redLower = np.array([0,50,50]) 
redUpper = np.array([15,245,255])

yellowLower = np.array([20,200,100])
yellowUpper = np.array([42,255,245])

##############FUNCTIONS#######################

def forward(delay):
    serMotor.write('f')
    time.sleep(delay)
    if (delay > 0):
        stop()
    #MOVE FORWARD

def forwardTurf(delay):
    serMotor.write('v')
    time.sleep(delay)
    if (delay > 0):
        stop()
    #MOVE FORWARD

def left(delay):
    serMotor.write('t')
    time.sleep(delay)
    stop()

def right(delay):
    serMotor.write('u')
    time.sleep(delay)
    stop()
    
def reverse(delay):
    serMotor.write('p')
    time.sleep(delay)
    if (delay > 0):
        stop()

def stop():
    serMotor.write('i')
    time.sleep(0.6)
    serMotor.write('j')
    #PUMP BRAKES

def parallelLeft(turf):
    p = 0
    while (p<2):
        sensor1 = 0
        sensor2 = 0
        for i in range(1,3):
            serSensor.write('a')
            sensor1 = sensor1 + int(serSensor.readline())
            serSensor.write('b')
            sensor2 = sensor2 + int(serSensor.readline())

        sensor1 = sensor1/2
        sensor2 = sensor2/2
        sensorDifference = sensor1 - sensor2
        if (turf==0):
            if (sensorDifference > 40):
                serMotor.write('h')
                #LEFT ADJUST
            elif (sensorDifference < -40):
                serMotor.write('g')
                #RIGHT ADJUST
            else:
                p=p+1
                #WE ARE PARALLEL
        elif (turf==1):
            if (sensorDifference > 40):
                serMotor.write('r')
                #LEFT ADJUST
            elif (sensorDifference < -40):
                serMotor.write('s')
                #RIGHT ADJUST
            else:
                p=p+1
                #WE ARE PARALLEL
    stop()    

def parallelRight(turf):
    p = 0
    while (p<2):
        sensor3 = 0
        sensor4 = 0
        for i in range(1,3):
            serSensor.write('c')
            sensor3 = sensor3 + int(serSensor.readline())
            serSensor.write('d')
            sensor4 = sensor4 + int(serSensor.readline())

        sensor3 = sensor3/2
        sensor4 = sensor4/2
        sensorDifference = sensor3 - sensor4
        if (turf==0):
            if (sensorDifference > 40):
                serMotor.write('g')
                #RIGHT ADJUST
            elif (sensorDifference < -40):
                serMotor.write('h')
                #LEFT ADJUST
            else:
                p=p+1
                #WE ARE PARALLEL
        elif (turf==1):
            if (sensorDifference > 40):
                serMotor.write('s')
                #RIGHT ADJUST
            elif (sensorDifference < -40):
                serMotor.write('r')
                #LEFT ADJUST
            else:
                p=p+1
                #WE ARE PARALLEL
    stop()
    
def sensor2GapRead(turf):
    #MOVE FORWARD UNTIL BACK SENSOR SEES GAP
    if (turf == 0):
        forward(0)
    else:
        forwardTurf(0)
    
    sensor2 = 0

    while (sensor2 < 1500):
        serSensor.write('b')
        sensor2 = int(serSensor.readline())
    stop()

def sensor1GapRead():
    #MOVE FORWARD UNTIL BACK SENSOR SEES GAP
    sensor1 = 0

    while (sensor1 < 1500):
        serSensor.write('a')
        sensor1 = int(serSensor.readline())
    stop()

def sensor4GapRead():
    #MOVE FORWARD UNTIL BACK SENSOR SEES GAP
    sensor4 = 0

    while (sensor4 < 1500):
        serSensor.write('d')
        sensor4 = int(serSensor.readline())
    stop()
    
def sensor5WallRead(distance):
    #MOVE FORWARD UNTIL FRONT SENSOR IS CLOSE TO WALL
    p=0
    while (p<2):
        forward(0)
        sensor5 = 10000

        while (sensor5 > distance):
            serSensor.write('e')
            sensor5 = int(serSensor.readline())
        stop()
        p=p+1
    
def sensor5BackUp(distance):
    #MOVE BACKWARD UNTIL FRONT SENSOR IS DISTANCE FROM WALL
    reverse(0)
    sensor5 = 0

    while (sensor5 < distance):
        serSensor.write('e')
        sensor5 = int(serSensor.readline())
    stop()
    
def wallFollowRight(j):

    for i in range (0,j):
        serSensor.write('c')
        sensor3 = int(serSensor.readline())
        serSensor.write('d')
        sensor4 = int(serSensor.readline())
        sensorMean = (sensor3 + sensor4)/2  

        if (sensorMean > 310): #~2 inches
            serMotor.write('c')
            
        if (sensorMean < 290):
            serMotor.write('d')

        time.sleep(.05)
        i=i+1
    stop()

def wallFollowRightFar(j):

    for i in range (0,j):
        serSensor.write('c')
        sensor3 = int(serSensor.readline())
        serSensor.write('d')
        sensor4 = int(serSensor.readline())
        sensorMean = (sensor3 + sensor4)/2  

        if (sensorMean > 440): 
            serMotor.write('c')
            
        if (sensorMean < 430):
            serMotor.write('d')

        time.sleep(.05)
        i=i+1
    stop()
    
def wallFollowLeft(j):

    for i in range (0,j):
        serSensor.write('a')
        sensor1 = int(serSensor.readline())
        serSensor.write('b')
        sensor2 = int(serSensor.readline())
        
        sensorMean = (sensor1 + sensor2)/2  

        if (sensorMean > 305): #~2 inches
            serMotor.write('d')
            
        if (sensorMean < 295):
            serMotor.write('c')

        time.sleep(.05)
        i=i+1
    stop()
    
def wallFollowLeftFar(j):

    for i in range (0,j):
        serSensor.write('a')
        sensor1 = int(serSensor.readline())
        serSensor.write('b')
        sensor2 = int(serSensor.readline())
        
        sensorMean = (sensor1 + sensor2)/2  

        if (sensorMean > 440): 
            serMotor.write('d')
            
        if (sensorMean < 430):
            serMotor.write('c')

        time.sleep(.05)
        i=i+1
    stop()
        
def findVictim(inTurf):

    VictimColor = 'N'
    noVictimCount = 0
    biggestCnt = np.empty(2)
    biggestCnt[:] = 0

    
    #NEED TO BE ABLE TO BREAK FROM THIS LOOP WHEN VICTIM IS IN RANGE 
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #Capture Image
        image = frame.array

        #CONVERT TO HSV
        hsv_Image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
         
        # find the colors within the specified boundaries and apply the mask
        redMask = cv2.inRange(hsv_Image, redLower, redUpper)
        redOutput = cv2.bitwise_and(hsv_Image, hsv_Image, mask= redMask)
        yellowMask = cv2.inRange(hsv_Image, yellowLower, yellowUpper)
        yellowOutput = cv2.bitwise_and(hsv_Image, hsv_Image, mask= yellowMask)

        #FINDING CONTOURS
        rcnts = cv2.findContours(redMask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        ycnts = cv2.findContours(yellowMask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
                
        #If we have red and yellow contours on the screen at once
        #Set the biggest contour (of either color) as biggestCnt
        if (len(rcnts) > 0) or (len(ycnts) > 0):

            if (len(rcnts) > 0) and (len(ycnts) < 1):
                victimColor = 'R'

            elif (len(ycnts) > 0) and (len(rcnts) < 1):
                victimColor = 'Y'

            elif (len(ycnts) > 0) and (len(rcnts) > 0):

                for i in range(0, len(rcnts)):
                    x,y,w,h = cv2.boundingRect(rcnts[i])
                    
                    if (cv2.contourArea(rcnts[i]) > 500) and (y < 300):
                        rbigCnt = rcnts[i]
                        biggestCnt = rbigCnt
                        victimColor = 'R'
                        #Set biggestCnt as the biggest Red Contour
                        #That meets the conditions
                        
                for i in range(0, len(ycnts)):
                    x,y,w,h = cv2.boundingRect(ycnts[i])
                        
                    if (cv2.contourArea(ycnts[i]) > 500) and (y < 300):
                            ybigCnt = ycnts[i]
                            biggestCnt = ybigCnt
                            victimColor = 'Y'
                            #Set the biggestCnt as the biggest yellow contour
                            #that meets the conditions

                
            #LOOP THROUGH RED CNTS
            if len(rcnts) > 0: 
                for i in range(0, len(rcnts)):
                    x,y,w,h = cv2.boundingRect(rcnts[i])
                    
                    if (cv2.contourArea(rcnts[i]) > 500) and (y < 300):
                        rbigCnt = rcnts[i]
                        biggestCnt = rbigCnt
                        #Set biggestCnt as the biggest Red Contour
                        #That meets the conditions

            if len(ycnts) > 0:
                for i in range(0, len(ycnts)):
                    x,y,w,h = cv2.boundingRect(ycnts[i])
                
                    if (cv2.contourArea(ycnts[i]) > 500) and (y < 300):
                        ybigCnt = ycnts[i]
                        biggestCnt = ybigCnt
                        #Set the biggestCnt as the biggest yellow contour
                        #that meets the conditions    

        else:
            noVictimCount = noVictimCount + 1
            if (noVictimCount > 9):
                victimColor = 'N'
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
                return victimColor

        if (biggestCnt.all() == 0):
            noVictimCount = noVictimCount + 1
            if (noVictimCount > 9):
                victimColor = 'N'
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
                return victimColor
        else:
            X,Y,W,H = cv2.boundingRect(biggestCnt)
            
            #Make turns based on the position of the center of the shape
            if (inTurf == 0):
            #City section
                if (X+(W/2) > 350): 
                    serMotor.write('h')
                    #print('LEFT')
                elif(X+(W/2) < 290):
                    serMotor.write('g')
                    #print('RIGHT')
                else:
                    serMotor.write('e')
                    #print('FORWARD')

            else:
            #Field Section
                if(X+(W/2) > 340) and (W < 90):
                    serMotor.write('h')
                    #print('TURF LEFT')
                elif(X+(W/2) < 300) and (W < 90):
                    serMotor.write('g')
                    #print('TURF RIGHT')
                elif (300 < X+(W/2) < 340) and (W < 90):
                    serMotor.write('q')
                    #print('TURF FORWARD')
                elif (X+(W/2) > 340) and (W >= 90): 
                    serMotor.write('h')
                    #print('LEFT')
                elif(X+(W/2) < 300) and (W >= 90):
                    serMotor.write('g')
                    #print('RIGHT')
                else:
                    serMotor.write('e')
                    #print('forward')

            #Exit the while loop
            if (W > 200):
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
                return victimColor
                    
        # show the images
        #cv2.imshow("image", image)
        #cv2.waitKey(1)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

def pickUpVictim():
    serMotor.write('m')
    time.sleep(1.7)
    serMotor.write('l')
    time.sleep(1.7)
    serMotor.write('n')
    time.sleep(1.7)
    serMotor.write('k')
    time.sleep(1.7)
    serMotor.write('o')
    time.sleep(1.7)
    
    
def dropVictim():
    serMotor.write('m')
    time.sleep(.75)
    serMotor.write('l')
    time.sleep(.75)
    serMotor.write('k')
    time.sleep(.75)

def returnVictim(victimColor):
    #Start in front of yellow area facing towards it
    #Drop off in yellow area and face away from yellow drop off area
    parallelLeft(0)
    forward(0)
    sensor1GapRead()
    parallelRight(0)
    
    if (victimColor == 'Y'):
        sensor5WallRead(1100)
        dropVictim()
        reverse(0)
        sensor1GapRead()
        parallelRight(0)
        left(1.1)
        
    #Drop off in red area and return to yellow drop off area facing away
    elif (victimColor == 'R'):
        forward(0)
        sensor2GapRead(0)
        left(0.6)
        reverse(.4)
        stop()
        ##parallelRight(0)
        sensor5WallRead(800)
        left(0.6)
        parallelRight(0)
        forward(1.5)
        stop()
        forward(0)
        wallFollowLeftFar(10)
        parallelLeft(0)
        wallFollowLeftFar(11)
        parallelLeft(0)
        sensor5WallRead(1100)
        dropVictim()
        reverse(0)
        sensor5BackUp(2072)
        right(1.4)
        parallelRight(0)
        forward(0)
        wallFollowRightFar(10)
        parallelRight(0)
        wallFollowRightFar(11)
        parallelRight(0)
        forward(0)
        sensor4GapRead()
        right(0.7)
        parallelLeft(0)
        sensor5WallRead(475)

        time.sleep(0.5)
        sensor5WallRead(400)
        right(0.7)

    else:
        forward(0)
        sensor2GapRead(0)
        parallelRight(0)
        left(1.2)
        
    parallelLeft(0)


def backToStart(victimColor):
    parallelLeft(0)
    right(.7)
    parallelRight(0)
    sensor5WallRead(500)
    right(.7)
    parallelLeft(0)
    sensor5WallRead(500)
    
        
def fieldFar():
    forward(1.5)
    wallFollowRight(20)
    parallelRight(0)
    parallelRight(0)
    forward(0)
    sensor1GapRead()
    left(.1)
    forward(0)
    sensor2GapRead(0)
    right(0.75)
    sensor5WallRead(400)
    parallelLeft(0)
    reverse(0)
    sensor5BackUp(3300)
    parallelLeft(0)
    left(.85)
    forward(0)
    sensor5WallRead(450)
    left(.6)
    parallelRight(0)
    forwardTurf(.6)
    stop()

def fieldFarToHome():
    parallelLeft(1)
    right(.8)
    parallelLeft(1)
    sensor2GapRead(1)
    left(.7)
    reverse(0.5)
    parallelLeft(1)
    sensor5WallRead(500)
    parallelLeft(0)
    right(.82)
    parallelLeft(0)
    wallFollowLeft(19)
    parallelLeft(0)
    
########FUNCTIONS######################

###BEGINNING OF PROCESS!!!
###START LOCATION

serSensor.write('f')
#LIGHT ARDUINO LED

#WAIT FOR BUTTON PRESS ON MOTOR BOARD
start = serMotor.readline()


parallelRight(0)
sensor2GapRead(0)
left(0.6)
parallelLeft(0)
for i in range(1,3):
    forward(0)
    sensor5WallRead(500)
    
#IN FRONT OF YELLOW DROP OFF ZONE
    
right(0.75)
parallelLeft(0)
forward(1.6)

parallelRight(0)
forward(0)
wallFollowRight(22)
parallelRight(0)
sensor5WallRead(1650)
parallelRight(0)

#At first victim!
victimColor = findVictim(0)
pickUpVictim()
#pick up first victim!
parallelRight(0)
reverse(0.6)

parallelRight(0)

left(1.15)
#turn around

parallelLeft(0)
forward(0)
wallFollowLeft(20)
parallelLeft(0)

returnVictim(victimColor)
###DROP OFF FIRST VICTIM

######################################################################

##CHECK FIRST FIELD VICTIM
left(.05)
forward(0)

sensor1GapRead()
left(.1)
forward(0)
sensor2GapRead(0)
parallelRight(0)
right(0.77)
reverse(5.25)
#sensor5BackUp(3300)
right(0.8)
    
forward(2.15)
#right(0.2)
##parallelLeft(1)
right(0.1)
victimColor = findVictim(1)

#If we don't see a victim
if (victimColor == 'N'):
    leftFieldCount = 0
    left(0.1)
    
    #Still no victim time to go to second victim
    parallelLeft(0)
    reverse(0)
    sensor1GapRead()
    left(0.7)
    sensor5WallRead(1875)
    right(.85)
    
    
#IF WE SEE A VICTIM
else:
    leftFieldCount = 1
    #WE FOUND THE LEFT FIELD VICTIM
    
    pickUpVictim()
    parallelLeft(0)
    
    left(.8)
    parallelRight(0)
    sensor5WallRead(400)
    left(.8)
    parallelRight(0)
    forward(0)
    sensor4GapRead()
    #####RISKY TURN ;)
    right(.9)
    sensor5WallRead(425)
    right(.85)
    parallelLeft(0)
    returnVictim(victimColor)
    forward(0)
    sensor1GapRead()
    serMotor.write('h')
    time.sleep(0.25)
    serMotor.write('h')
    time.sleep(0.25)
    forward(0)
    sensor2GapRead(0)
    parallelRight(0)

    right(0.7)
    #parallelRightFar()
    sensor5BackUp(1776)
    right(0.725)

#################################################################################

##PICK UP SECOND CITY VICTIM

victimColor = findVictim(1)
stop()
pickUpVictim()
parallelLeft(0)

reverse(0)
sensor1GapRead()
parallelLeft(0)
left(0.6)
#parallelRightFar()
forward(0)
sensor5WallRead(475)
right(0.7)
parallelLeft(0)

returnVictim(victimColor)
######RETURN SECOND CITY VICTIM
######################################################################
##peg3333 (SECOND FIELD VICTIM)
fieldFar()
left(.2)
forward(1)
victimColor = findVictim(1)
pickUpVictim()
right(.2)
parallelRight(1)

#If it's in the close location, let's make sure we don't hit the wall
serSensor.write('e')
sensor5 = int(serSensor.readline())
if (sensor5 > 2100):
    wallFollowRightFar(8)

sensor5WallRead(500)
right(.9)
parallelLeft(1)
sensor5WallRead(500)
right(.9)
parallelLeft(1)
wallFollowLeft(15)
parallelLeft(1)
sensor5WallRead(500)

fieldFarToHome()
if (leftFieldCount == 1):
    #IF WE ALREADY GOT THE LEFT VICTIM
    returnVictim(victimColor)
    backToStart(victimColor)
else:
    returnVictim(victimColor)

    ##########GET LAST VICTIM IF WE NEED TO
    fieldFar()    #FAR RIVER PEG
    parallelRight(1)
    wallFollowRightFar(16)
    parallelRight(1)
    left(.2)

    forwardTurf(0)
    sensor5WallRead(700)
    left(.7)
    parallelRight(1)
    forwardTurf(.5)
    wallFollowRightFar(32)
    parallelRight(1)
    left(.15)
    victimColor = findVictim(1)
    pickUpVictim()
    right(.3)
    parallelRight(1)
    right(.9)
    parallelLeft(1)
    forwardTurf(0)
    sensor5WallRead(700)
    parallelLeft(1)
    right(.8)
    parallelLeft(1)
    forwardTurf(0)
    wallFollowLeftFar(32)
    right(.3)
    forwardTurf(0)
    sensor5WallRead(800)
    parallelLeft(1)
    right(.8)
    parallelLeft(1)
    forwardTurf(0)
    wallFollowLeft(8)
    parallelLeft(1)
    wallFollowLeft(8)
    parallelLeft(1)
    forward(0)
    sensor5WallRead(750)
    parallelLeft(1)

    fieldFarToHome()
    returnVictim(victimColor)
    backToStart(victimColor)
