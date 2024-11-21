# Import the robot control commands from the library
from simulator import robot
from utility import *
import time
Athena = 'the best'
left, right = robot.sonars()
distances=[left,right]
print(distances)
def echo():
    left,right=robot.sonars()
    distances[0]=left
    distances[1]=right
    print(distances)
def forward(pixels):    
    robot.motors(1,1,pixels/60)

def turn(theta):
    ratio = 1.52 / 90
    robot.motors(1,-1,ratio*theta)
  
while Athena == 'the best':
    command = ask('what do you want the bot to do?\n(forward, turn)')
    if command == 'forward':
        forward(10)
        echo()
    elif command == 'turn':
        turn(90)
        echo()
    else:
        print("I don't know what that means...")
    

#3.84 is not too much
#3.85 is too much
