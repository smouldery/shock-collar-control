## NOT RECCOMENDED - THIS MODULE IS DEPRECIATED AND NO LONGER MAINTAINED
## NOT GUARANTEED TO WORK

## This is free and unencumbered software released into the public domain. 
## see LICENSE file or https://unlicense.org/ for full text of license.

## takes PARAMATERS and transmits 
## python3 transmitter_vars.py mode power time channel key (opt)

import gpiozero
## used to manually control the GPIO pins.
import time
## so we can use 'sleep'
import sys 
## so we can grab args from command line

## grab variables
power_ = int(sys.argv[1])
time_ = float(sys.argv[2])
mode_ = int(sys.argv[3])
channel_ = int(sys.argv[4])

try:
    len(str(sys.argv[5]))
except IndexError:
    key_ = '00101100101001010'
else:
    if len(str(sys.argv[5])) != 17:
        key_ = '00101100101001010'
    else:
        key_ = str(sys.argv[5])
## TIMINGS
## see control-protocol.md on the github for this project for details of the timings and pictures etc.
## the reason there's ones commented out is because I made manual adjustments and wanted to keep the old values. 
## i'll probably delete later.

#start = 0.001545
start = 0.001300
#start_space = 0.00236
start_space = 0.00200
start_gap = start_space - start
#space = 0.00105
space = 0.00080
#zero = 0.00023
zero = 0.00015
zero_space = space - zero
#one = 0.000755
one = 0.000730
one_space = space - one

## we use this to control the transmitter manually
transmitter = gpiozero.LED(17)

## prep transmit functions

## tell the program how to send a 'one' bit.
def O():
    #space = 0.00105
    space = 0.00080
    #one = 0.000755
    one = 0.000730
    one_space = space - one
    transmitter.on()
    time.sleep(one)
    transmitter.off()
    time.sleep(one_space);

## tell the program how to send a 'zero' bit. 
def Z():
    #space = 0.00105
    space = 0.00080
    #zero = 0.00023
    zero = 0.00015
    zero_space = space - zero
    transmitter.on()
    time.sleep(zero)
    transmitter.off()
    time.sleep(zero_space);

## tell the program how to transmit using a given mode, power and time.
## if you're wondering why there's a _, it's because stuff like time is reserved by python
## and was causing issues. so I changed them all to be _.
def transmit(mode_,power_,time_,channel_):

    power_binary = '{0:08b}'.format(int(power_))
    ## we convert the power value between 0-100 (After converting it to an interger) to a 7 bit binary encoded number. 

    timer = time.time() + time_
    ## we set 'timer' as the current time + the time we want the thing to last, gettin the time we need to stop transmitting.

    while True:
        ## starting bit

        transmitter.on()
        time.sleep(start)
        transmitter.off()
        time.sleep(start_gap)
        ## this sends the 'starting bit' - it's longer than a normal One bit.
        ## see control-protocol.md on the github for details/

        ## start primary sequence
        O()
        #there's two ones in the start sequence, this sends the normal one.

        #channel
        ## this sends the channel. this is a binary setting despite having 3 bits. 000 = channel 1
        ## 111 = channel 2
        ## channel will default to 1 if this is not present in settings for some
        if channel_ == 2:
            O()
            O()
            O()
        else: 
            Z()
            Z()
            Z()

        ##mode
        ## we send the mode.

        if mode_ == 1:
        ## flash the ight on the collar. 
            O()
            Z()
            Z()
            Z()
        elif mode_ == 3:
        ## vibrate the collar
            Z()
            Z()
            O()
            Z()
        elif mode_ == 4:
        ## vibrate the collar.
            Z()
            Z()
            Z()
            O()
        else:
            #mode = 2
            ## beep the collar. it was done like this so the 'else' is a beep, not a shock for safety. 
            Z()
            O()
            Z()
            Z()
        
        ## key?
        ## seems to be an ID Sequence for the remote.
        ## in any case it's static. 
        ## 00101100101001010 is the default
        Z()
        Z()
        O()
        Z()
        
        O()
        O()
        Z()
        Z()
        
        O()
        Z()
        O()
        Z()

        Z()
        O()
        Z()
        O()
        Z()

        
    ## power 
    ## sends the power. we defined the 7 bit binary sequence earlier, this sends it.
    ## again we use zero as the 'else' because that's the lower power setting.
        for x in range (0, 7):
            if int(power_binary[x]) == 1:
                O()
            else:
                Z()
    ## mode inverse
    ## this sends the mode - the closing 7 bits are the inverse of the first 7
        if mode_ == 1:
            O()
            O()
            O()
            Z()
        elif mode_ == 3:
            O()
            Z()
            O()
            O()
        elif mode_ == 4:
            Z()
            O()
            O()
            O()
        else:
            #mode = 2 
            O()
            O()
            Z()
            O()
        
        ##channel_inverse
        ## as above. inverse of above. 
        if channel_ == 2:
            Z()
            Z()
            Z()
        else:
            O()
            O()
            O()

        #signoff
        ## there is NOT an extented 'zero' to close it. that's just for the first one 
        ## and might not even be intentional.
        Z()
        Z()

        ## the way the collar does timing, we just need to send the same sequence for as long as we want the collar to work. 
        ## the sleep here is to make sure we aren't bunching them up too much. 
        time.sleep(0.003)

        if time.time() > timer:
            break;

if power_ < 3:
    power_ = 3
transmit(mode_,power_,time_,channel_)





