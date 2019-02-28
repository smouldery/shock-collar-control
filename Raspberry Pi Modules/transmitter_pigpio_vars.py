## takes PARAMATERS and transmits 
## python3 transmitter_vars.py mode power time channel key (opt)

import pigpio # for pulse control
import time # for sleep()
import sys # to import variables from command line call

## grab the vars from the arguments passed to this program
mode_ = int(sys.argv[1])
power_ = int(sys.argv[2])
time_ = float(sys.argv[3])
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

## define how to actually send the bits
def transmitter(sequence, time_):
    pi = pigpio.pi() # set the 'pi' variable to mean wean we need to access LOCAL pi

    #set output pins
    G1 = 17

    pi.set_mode(G1, pigpio.OUTPUT) # GPIO 17 as output

    pi.wave_clear() # clear existing waveforms

    #create lists of parts of the wave we need 
    start_=[]
    one_=[]
    zero_=[]
    end_=[]
    sequence_wave=[]

    # define times
    start_bit = 1540
    start_delay = 800
    space = 1040
    zero_bit = 220
    zero_delay = space - zero_bit
    one_bit = 740
    one_delay = space - one_bit 
    EOS_delay = 7600

    sequence_wave.append(pigpio.pulse(1<<G1, 0, start_bit))
    sequence_wave.append(pigpio.pulse(0, 1<<G1, start_delay))

    for x in range(0, 40): #adds the sequence bits to the waveform, in order.
        if int(sequence[x]) == 0:
            sequence_wave.append(pigpio.pulse(1<<G1, 0, zero_bit)) ## fix
            sequence_wave.append(pigpio.pulse(0, 1<<G1, zero_delay))
            print("zero")
        else:
            sequence_wave.append(pigpio.pulse(1<<G1, 0, one_bit)) ## fix
            sequence_wave.append(pigpio.pulse(0, 1<<G1, one_delay))
            print("one")

    sequence_wave.append(pigpio.pulse(0, 0, EOS_delay))

    pi.wave_add_generic(sequence_wave)
    waveID = pi.wave_create() #save the completed wave and send wave ID to var
    print("wave ID:")
    print(str(waveID))

    pi.wave_send_repeat(waveID)
    time.sleep(time_)
    pi.wave_tx_stop() # stop waveform

    pi.wave_clear() # clear all waveforms

    pi.write(17, 0)

## tell the program how to transmit using a given mode, power and time.
## if you're wondering why there's a _, it's because stuff like time is reserved by python
## and was causing issues. so I changed them all to be _.
def transmit(mode_,power_,time_,channel_,key_):

    key_sequence = key_

    # if int(power_) < 3 and mode_ is not 2:
    # ## this is to fix a bug affecting power 0-2 causing errors. increases power to three if it's 0-2 to avoid it. 
    #     power_ = 3

    power_binary = '0000101'
    #power_binary = '{0:08b}'.format(int(power_))
    ## we convert the power value between 0-100 (After converting it to an interger) to a 7 bit binary encoded number. 

    print(power_binary)
    ## this is for debugging purposes

    print (str(channel_))
   
        ## def channel string:
    if channel_ == 2:
        channel_sequence = '111'
        channel_sequence_inverse = '000'
    else: 
        channel_sequence = '000'
        channel_sequence_inverse = '111'

    if mode_ == 1:
        ## flash the ight on the collar. 
        mode_sequnce = '1000'
        mode_sequnce_inverse = '1110'
    elif mode_ == 3:
        ## vibrate the collar
        mode_sequnce = '0010'
        mode_sequnce_inverse = '1011'
    elif mode_ == 4:
        #shock the collar 
        mode_sequnce = '0001'
        mode_sequnce_inverse = '0111'
    elif mode_ == 2:
        mode_sequnce = '0100'
        mode_sequnce_inverse = '1101' 
    else:
        #mode = 2
        ## beep the collar. it was done like this so the 'else' is a beep, not a shock for safety. 
        mode_sequnce = '0100'
        mode_sequnce_inverse = '1101' 
        
    sequence = '1' + channel_sequence + mode_sequnce + key_sequence + power_binary + mode_sequnce_inverse + channel_sequence_inverse + '00'

 
    transmitter(sequence, time_)

transmit(mode_,power_,time_,channel_,key_)