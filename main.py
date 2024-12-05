# Import the robot control commands from the library
from simulator import robot
from utility import *
import time

Athena = 'the best'
robotAngle = [0]

left, right = robot.sonars()
distances=[left,right]

defaultSteps = []
defaultValues = []
dance1Steps = []
dance1Values = []
dance2Steps = []
dance2Values = []
dance3Steps = []
dance3Values = []

boxWidth = 660
boxHeight = 410

def space():
    return min(robot.sonars())
def echo():
    left,right=robot.sonars()
    distances[0]=left
    distances[1]=right
    print(distances)

def forward(pixels):    
    robot.motors(1,1,pixels/60)
def back(px):
    robot.motors(-1,-1,px/60)

def turnLeft(theta):
    ratio = 58.8
    robot.motors(1,-1,theta/ratio)
    robotAngle[0]= (robotAngle[0] + theta) % 360
def turnRight(theta):
    ratio = 58.8
    # 1.5306122449 seconds for 90 degrees
    robot.motors(-1,1,theta/ratio)
    robotAngle[0]= (robotAngle[0] - theta) % 360

def faceInDirection(direction):
    x = robotAngle[0]-direction
    if 180>robotAngle[0]-direction>0:
        turnRight(x)
    else:
        turnLeft(180-x)
    robotAngle[0] = direction
def findBearings():
    
    oldFacing = robotAngle[0]
    faceInDirection(0)
    distanceToRight = min(robot.sonars())
    faceInDirection(90)
    distanceToTop = min(robot.sonars())
    faceInDirection(oldFacing)
    return oldFacing,distanceToRight,distanceToTop

danceCommands = ['write','run','step','add','delete','done']

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
def dance(whichOne,startPoint=0):
    progress = startPoint
    if whichOne == 'default':
        while progress < len(defaultSteps):
            doAThing(defaultSteps[progress],defaultValues[progress])
            progress +=1
    elif whichOne == '1':
        while progress < len(defaultSteps):
            doAThing(dance1Steps[progress],dance1Values[progress])
            progress +=1
    elif whichOne == '2':
        while progress < len(defaultSteps):
            doAThing(dance2Steps[progress],dance2Values[progress])
            progress +=1
    elif whichOne == '3':
        while progress < len(defaultSteps):
            doAThing(dance2Steps[progress],dance2Values[progress])
            progress +=1

stepsIn = 0
allDances=['default','1','2','3']
allSteps=[defaultSteps,dance1Steps,dance2Steps,dance3Steps]
allValues=[defaultValues,dance1Values,dance2Values,dance3Values]

def writeDance(saveSlot):
    mode = ask('what do you want to do?\n'+str(danceCommands))
    if mode == 'run':
        dance(saveSlot,stepsIn)
        stepsIn = len(allSteps[indexInList(saveSlot,allDances)])
    if mode == 'step':
        if saveSlot == '1':
            doAThing(dance1Steps[stepsIn],dance1Values[stepsIn])
        if saveSlot == '2':
            doAThing(dance2Steps[stepsIn],dance2Values[stepsIn])
        if saveSlot == '3':
            doAThing(dance3Steps[stepsIn],dance3Values[stepsIn])
        stepsIn +=1
    if mode == 'add':
        insert(ask('what to add?'),stepsIn,allSteps[indexInList(saveSlot,allDances)])
        insert(ask('number that goes with it?\n(if it doesn\'t need one just put whatever number)'),stepsIn,allValues[indexInList(saveSlot,allDances)])
        stepsIn +=1
    if mode == 'delete':
        allSteps[indexInList(saveSlot,allDances)].__delitem__(stepsIn)
        allValues[indexInList(saveSlot,allDances)].__delitem__(stepsIn)
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

while Athena == 'the best':
    command = ask('what do you want the bot to do?\n'+str(commandsBasic)+'\n'+str(commandsAdvanced))
    if command == 'help':
        print(helpMenu)
    elif command == 'forward':
        distance = 10000
        while distance >= space():
            distance = float(ask('How far?'))
            if distance >= space():
                print("That's too far! the robot will hit the edge!")
        forward(distance)
        echo()
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
        print("I haven't prepared this yet")
    elif command == 'center':
        faceInDirection(0)
        echo()
        if distances[0] != distances[1]:
            pass #The angle is not actually zero
        if distances[0] >260:
            forward(distances[0]-260)
        elif distances[0] <260:
            back(260-distances[0])
        elif distances[0] == 260:
            pass #Already centered
        else:
            print('oh ****')
            break
    elif command == 'echo':
        echo()
    elif command == 'quit':
        break
    elif command == 'face':
        newHeading = float(ask('in what direction?'))
        faceInDirection(newHeading%360)
    elif command == 'where':
        print(findBearings())
    elif command == 'secret':
        print("The secret commands are:\n"+str(commandsSecret))
    else:
        print("I don't know what that means... \n try 'help' for a list of commands.")


# - - End - - #
