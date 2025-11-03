
# Q1
what is the difference between parallel and serial transmission

serial transmission sends data one bit at a time 
parallel transmission is able to send/receive multiple bits along multiple wires in accordance with a clock signal 

these lines of data are called bus's

parallel connections cannot travel long distances but are however extremely fast
pcie, sata, CPU sockets

serial connections are slower but can be along a much longer distance

# Q2
What are skew and crosstalk and how do they affect transmission

data is read on the data lines in sync with the clock signal. The wires cannot be perfect so the data can arrive at different times creating "skew" 

crosstalk it the interference caused by wire being close to each other and getting affected by each other electromagnetic field

# Q3
when is serial more appropriate than parallel

when transferring over long distance as skew is impossible and cross talk is minimized

|              | Advantage                | Disadvantage           |
| :----------: | :----------------------- | :--------------------- |
|  **Serial**  | long distance<br>cheaper | slow                   |
| **Parallel** | faster<br>simpler        | skew <br>crosstalk<br> |


# Q4
what is the difference between synchronous and asynchronous transmission 

synchronous transmission needs to be on a common clock, it is a constant flow of data


