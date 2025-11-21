1. 
	- A start bit is to let the reviving end know that the next set of data is meaningful
	- A stop bit indicates the end of meaningful data and the end of the transmission
2. A protocol is the predefined what two computer systems will exchange data
3. latency is the time taken for a signal to be sent and received 
4. 
	1. serial data transmission can be used over long distances. as there is only one stream of data the use of radio, WiFi or other long form wireless communication methods are a lot easier to implement and more reliable
	2. serial data transmission over cable is cheaper. only one cable needs to be layed/used and is therefore cheaper to implement.
5. 
	- Bit rate is the amount of bits that can be transferred in a given time span usually per second
	-  latency is the time taken for a signal to be sent and received 
6. 
	1. parallel communication sends around a byte at a time over multiple lanes with an extra cable for a synchronisation signal. serial communication sends information 1 bit at a time using start and stop bits to mark the start and end of transmissions
	2. USB is simple to implement and a widely accepted standard
	3. baud rate sets the maximum frequency at witch the frequency can change 
	4. in more advanced protocols where each frequency can represent a larger number of bits 
7. 
	1.  parallel communication sends around a byte at a time over multiple lanes with an extra cable for a synchronisation signal.
	2.  
		1. the effects of data skew (where bits arrive at different times) are amplified over longer distances making the transmission more unreliable
		2. using serial transmission
8. 
	1. if there are an even amount of bits in the 7 bit character a 1 is added to the beginning or end of the byte if its odd it'll add a 0. when the signal is received the program calculates weather the parity bit is correct if not we can assume something went wrong in transmission and request the byte again 
	2. there is a direct relationship between bit rate and bandwidth. greater the bandwidth the higher the bit rate can be transmitted