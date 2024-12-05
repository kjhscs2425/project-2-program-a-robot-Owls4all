# Import the robot control commands from the library
from simulator import robot
from utility import *
import time
Athena = 'the best'
robotAngle = [0]
left, right = robot.sonars()
distances=[left,right]
print(distances)

boxWidth = 660
boxHeight = 410

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
    faceInDirection[0]
    distanceToRight = min(robot.sonars())
    faceInDirection(90)
    distanceToTop = min(robot.sonars())
    faceInDirection(oldFacing)
    return oldFacing,distanceToRight,distanceToTop

commandOptions=['forward','left','right','back','face','where','quit']


while Athena == 'the best':
    command = ask('what do you want the bot to do?\n'+str(commandOptions))
    if command == 'forward':
        distance = 10000
        while distance >= min(distances):
            distance = float(ask('How far?'))
            if distance >= min(distances):
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
        print("I haven't prepared this yet")
    elif command == 'center':
        if 180 >= robotAngle[0] > 0:
            turnRight(robotAngle[0])
        elif 180 < robotAngle[0] < 360:
            turnLeft(robotAngle[0]-180)
        elif robotAngle[0] == 0:
            pass #(Already at correct angle)
        else:
            print('oh ****')
            break
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
        print(findBearings)
    else:
        print("I don't know what that means...")


# - - End - - #
