# Import the robot control commands from the library
from simulator import robot
import time

robot.motors(1,1,3.84)
left, right = robot.sonars()
#3.84 is not too much
#3.85 is too much
