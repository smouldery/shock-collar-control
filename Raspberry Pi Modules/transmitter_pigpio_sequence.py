## This is free and unencumbered software released into the public domain. 
## see LICENSE file or https://unlicense.org/ for full text of license.

## this file takes TWO arguments, a 41 bit string and a float time value


import pigpio # for pulse control
import time # for sleep()
import sys # to import variables from command line call

sequence = str(sys.argv[1])
time_ = float(sys.argv[2])

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

transmit(sequence, time_)
