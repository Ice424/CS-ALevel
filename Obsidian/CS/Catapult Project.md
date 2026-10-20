# How to use:
- Align robot with the VEX field grid in either of the red boxes below against the back wall and start the program
![[TopView_crop.png]]
- Once the gyro is calibrated press either the left or right arrow to indicate which side of the field it is on
- You can correct the inconsistencies in the robots movements while it is running (especially while it is aligning with the light sensor for a second time) by pushing it

## How it works
- The robot first needs to figure out where the light sensor is located It does a 90 degree sweep of the side of the field that it is on
- While the robot is rotating it looks for the light green bar and notes the maximum width the bar
- As objects look smaller when further away the robot takes the perceived width of the bar it found and compares it to a table of prerecorded values to find at which position on the filed the light sensor is
- Once the robot drive to the location it offsets the robot slightly due to the offset light sensor (it had to be moved to make space for the camera)
- The robot drives into the bar and reverse slightly to increase the chance the light sensor sees the correct signal
- To get the signal (light on for 1 second is 0  or green, light on for 2 seconds is 1 or red) we wait at the light emitter for just over 1 second and check if the light is still on
- The signal we get determines how far the robot reverses away from the light emitter
- The robot marks how far it is away from the target and the difference between its current distance and the "ideal distance" using the distance sensor on the front of the robot
- It drives to the target fires and repeats the process by driving to the position it recorded before going towards the target
