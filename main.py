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
    ratio = 1.5 / 90#was 1.52
    robot.motors(1,-1,ratio*theta)
    robotAngle[0]= (robotAngle[0] + theta) % 360
def turnRight(theta):
    ratio = 1.5 / 90
    robot.motors(-1,1,ratio*theta)
    robotAngle[0]= (robotAngle[0] - theta) % 360

commandOptions=['forward','left','right','back','quit']
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
        echo()
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

    else:
        print("I don't know what that means...")


potatoes = 'cool'
