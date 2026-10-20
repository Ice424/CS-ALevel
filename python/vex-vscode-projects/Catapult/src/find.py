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

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)



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

#endregion VEXcode Generated Robot Configuration

vexcode_vision_11_objects = []
myVariable = 0
start_side = LEFT
def start_left():
    global start_side 
    start_side = RIGHT
    when_started1()

def start_right():
    global start_side 
    start_side = LEFT
    when_started1()

def when_started1():
    global myVariable, start_side, vexcode_vision_11_objects
    brain.play_sound(SoundType.SIREN)

    stage = 0
    calibartion_times = 0
    while True:
        
        if stage == 0:
            
            vexcode_vision_11_objects = vision_11.take_snapshot(vision_11__SIG_1)
            if vexcode_vision_11_objects and calibartion_times <= 60:
                calibartion_times +=1
                print(calibartion_times)
                if vexcode_vision_11_objects[0].centerX > 316 / 2:
                    drivetrain.turn(LEFT)
                    print("left")
                else:
                    drivetrain.turn(RIGHT)
                    print("right")
            elif calibartion_times > 60:
                stage = 1
                drivetrain.stop()
            
        

        

brain.buttonLeft.released(start_left)
brain.buttonRight.released(start_right)