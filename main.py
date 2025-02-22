# Import the robot control commands from the library
from simulator import *
import numpy as np
from utility import *
import time

Athena = 'the best'
robotAngle = [0]

left, right = robot.sonars()
distances=[left,right]

defaultSteps = ['center', 'left', 'right', 'left', 'forward', 'back', 'forward', 'left', 'right', 'left', 'back', 'forward', 'back', 'right', 'left', 'right', 'back','forward','back', 'right', 'left', 'right', 'back', 'forward', 'back', 'right', 'left', 'right', 'forward', 'back', 'forward', 'left', 'right', 'left']
defaultValues = [0.0, 180.0, 270.0, 90.0, 25.0, 50.0, 25.0, 45.0, 90.0, 45.0, 75.0, 100.0, 25.0, 45.0, 90.0, 45.0, 15 , 30, 15, 180.0, 270.0, 90.0, 25.0, 50.0, 25.0, 45.0, 90.0, 45.0, 75.0, 100.0, 25.0, 45.0, 90.0, 45.0]
dance1Steps = []
dance1Values = []
dance2Steps = []
dance2Values = []
dance3Steps = []
dance3Values = []

#SmallestTooBig : 72
#BiggestTooSmall : 68
sonarsD = 70.5 # the distance between the sonar sensors
boxWidth = 660
boxHeight = 410
ratios = [0.016666666666666666,0.012018542928131136] #[seconds per pixel, #seconds per degree]

def calibrate(sonarsDisplacement):
    print('Calibrating angle...')
    left,right = robot.sonars()
    delta = right-left
    startAngle = np.abs(makeDegrees(np.arctan(delta/sonarsDisplacement)))
    print(f'Initial angle {startAngle} degrees')
    robot.motors(1,-1,1)
    left,right = robot.sonars()
    delta = right-left
    endAngle = np.abs(makeDegrees(np.arctan(delta/sonarsDisplacement)))
    angleDif = endAngle-startAngle
    print(f'turned {angleDif} degrees in 1 second')

    print(f'endAngle:{endAngle} degrees')
    
    angleRatio = 1/angleDif
    ratios[1]=(angleRatio)
    print("Resetting angle...")
    
    robot.motors(-1,1,endAngle*ratios[1])
    print('Calibrating speed...')
    left,right = robot.sonars()
    robot.motors(1,1,1)
    newLeft,newRight = robot.sonars()
    dif = abs(newLeft-left)
    print(f'traveled {dif} in 1 second.')
    print('Resetting position...')
    robot.motors(-1,-1,1)

    ratio = 1/dif
    ratios[0]=ratio
    

    

    print('Calibration complete')
    print(ratios)
def space():
    return min(robot.sonars())-30
def backSpace(): #Not currently operational
    x=robot.driver.x
    y=robot.driver.y
    r=np.sqrt(800)
    h=(robotAngle[0]+180)%360

    W=x    
    E=boxWidth-x
    N=y  
    S=boxHeight-y

    
    return 500-30#not accurate but I will deal with it later
def echo():
    left,right=robot.sonars()
    distances[0]=left
    distances[1]=right
    print(distances)

def forward(pixels):    
    #if pixels < space():
    new_px = pixels
        
   # else: 
    #    new_px = (space())
    robot.motors(1,1,new_px*ratios[0])  
def back(px):
    #if px < backSpace():
    new_px = px
        
    #else: 
       # new_px = (backSpace())
    robot.motors(-1,-1,new_px*ratios[0])  

def turnLeft(theta):
    print(theta)
    print(theta*ratios[1])
    robot.motors(1,-1,theta*ratios[1])
    robotAngle[0]= (robotAngle[0] + theta) % 360
def turnRight(theta):
   
    robot.motors(-1,1,theta*ratios[1])
    robotAngle[0]= (robotAngle[0] - theta) % 360

def faceInDirection(direction):
    x = robotAngle[0]
    direction = direction%360
    angleToTurn = direction-x
    #pretend x is 0
    if direction-x >=0 and direction-x <=180:
        turnLeft(angleToTurn)
    elif direction-x >=180:
        angleToTurn = 360-(direction-x)
    if angleToTurn <0:
        turnRight(abs(angleToTurn))
    robotAngle[0]=direction
def findBearings():
    
    oldFacing = robotAngle[0]
    faceInDirection(0)
    distanceToRight = space()
    faceInDirection(90)
    distanceToTop = space()
    faceInDirection(oldFacing)
    return oldFacing,distanceToRight,distanceToTop


def bounce():
    d = space()
    forward(d)
    while d>=10:
        d*=0.75
        back(d)
        forward(d)
danceCommands = ['run','step','add','delete','print','restart','done']

def center():
        if space() <50:
            back(50-space())
    #--------------vertical------------------#
        faceInDirection(90)
        left,right=robot.sonars()
        distances[0]=left
        distances[1]=right
        if distances[0] >110.27169461830995:
            forward(distances[0]-110.27169461830995)
        elif distances[0] <110.27169461830995:
            back(110.27169461830995-distances[0])  
    #-------------horizontal-----------------#
        faceInDirection(0)
        left,right=robot.sonars()
        distances[0]=left
        distances[1]=right
        if distances[0] != distances[1]:
            pass #The angle is not actually zero
        if distances[0] >260:
            forward(distances[0]-260)
        elif distances[0] <260:
            back(260-distances[0])    
def doAThing(thing,value):
    if thing == 'forward':
        forward(value)
    if thing == 'back':
        back(value)
    if thing == 'left':
        turnLeft(value)
    if thing == 'right':
        turnRight(value)
    if thing == 'face':
        faceInDirection(value)
    if thing == 'center':
        center()
    if thing == 'bounce':
        bounce()

def dance(whichOne,startPoint=0):
    progress = startPoint
    if whichOne == 'default':
        while progress < len(defaultSteps):
            doAThing(defaultSteps[progress],defaultValues[progress])
            progress +=1
    elif whichOne == '1':
        while progress < len(dance1Steps):
            doAThing(dance1Steps[progress],dance1Values[progress])
            progress +=1
    elif whichOne == '2':
        while progress < len(dance2Steps):
            doAThing(dance2Steps[progress],dance2Values[progress])
            progress +=1
    elif whichOne == '3':
        while progress < len(dance3Steps):
            doAThing(dance2Steps[progress],dance2Values[progress])
            progress +=1

stepsIn = [0]
allDances=['default','1','2','3']
allSteps=[defaultSteps,dance1Steps,dance2Steps,dance3Steps]
allValues=[defaultValues,dance1Values,dance2Values,dance3Values]

def writeDance(saveSlot):
    mode = ask('what do you want to do?\n'+str(danceCommands))
    if mode == 'run':
        dance(saveSlot,stepsIn[0])
        stepsIn[0] = len(allSteps[indexInList(saveSlot,allDances)])-1
    if mode == 'step':
        if saveSlot == '1':
            doAThing(dance1Steps[stepsIn[0]],dance1Values[stepsIn[0]])
        if saveSlot == '2':
            doAThing(dance2Steps[stepsIn[0]],dance2Values[stepsIn[0]])
        if saveSlot == '3':
            doAThing(dance3Steps[stepsIn[0]],dance3Values[stepsIn[0]])
        stepsIn[0] +=1
    if mode == 'add':
        insert(ask('what to add?'),stepsIn[0],allSteps[indexInList(saveSlot,allDances)])
        insert(float(ask('number that goes with it?\n(if it doesn\'t need one just put whatever number)')),stepsIn[0],allValues[indexInList(saveSlot,allDances)])
        stepsIn[0] +=1
    if mode == 'delete':
        allSteps[indexInList(saveSlot,allDances)].__delitem__(stepsIn[0]-1)
        allValues[indexInList(saveSlot,allDances)].__delitem__(stepsIn[0]-1)
    if mode == 'print':
        print(allSteps[indexInList(saveSlot,allDances)])
        print(allValues[indexInList(saveSlot,allDances)])
    if mode == 'restart':
        stepsIn[0] = 0
    if mode == 'undo':
        stepsIn[0]-=1
    if mode == 'done':
        return
    writeDance(saveSlot)

commandsBasic=['forward','left','right','back','help','quit']
commandsAdvanced=['face','where','echo','center']
commandsSecret = ['dance','bounce','choreograph']

helpMenu = '''
===============================================================
Basic commands:                                          
    forward - move the robot forward.
        requires input - how far. (units in pixels.)
    back - move the robot backward.
        requires input - how far. (units in pixels.)
    left - turn the robot counterclockwise.
        requires input - what angle. (units in degrees.)
    right - turn the robot clockwise.
        requires input - what angle. (units in degrees.)
    help - brings up this information
    quit - terminates the program.
Advanced commands:
    face - points the robot in a given direction.
        requires input - direction.
    where - returns the robot's position.
        gives output: [angle, distanceToRight, distanceToTop]
    echo - returns sonar readings.
        gives output: [leftSonar,rightSonar]
    center - returns the robot to the center of the screen.
Other commands:
    secret - displays the list of hidden commands.
    dance - the robot returns to center and then performs a choreographed dance.
    bounce - the robot goes forward until it is close to the wall,
        then backward a slightly smaller distance, 
        repeating until it goes less than 10 pixels.
===============================================================
'''
#Setting up shortcuts
face = faceInDirection
l = turnLeft
r = turnRight
fd = forward

calibrate(sonarsD)

#'''
while Athena == 'the best':
    print(f'X:{robot.driver.x}, Y:{robot.driver.y}')
    command = ask('what do you want the bot to do?\n'+str(commandsBasic)+'\n'+str(commandsAdvanced))
    if command == 'help':
        print(helpMenu)
    elif command == 'forward':
        distance = float(ask('How far?'))
        forward(distance)
    elif command == 'back':
        d = float(ask('How far?'))
        back(d)
    elif command == 'left':
        angle=float(ask('What angle?'))
        turnLeft(angle)
    elif command == 'right':
        angle=float(ask('What angle?'))
        turnRight(angle)
    elif command == 'dance':
        chosenOne=ask('which dance?\n[default, 1, 2, 3]')
        if not searchList(chosenOne,['default','1','2','3']):
           print("That's not an option!")
        else:
           dance(chosenOne)      
    elif command == 'bounce':
        bounce()
    elif command == 'center':
        center()
    elif command == 'choreograph':
        stepsIn[0]=0
        writeDance(ask('Which save slot?\n[1, 2, 3]'))
    elif command == 'echo':
        echo()
    elif command == 'quit':
        break
    elif command == 'face':
        newHeading = float(ask('in what direction?'))
        faceInDirection(newHeading%360)
    elif command == 'where':
        angle,distToRight,distToTop = findBearings()
        print(f'The robot is facing {angle} degrees, is {distToRight} pixels from the right, and {distToTop} pixels from the top.')
    elif command == 'secret':
        print("The secret commands are:\n"+str(commandsSecret))
    else:
        print("I don't know what that means... \n try 'help' for a list of commands.")
#'''

'''
debuggging = True
newTry = sonarsD
while debuggging:
    print(newTry)
    calibrate(newTry)
    go = ask('ready to turn left?')
    if searchList(go,YesList):
        turnLeft(90)
    left,right = robot.sonars()
    delta = right-left
    tryAngle = np.abs(makeDegrees(np.arctan(delta/newTry)))
    print(f'it tried to turn 90° but is facing {tryAngle}°')
    newTry = float(ask('new number to try?'))
    turnRight(90)
    quit = ask('done debugging?')
    if searchList(quit,YesList):
        debuggging = False
'''

# - - End - - #
