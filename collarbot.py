from collarbot_config import *
## this loads the TOKEN variable for the discord module.""
## you need a file in the same folder as this script with the name collarbot_config.py, containing one line, "TOKEN = '<yourtoken>'"

import discord
## discord bot interface
import time
## so we can use 'sleep'

## TIMINGS
## see control-protocol.md on the github for this project for details of the timings and pictures etc.
## the reason there's ones commented out is because I made manual adjustments and wanted to keep the old values. 
## i'll probably delete later.


## key
## if no or incorrectly formatted key, set it manually
if len(key_) != 17:
    key_ = '00101100101001010'


## tell the program how to transmit using a given mode, power and time.
## if you're wondering why there's a _, it's because stuff like time is reserved by python
## and was causing issues. so I changed them all to be _.
def transmit(mode_,power_,time_,channel_,key_):

    print("transmitting now...")
    ## this is for debugging purposes mostly. 

    power_binary = '0000101'
    #power_binary = '{0:08b}'.format(int(power_))
    ## we convert the power value between 0-100 (After converting it to an interger) to a 7 bit binary encoded number. 

    print(power_binary)
    ## this is for debugging purposes

    timer = time.time() + time_
    ## we set 'timer' as the current time + the time we want the thing to last, gettin the time we need to stop transmitting.

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
        mode_sequnce_inverse = '0111'
    elif mode_ == 3:
        ## vibrate the collar
        mode_sequnce = '0010'
        mode_sequnce_inverse = '1101'
    elif mode_ == 4:
        #shock the collar 
        mode_sequnce = '0001'
        mode_sequnce_inverse = '1110'
    else:
        #mode = 2
        ## beep the collar. it was done like this so the 'else' is a beep, not a shock for safety. 
        mode_sequnce = '0100'
        mode_sequnce_inverse = '1011' 

    # Define the key! 

    key_sequence = key_
    

    sequence = '1' + channel_sequence + mode_sequnce + key_sequence + power_binary + mode_sequnce_inverse + channel_sequence_inverse + '00'

    print('S' + sequence)


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

     
    if message.content.startswith('!shockD'):
        
        ## we already know the mode - so we set it now.
        mode_ = 4

        if ShockEnabled == False:
            msg = '{0.author.mention}, shock mode is disabled. if this is not wanted, please modify config file and restart the bot'.format(message)
            await client.send_message(message.channel, msg)
            return

        power_ = int(ShockDefaultLevel)

        if int(power_) < 3:
            ## this is to fix a bug affecting power 0-2 causing errors. increases power to three if it's 0-2 to avoid it. 
                power_ = 3
        print(power_)

        if int(power_) > int(ShockMaxLevel):
            power_ = int(ShockMaxLevel)

        time_ = float(ShockDefaultTime)

        if float(time_) > float(ShockMaxTime):
            time_ = float(ShockMaxTime)
        
        transmit(mode_,power_,time_,channel_,key_)

        msg = '{0.author.mention}, shocking now at ' + str(power_) + '% for ' + str(time_) + 's :3'.format(message)
    
        await client.send_message(message.channel, msg)
        ## exit once message sent.                   
        return

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
            msg = '{0.author.mention}, please state in the form !shock:3 003% 0.50s, where 003% is a power level between 003 and ' + str(ShockMaxLevel) +  ', and 0.50s is a time between 0.25 and ' + str(ShockMaxTime) + '.\n PLEASE BE CONSERVATIVE WITH POWER LEVELS, 100 is a VERY strong shock.'.format(message)
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
            msg = '{0.author.mention}, please state as !shock:3 003% 0.50s, where 003% is a power level between 003 and ' + str(ShockMaxLevel) + ', and 0.50s is a time between 0.25 and ' + str(ShockMaxTime) + '.\n PLEASE BE CONSERVATIVE WITH POWER LEVELS, 100 is a VERY strong shock.'.format(message)
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
            msg = '{0.author.mention}, please state as !shock:3 003% 0.50s, where 003% is a power level between 003 and ' + str(ShockMaxLevel) + ', and 0.50s is a time between 0.25 and ' + str(ShockMaxTime) + '.\n PLEASE BE CONSERVATIVE WITH POWER LEVELS, 100 is a VERY strong shock.'.format(message)
            ## tell the user that their command doesn't match syntax. 
            await client.send_message(message.channel, msg)
            ## exit once this message is sent. 
            return

        if int(power_) > int(ShockMaxLevel) or float(time_) > float(ShockMaxTime):
            msg = '{0.author.mention}, please state as !shock:3 003% 0.50s, where 003% is a power level between 003 and ' + str(ShockMaxLevel) + ', and 0.50s is a time between 0.25 and ' + str(ShockMaxTime) + '.\n PLEASE BE CONSERVATIVE WITH POWER LEVELS, 100 is a VERY strong shock.'.format(message)
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

