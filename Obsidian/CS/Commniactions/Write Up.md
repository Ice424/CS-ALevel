
## The Initial Problem

When looking at the example code I quickly realized that throughput of information would be an issue. Waiting 1 second for 0 and 2 for 1 would mean that transferring the text hello world would take 131 seconds or 2 mins and 11 seconds.

The two solutions would be to either shorten the amount of time each pulse takes or change to a different system.
$\frac{7}{8}$

shortening the time taken for pulses sounds like a good idea however ideally you would want the difference in time between 1 and 0 to be as small as possible however with vex hardware it can be difficult to detect small differences in timing. this gives us three values to fine tune: length of pulse for 0, time between pulses, length of pulse for 1

Due to the amount of fine tuning getting this to run fast would require i decided to switch to a different protocol.

## The new protocol

In the original program there is a synchronization step at the start of each file. for the original setup it is not actually needed and the receiver will respond anytime it receives a two or 1 second pulse of light. I decided to use this synchronization to start a clock on both brains with a preset rate 

Every clock cycle the light would change to the next bit on for 1 off for 0. The receiver would then read the values in and display the output. 

This gives us 1 value to fine tune instead of 3, the clock speed.

## Iteration 1 

```python title:Sender
#Previous synchronisation code

text_to_send = "Hello World"

for char in text_to_send:
	#converts text_to_send into a list a list of binary values
	#hello = [0,1,0,0,1,0,0,0,0,1,1,0,0,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,1]
	list_to_send.append(list("{ascii:08b}".format(ascii=ord(char))))
	
for byte in list_to_send:
	for bit in byte:
	bit = int(bit)
	if bit:
		color_6.set_light(100,PERCENT)
	else:
		color_6.set_light(0,PERCENT)
	wait(INTERVAL,MSEC)
```

```python title:Receiver
#Previous synchronisation code

while True
	signal_level = optical_3.brightness()
	
	
	if signal_level > midpoint:
		touchled_4.set_brightness(100)
		received.append("1")
		
	else:
		touchled_4.set_brightness(0)
		received.append("0")
		
	wait(INTERVAL, MESC)
	
	print(received)
	
```


in the code above you can see the general structure for the sender and the receiver this initial iteration had several notable issues

#### Problems

the value midpoint was arbitrarily set to 50% so the program did not adapt well to different lighting conditions alongside the fact that the receiver would never display the text or stop running

the most pressing issue however is the value from the receiver being read at the same time the sender is changing value causing a lot of misinterpreted values

## Iteration 2

To  fix the two  most pressing issues the start of `list_to_send` had `[1,0]` appended to the beginning of the list to calibrate the midpoint & the entire receiver would be offset by half of the clock Speed meaning that the values would be read during each pulse rather than as they were changing

```python title:ReceiverCalibration

wait(INTERVAL/2,MSEC)

on = optical_3.brightness()
wait(INTERVAL)
off = optical_3.brightness()
wait(INTERVAL)

midpoint = (on + off) // 2
```

The receiver also was change to handle received  binary byte by byte and would check for the ASCII end transmission signal or for 8 0's implying an incorrect transmission or that the sender has crashed 

```python title:Receiver
## while final received bytes are not the ASCII end transmission signal or for 8 0's
while not(received[-8:] == ["0","0","0","0","0","0","0","0"] or recived[-8:] == ["0","0","0","0","0","1","0","0"]):

    #record the brightness
    signal_level = optical_3.brightness()
    
    #if light is on append 1 to current byte if not append 0
    if signal_level > midpoint:
        current_byte.append("1")

    else:
        touchled_4.set_brightness(0)
        current_byte.append("0")
        
    wait(INTERVAL)
    
    #if received full byte
    if len(current_byte) == 8:
	    #decode the text from binary and store it
        decoded_text = decoded_text + chr(int("".join(current_byte[-8:]),2))
        #append to the total recived value
        recived.extend(current_byte)
        #reset the current byte
        current_byte = []

		#display decoded text to the screen
        brain.screen.clear_row(1)
        brain.screen.set_cursor(1, 1)
        brain.screen.print(decoded_text)
```

The Decoded Text was also displayed on screen 

#### Problems
Due to the nature of python displaying to the screen and general computation would cause the two programs to become de-synchronised while sending long transmissions to fix this a short re-synchronisation pulse was sent at the end of each byte that the transmitter would wait for 

## Iteration 3

```python title:Receiver
 if len(current_byte) == 8:
 
		#previously discussed code
		
		#send resynchronisation pulse we dont wait for a relply as it is not needed
		optical_3.set_light(LedStateType.ON)
        wait(INTERVAL,MSEC)
        optical_3.set_light(LedStateType.OFF)
        wait(INTERVAL,MSEC)
        #offset to measure between pulse change
        wait(INTERVAL/2,MSEC)
```

```python title:Sender
#wait for resync pulse
while not colour_feedback > 15:
    colour_feedback = color_6.brightness()

wait(INTERVAL,MSEC)
    
```

though testing a full handshake was found unnecessary and a single pules from the receiver every byte is enough to keep the two in sync


## Iteration 4
A keyboard input was added to the sender to drive interaction at open evening unfortunately the Receiver program was in a broken state as  line 11 was missing in the code above causing similar issues as in [[#Iteration 1]] after 1 byte

```python title:Receiver(Repeated)
        #offset to mesure inbetween pulse change
        wait(INTERVAL/2,MSEC)
```

After Open Evening changes were made to the initial synchronisation changing the colour to purple to avoid the programs starting from light leak from nearby monitors (that was mainly blue) and to be faster and more reliable [[#full files]]

## Overall

due to the changing midpoint the program was able to send the text "hello there world how are you" in low lighting conditions over 30cm

this program could be further improved with parity bits or other forms of error detection as that is currently absent and could be used in conditions with a lot of interference from other light sources 

## Full files
```python title:SenderFull
import math
from vex import *

# Begin project code
text_to_send = ""
CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_!"
current_char = 0
ready_to_send = False

#Keyboard functions
def left():
    global current_char
    current_char = (current_char - 1) % len(CHARS)

def right():
    global current_char
    current_char = (current_char + 1) % len(CHARS)

def confirm():
    global current_char
    global text_to_send
    global CHARS
    global ready_to_send
	
	#escape special characters (change _ to space and ! sends inputted text)
    if CHARS[current_char] == "!":
        ready_to_send = True
    if CHARS[current_char] == "_":
        text_to_send += " "
    else:
        text_to_send +=  CHARS[current_char]


brain.buttonLeft.released(left)
brain.buttonRight.released(right)
brain.buttonCheck.released(confirm)
#loop to hold sending untill text inputted
while not ready_to_send:
    brain.screen.clear_row(1)
    brain.screen.set_cursor(1, 1)

    brain.screen.print(text_to_send)
    brain.screen.print(CHARS[current_char])
    
    wait(100, MSEC)

#set interval
INTERVAL = 200
colour_feedback = 0

list_to_send = []
touchled_3.set_brightness(100)
touchled_3.set_color(Color.PURPLE)
#wait for receiver pulse
while not colour_feedback > 15:
    colour_feedback = color_6.brightness()
touchled_3.set_brightness(0)
#reciver pulses for 500 MSEC wait utill it turns off
wait(500,MSEC)

#change text to binary list
for char in text_to_send:
    list_to_send.append(list("{ascii:08b}".format(ascii=ord(char))))

list_to_send.append([0,0,0,0,0,1,0,0])


#send calibration bits
color_6.set_light(100,PERCENT)
wait(INTERVAL,MSEC)
color_6.set_light(0,PERCENT)
wait(INTERVAL,MSEC)

#start of transmission loop
for byte in list_to_send:
	#print current byte to screen
    brain.screen.set_cursor(1, 1)
    brain.screen.clear_row(1)
    brain.screen.print(byte)

    for bit in byte:
       
        bit = int(bit)
        if bit:
            color_6.set_light(100,PERCENT)
        else:
            color_6.set_light(0,PERCENT)
        wait(INTERVAL,MSEC)   
        color_6.set_light(0,PERCENT)
    
    #wait for resync pulse
    colour_feedback = color_6.brightness()
    while not colour_feedback > 15:
        colour_feedback = color_6.brightness()
    wait(INTERVAL,MSEC)
```

```python title:ReceiverFull
# Library imports
from vex import *


colour_received = 0
signal_level = 0

INTERVAL = 200
current_byte = []

received = []
decoded_text = ""

touchled_4.set_brightness(0)
optical_3.set_light_power(100,PERCENT)
optical_3.set_light(LedStateType.OFF)


colour_received = optical_3.color()

#wait until we see purple
while str(colour_received) != "Color 00FF00FF":
    colour_received = optical_3.color()

#send 500 MESC flash
optical_3.set_light(LedStateType.ON)
wait(500,MSEC)
optical_3.set_light(LedStateType.OFF)

#calibrate midpoint & offset 
wait(INTERVAL/2,MSEC)
on = optical_3.brightness()
wait(INTERVAL)
off = optical_3.brightness()
wait(INTERVAL)
midpoint = (on + off) // 2
#print midpoint on screen (second line)
brain.screen.set_cursor(2, 1)
brain.screen.print(midpoint)

wait(INTERVAL)

#main loop start
## while final received bytes are not the ASCII end transmission signal or for 8 0's
while not(received[-8:] == ["0","0","0","0","0","0","0","0"] or received[-8:] == ["0","0","0","0","0","1","0","0"]):
    
    #record the brightness
    signal_level = optical_3.brightness()
    
    #if light is on append 1 to current byte if not append 0
    if signal_level > midpoint:
        touchled_4.set_brightness(100)
        current_byte.append("1")
    else:
        touchled_4.set_brightness(0)
        current_byte.append("0")
    
    wait(INTERVAL)
    
    touchled_4.set_brightness(0)
    
    #if received full byte
    if len(current_byte) == 8:
        #decode the text from binary and store it
        decoded_text = decoded_text + chr(int("".join(current_byte[-8:]),2))
        #append to the total recived value
        received.extend(current_byte)
        #reset the current byte
        current_byte = []
        
        #display decoded text to the screen
        brain.screen.clear_row(1)
        brain.screen.set_cursor(1, 1)
        brain.screen.print(decoded_text)
        
        #send resynchronisation pulse
        optical_3.set_light(LedStateType.ON)
        wait(INTERVAL,MSEC)
        optical_3.set_light(LedStateType.OFF)
        wait(INTERVAL,MSEC)
        #offset to measure between pulse change
        wait(INTERVAL/2,MSEC)

          

#print final text to screen with end character removed
decoded_text = decoded_text[:-2]
brain.screen.clear_row(1)
brain.screen.set_cursor(1, 1)
brain.screen.print(decoded_text)
        
brain.play_sound(SoundType.TADA)
```