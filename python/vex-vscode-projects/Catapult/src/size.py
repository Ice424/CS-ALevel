#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
# vex-vision-config:begin
vision_11__SIG_1 = Signature(1, -2665, -1357, -2011,-6153, -4663, -5408,2.5, 0)
vision_11 = Vision(Ports.PORT11, 40, vision_11__SIG_1)
# vex-vision-config:end
left_drive_smart = Motor(Ports.PORT1, 1.0, False)
right_drive_smart = Motor(Ports.PORT6, 1.0, True)

optical_12 = Optical(Ports.PORT12)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)

catupult_motor = Motor(Ports.PORT2, 1.0, False )

distance_7 = Distance(Ports.PORT7)

# generating and setting random seed
def initializeRandomSeed():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    systemTime = brain.timer.system() * 100
    urandom.seed(int(xaxis + yaxis + zaxis + systemTime)) 
    
# Initialize random seed 
initializeRandomSeed()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()
start_rot = 0
def start_left():
    global start_rot 
    start_rot = -90
    when_started1()

def start_right():
    global start_rot 
    start_rot = 90
    when_started1()

def when_started1():
    drivetrain.drive_for(FORWARD, 6.5, INCHES)
    global start_rot 
    distances = [123,78,40,30,18]
    optimal_distance = 20
    vexcode_vision_11_objects = []
    list_widths = [0]
    drivetrain.turn_to_rotation(start_rot, velocity=10, wait=False)
    while drivetrain.is_turning():
        vexcode_vision_11_objects = vision_11.take_snapshot(vision_11__SIG_1)
        brain.screen.clear_screen()
        if vexcode_vision_11_objects:
            brain.screen.set_cursor(1, 1)
            brain.screen.print(vexcode_vision_11_objects[0].width)
            list_widths.append(vexcode_vision_11_objects[0].width)

        brain.screen.set_cursor(2, 1)
        brain.screen.print(drivetrain.is_turning())



    list_widths.sort()
    brain.screen.clear_screen()
    brain.screen.set_cursor(2, 1)
    distance = min(distances, key=lambda x:abs(x-list_widths[-1]))

    pos = distances.index(distance)

    brain.screen.print(list_widths[-1])
    brain.screen.set_cursor(3, 1)
    brain.screen.print(pos)

    drivetrain.turn_to_rotation(0)

    drivetrain.drive_for(FORWARD, 12*(pos+1), INCHES)
    if start_rot > 0:
        drivetrain.drive_for(FORWARD, 4, INCHES)
    else:
        pass
        #drivetrain.drive_for(REVERSE, 2, INCHES)
    drivetrain.turn_to_rotation(start_rot)

    drivetrain.drive_for(FORWARD, 18, INCHES)
    sleep(1.2, SECONDS)
    brain.screen.set_cursor(4, 1)
    if optical_12.brightness() >= 50:
        brain.screen.print("red")
        target = "red"
        offset = -3
    else:
        brain.screen.print("green")
        target = "green"
        offset = 2
    
    if start_rot < 0:
        offset = -offset
    
    drivetrain.drive_for(REVERSE, 15.5 + offset, INCHES)

    drivetrain.turn_to_rotation(0)
    recorded_distance = distance_7.object_distance()

    while distance_7.object_distance(INCHES) != optimal_distance:
        brain.screen.set_cursor(1, 1)
        brain.screen.clear_screen()
        brain.screen.print(distance_7.object_distance(INCHES))
        if distance_7.object_distance(INCHES) < optimal_distance:
            drivetrain.drive(REVERSE)
        else:
            drivetrain.drive(FORWARD)
    drivetrain.stop()


brain.buttonLeft.released(start_left)
brain.buttonRight.released(start_right)