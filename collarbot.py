## This is free and unencumbered software released into the public domain. 
## see LICENSE file or https://unlicense.org/ for full text of license.

from collarbot_config import *
## this loads the TOKEN variable for the discord module.""
## you need a file in the same folder as this script with the name collarbot_config.py, containing one line, "TOKEN = '<yourtoken>'"

import discord
## discord bot interface
import time
## so we can use 'sleep'
import random ## so we can use roulette

## for the transmitter function:
import pigpio ## import the pigpio library for this function

## key
## if no or incorrectly formatted key, set it manually
if len(key_) != 17:
    key_ = '00101100101001010'

pi = pigpio.pi() # set the 'pi' variable to mean wean we need to access LOCAL pi

#string transmission module
def transmitter(sequence, time_):

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
        else:
            sequence_wave.append(pigpio.pulse(1<<G1, 0, one_bit)) ## fix
            sequence_wave.append(pigpio.pulse(0, 1<<G1, one_delay))

    sequence_wave.append(pigpio.pulse(0, 0, EOS_delay))

    pi.wave_add_generic(sequence_wave)
    waveID = pi.wave_create() #save the completed wave and send wave ID to var

    pi.wave_send_repeat(waveID)
    time.sleep(time_)
    pi.wave_tx_stop() # stop waveform

    pi.wave_clear() # clear all waveforms

    pi.write(17, 0)
    print("transmission done")
## tell the program how to transmit using a given mode, power and time.
## if you're wondering why there's a _, it's because stuff like time is reserved by python
## and was causing issues. so I changed them all to be _.
def transmit(mode_,power_,time_,channel_,key_):

    print("transmitting now...")
    

    if int(power_) < 3 and mode_ is not 2:
    ## this is to fix a bug affecting power 0-2 causing errors. increases power to three if it's 0-2 to avoid it. 
        power_ = 3

    power_binary = '{0:07b}'.format(int(power_))

    ## we convert the power value between 0-100 (After converting it to an interger) to a 7 bit binary encoded number. 

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

    # Define the key! 

    key_sequence = key_
    
    sequence = '1' + channel_sequence + mode_sequnce + key_sequence + power_binary + mode_sequnce_inverse + channel_sequence_inverse + '00'

    while pi.wave_tx_busy(): # wait for prior waveform to be sent
        time.sleep(0.2)
    transmitter(sequence,time_)



print("variables and functions defined")
## debugging purposes.

client = discord.Client()
## convenience purposes. 

## defs of message conetent

help_message = ('Hi there! \n i\'m is still incomplete but right now I can: \n- Flash the collar, say !flash \n- Beep the collar, say !beep \n- Vibrate the collar, say !vibrate 003% 0.50s, where 003% is a power level between 003 and {0}, and 0.50s is a time between 0.25 and {1}. \n- administrate a shock! Say !shock:3 003% 0.50s, where 003% is a power level between 003 and {2}, and 0.50s is a time between 0.25 and {3}.\n PLEASE BE CONSERVATIVE WITH POWER LEVELS, 100 is a VERY strong shock. \n- print this help promt using !help \n- Test if the bot is online using !test \n set output to channel 1 using !channel \n set output to channel 2 using !channel2 \n have some fun by typing !shockroulette or !sr which, 1 time out of {4} will give a shock'.format(str(VibrateMaxLevel), str(VibrateMaxTime), str(ShockMaxLevel), str(ShockMaxTime), str(roulette_chance)))

shock_mode_disabled = 'shock mode is disabled. if this is not desired, please modify config file and restart the bot. otherwise, please choose a non-shock command.'

wrong_syntax_command_type = 'command' ## dummy

wrong_syntax_shock = 'please state in the form !{0} 003% 0.50s, where 003% is a power level between 003 and {1}, and 0.50s is a time between 0.25 and {2}.\n PLEASE BE CONSERVATIVE WITH POWER LEVELS, 100 is a VERY strong shock.'.format( wrong_syntax_command_type, str(ShockMaxLevel), str(ShockMaxTime))

wrong_syntax_vibrate = 'please state in the form !{0} 003% 0.50s, where 003% is a power level between 003 and {1}, and 0.50s is a time between 0.25 and {2}.'.format(wrong_syntax_command_type, str(VibrateMaxLevel), str(VibrateMaxTime))

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('{0}channel1'.format(command_char)):
        global channel_
        channel_ = 1
        msg = '{0.author.mention}, set to channel 1!'.format(message)
        await client.send_message(message.channel, msg)
        return
    if message.content.startswith('{0}channel2'.format(command_char)):
        global channel_
        channel_ = 2
        msg = '{0.author.mention}, set to channel 2!'.format(message)
        await client.send_message(message.channel, msg)
        return
    ## temp bugfix - channel var isn't coming through to the function for some reason.

    if 'channel_' not in globals():
        global channel_
        channel_ = 1
    ## note - the code is largely the same on these so i'll put full comments on one only to save space.

    ## mostly for debugging purposes.
    if message.content.startswith('{0}test'.format(command_char)):
        msg = '{0.author.mention}, online!'.format(message)
        await client.send_message(message.channel, msg)
 
    ## 'roulette' 1/x chance of a shock!
    if message.content.startswith('{0}shockroulette'.format(command_char)) or message.content.startswith('{0}sr'.format(command_char)):
        msg = '{0.author.mention}, spinning the wheel of fate...'.format(message)
        await client.send_message(message.channel, msg)
        time.sleep(roulette_delay)
        if ShockEnabled == False:
            msg = shock_mode_disabled.format(message)
            await client.send_message(message.channel, msg)
            return
        elif random.randint(1, roulette_chance) == 1:
            mode_ = 4
            if roulette_level_fixed == False:
                power_ = random.randint(1, ShockMaxLevel)
                time_ = float(random.randint(1, int(ShockMaxTime)))
            else:
                power_ = ShockDefaultLevel
                time_ = ShockDefaultTime
            transmit(mode_,power_,time_,channel_,key_)
            msg = '{0.author.mention}, ZZZAPPED at {1}% power for {2}s'.format(message, str(power_), str(time_))
            await client.send_message(message.channel, msg)                
            return
        else:
            mode_ = 3
            power_ = 100
            time_ = 0.70
            transmit(mode_,power_,time_,channel_,key_)
            msg = '{0.author.mention}, *click*'.format(message)
            await client.send_message(message.channel, msg)                
            return

    ## list commands and format, and default values when user says !help
    if message.content.startswith('{0}help'.format(command_char)):
        msg = help_message.format(message)
        await client.send_message(message.channel, msg)

    ## function to flash the collar. currently stuck on 1 second for convenience.
    if message.content.startswith('{0}flash'.format(command_char)):
        mode_ = 1
        power_ = 1
        time_ = 1
        transmit(mode_,power_,time_,channel_,key_)
        msg = '{0.author.mention}, flashing now!'.format(message)
        await client.send_message(message.channel, msg)

    ## function to beep the collar. currently stuck on 1 second for convenience.
    if message.content.startswith('{0}beep'.format(command_char)):
        mode_ = 2
        power_ = 1
        time_ = 1
        transmit(mode_,power_,time_,channel_,key_)
        msg = '{0.author.mention}, beeping now!'.format(message)
        await client.send_message(message.channel, msg)

        
    ## fully functional vibration of collar. can set time and power. 
    if message.content.startswith('{0}vibrate'.format(command_char)):
        mode_ = 3

        if message.content == '{0}vibrate'.format(command_char):
            power_ = int(VibrateDefaultLevel)
            time_ = float(VibrateDefaultTime)
            transmit(mode_,power_,time_,channel_,key_)
            msg = '{0.author.mention}, Vibrating now at {1}% for {2}s'.format(message, str(power_), str(time_))
            await client.send_message(message.channel, msg)
            return

        if len(message.content) < 18:
            
            msg = wrong_syntax_vibrate.format(message)
            await client.send_message(message.channel, msg)
            return
        if message.content[12] == '%':
            power_ = message.content[9:12]
        else:
            msg = wrong_syntax_vibrate.format(message)
            await client.send_message(message.channel, msg)
            return
        if message.content[18] == 's' and float(message.content[14:18]) > 0.24 and float(message.content[14:18]) < 9.00:
            time_ = float(message.content[14:18])
        else:
            
            msg = wrong_syntax_vibrate.format(message)
            await client.send_message(message.channel, msg)
            return
        transmit(mode_,power_,time_,channel_,key_)
        msg = '{0.author.mention}, vibrating now :3'.format(message)
        await client.send_message(message.channel, msg)   


    #shocks the collar. this one will have full annotation, code is the same as above examples. 
    if message.content.startswith('{0}shock:3'.format(command_char)):
    ## I know the :3 is annoying but it caused issues if it's not there -
    ## code parsing has to be adjusted and it broke when it was 2 chars shorter
        
        ## we already know the mode - so we set it now.
        mode_ = 4

        if ShockEnabled == False:
            msg = shock_mode_disabled.format(message)
            await client.send_message(message.channel, msg)
            return
        if message.content == '{0}shock:3'.format(command_char):
            power_ = int(ShockDefaultLevel)           
            time_ = float(ShockDefaultTime)
            channel_ = 1
            transmit(mode_,power_,time_,channel_,key_)
            msg = '{0.author.mention}, shocking now at {1}% for {2}s :3'.format(message, str(power_), str(time_))
            await client.send_message(message.channel, msg)
            return
        if len(message.content) < 18:
            msg = wrong_syntax_shock.format(message)
            await client.send_message(message.channel, msg)
            return
        ## we check the code matches the syntax (!shock:3 044% 1.00s)


        if message.content[12] == '%':
            ## if it does, grab the power. we don't validate this as we assume if the syntax for the % matches,
            ## so do the preceeding 3 digits.
            power_ = message.content[9:12]
            ## debugging purposes. 
        else:
        ## if syntax isn't followed, we assume it's wrong. pretty annoying but it's a known issue and priority to fix. 
            
            msg = wrong_syntax_shock.format(message)
            ## tell the user that their command doesn't match syntax. 
            await client.send_message(message.channel, msg)
            ## exit once this message is sent. 
            return
        if message.content[18] == 's' and float(message.content[14:18]) > 0.24 and float(message.content[14:18]) < 9.00:
        ## we check the code matches the syntax (!shock:3 044% 1.00s)
        ## times are decimal compatible so HAS to be a float value. 
            time_ = float(message.content[14:18])
            ## if it does, grab the time. we don't validate this as we assume if the syntax for the % matches,
            ## so do the preceeding 4 chars.
            
        else:
            ## if syntax isn't followed, we assume it's wrong. pretty annoying but it's a known issue and priority to fix. 
            
            msg = wrong_syntax_shock.format(message)
            ## tell the user that their command doesn't match syntax. 
            await client.send_message(message.channel, msg)
            ## exit once this message is sent. 
            return

        if int(power_) > int(ShockMaxLevel) or float(time_) > float(ShockMaxTime):
            
            msg = wrong_syntax_shock.format(message)
            ## tell the user that their command doesn't match syntax. 
            await client.send_message(message.channel, msg)
            ## exit once this message is sent. 
            return
            
        transmit(mode_,power_,time_,channel_,key_)
        ## this is defined above - now we have the time, power, mode, we send the pulses as per the function defined above. 
        ## if changing collar / hardware, this is the only part that would probably need to be changed if it had similar functions.
        msg = '{0.author.mention}, shocking now :3'.format(message)
        ## advise the user their thing was sucessful. Technically this sends once the shock is DONE which isn't ideal but it's ok for now.
        await client.send_message(message.channel, msg)
        ## exit once message sent.                   
        return
        
client.run(TOKEN)
## start the discord bot!

