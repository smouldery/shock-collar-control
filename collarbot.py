from collarbot_config import *
## this loads the TOKEN variable for the discord module.""
## you need a file in the same folder as this script with the name collarbot_config.py, containing one line, "TOKEN = '<yourtoken>'"
import gpiozero
## used to manually control the GPIO pins.
import discord
## discord bot interface
import time
## so we can use 'sleep'

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

## key
## if no or incorrectly formatted key, set it manually
if len(key_) != 17:
    key_ = '00101100101001010'

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
def transmit(mode_,power_,time_,channel_,key_):

    print("transmitting now...")
    ## this is for debugging purposes mostly. 

    power_binary = '{0:08b}'.format(int(power_))
    ## we convert the power value between 0-100 (After converting it to an interger) to a 7 bit binary encoded number. 

    print(power_binary)
    ## this is for debugging purposes

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
        ## BELOW FEATURE IN BETA!!! 
        # print (key_)
        # for x in range (0, 17):
        #     if int(key_[x]) == 1:
        #         O()
        #     else:
        #         Z()
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
    print("transmit complete")
    ## debugging purposes.



print("variables and functions defined")
## debugging purposes.

client = discord.Client()
## convenience purposes. 

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    ## note - the code is largely the same on these so i'll put full comments on one only to save space.


    ## mostly for debugging purposes.
    if message.content.startswith('!test'):
        msg = '{0.author.mention}, online!'.format(message)
        await client.send_message(message.channel, msg)
 
    ## list commands and format, and default values when user says !help
    if message.content.startswith('!help'):
        msg = '{0.author.mention}, Hi there! \n i\'m is still incomplete but right now I can: \n- Flash the collar, say !flash \n- Beep the collar, say !beep \n- Vibrate the collar, say !vibrate 003% 0.50s, where 003% is a power level between 003 and ' + str(VibrateMaxLevel) +  ', and 0.50s is a time between 0.25 and ' + str(VibrateMaxTime) + '. \n- administrate a shock! Say !shock:3 003% 0.50s, where 003% is a power level between 003 and ' + str(ShockMaxLevel) +  ', and 0.50s is a time between 0.25 and ' + str(ShockMaxTime) + '.\n PLEASE BE CONSERVATIVE WITH POWER LEVELS, 100 is a VERY strong shock. \n- print this help promt using !help \n- Test if the bot is online using !test'.format(message)
        await client.send_message(message.channel, msg)

    ## function to flash the collar. currently stuck on 1 second for convenience.
    if message.content.startswith('!flash'):
        mode_ = 1
        power_ = 1
        time_ = 1
        transmit(mode_,power_,time_,channel_,key_)
        msg = '{0.author.mention}, flashing now!'.format(message)
        await client.send_message(message.channel, msg)

    ## function to beep the collar. currently stuck on 1 second for convenience.
    if message.content.startswith('!beep'):
        mode_ = 2
        power_ = 1
        time_ = 1
        transmit(mode_,power_,time_,channel_,key_)
        msg = '{0.author.mention}, beeping now!'.format(message)
        await client.send_message(message.channel, msg)
        
    ## fully functional vibration of collar. can set time and power. 
    if message.content.startswith('!vibrate'):
        mode_ = 3

        if len(message.content) < 18:
            msg = '{0.author.mention}, please state in the form !vibrate 020% 0.50s'.format(message)
            await client.send_message(message.channel, msg)
            return
        if message.content[12] == '%':
            power_ = message.content[9:12]
            if int(power_) < 3:
                power = 3
            print(power_)
        else:
            msg = '{0.author.mention}, please include power between 3-100 with 3 digits i.e 020%, and the form !vibrate 020% 0.50s'.format(message)
            await client.send_message(message.channel, msg)
            return
        if message.content[18] == 's' and float(message.content[14:18]) > 0.24 and float(message.content[14:18]) < 9.00:
            time_ = float(message.content[14:18])
            
            print(time_)
        else:
            msg = '{0.author.mention}, please time between 0.25-9 seconds as 0.00s, and the form !vibrate 020% 0.50s'.format(message)
            await client.send_message(message.channel, msg)
            return
        transmit(mode_,power_,time_,channel_,key_)
        msg = '{0.author.mention}, vibrating now :3'.format(message)
        await client.send_message(message.channel, msg)   

    #shocks the collar. this one will have full annotation, code is the same as above examples. 
    if message.content.startswith('!shock:3'):
    ## I know the :3 is annoying but it caused issues if it's not there -
    ## code parsing has to be adjusted and it broke when it was 2 chars shorter
        
        ## we already know the mode - so we set it now.
        mode_ = 4

        if ShockEnabled == False:
            msg = '{0.author.mention}, shock mode is disabled. please modify config file and restart the bot'.format(message)
            await client.send_message(message.channel, msg)
            return
        if len(message.content) < 18:
            msg = '{0.author.mention}, please state in the form !shock:3 020% 0.50s'.format(message)
            await client.send_message(message.channel, msg)
            return
        ## we check the code matches the syntax (!shock:3 044% 1.00s)


        if message.content[12] == '%':
            ## if it does, grab the power. we don't validate this as we assume if the syntax for the % matches,
            ## so do the preceeding 3 digits.
            power_ = message.content[9:12]
            ## doing the above.
            if int(power_) < 3:
            ## this is to fix a bug affecting power 0-2 causing errors. increases power to three if it's 0-2 to avoid it. 
                power = 3
            print(power_)
            ## debugging purposes. 
        else:
        ## if syntax isn't followed, we assume it's wrong. pretty annoying but it's a known issue and priority to fix. 
            msg = '{0.author.mention}, please include power between 3-100 with 3 digits i.e 020%, and the form !shock:3 020% 0.50s'.format(message)
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
            
            print(time_)
            ## debugging purposes. 
        else:
            ## if syntax isn't followed, we assume it's wrong. pretty annoying but it's a known issue and priority to fix. 
            msg = '{0.author.mention}, please time between 0.25-9 seconds as 0.00s and the form !shock:3 020% 0.00s'.format(message)
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

