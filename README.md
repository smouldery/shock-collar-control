# shock-collar-control
Hardware instructions, RF protocol decoding, and control software to enable remote control of commercially available shock collars

1: preliminaries:
- this project is to control a shock collar - a device traditionally used in "training" dogs and pets. while I cannot stop you from using it for this purpose, I condemn in the strongest possible terms the use of shock collars, and by extension, the use of this software to control shock collars, that are used on any entity that can feel pain that is unable to (i.e. non-human animals, human children) or does not (i.e. unwilling adults) consent to it's use on them. 

- this project uses commecial products that are intended for use on non-human animals, and involve electricity. I offer no guarantee that use outside (or within) the manifacturers intended use are safe and I reccomend you seek medical advice on the issue before use.

- all code in this repository, and all comments / contributions, should be safe for work. any NSFW uses of the shock collar control system are fine by me but should be discussed in a manner that minimizes their nsfw-ness please!

- this project makes use of a number of less-open / completely closed / commerical software and hardware. if anyone has affordable alternatives, i'd love to hear them, I used what I did because I wanted a working thing.

Hope y'all enjoy it!

  - Smouldery

2: Introduction:
2.1: general intro:

this project aims to take manually controlled shock collars, and introduce a remote interface so they can be operated either autonomously, or manually over larger distances than is possible with provided hardware. code is in python3. 

  2.2: initial project scope:
    2.2.1: Initially, the testing is being done with an 'Esky® –Electronics Sky' shock collar, model 998DR-1. this model is tricky to find but similar versions can be found, and I suspect operate on the same protocols as the one I have. 
    2.2.2: This collar operates on the 433mhz frequency, using a one-way radio transmission in binary strings of 42 bits in length (the first bit is timed differently and longer. this sequence incorporates 3 primary sections: an opening sequence of 7 bits which specifies collar channel and mode, what appears to be a remote 'key' of 13 bits that is static and identifies the remote, the power level of the action (shock or vibrate) as a whole number % between 0-100, encoded as a 7-bit binary number, and finally a 7 bit closing sequence, which is the inverse of the 7 bit starting sequence. This is transmitted for the duration it is desired the collar operate for, and the duration for which the collar receives the signal is the sole method shock time is regulated (collar cuts out at 10 seconds for safety reasons). further details of this protocol, and the steps taken to decode it, can be found in control-protocol.md
  2.3 Hardware: at present, the controller runs on a Raspberry pi 2 (official hardware) and model 2008-8 433mhz transmitter of unknown origin (i.e. buy a cheap one). this just runs off the raspberry pi power provided via the pins. 
    
3: the code so far...
  3.1: current status: at present, the code is operating in what seems to be a stable manner. I have a discord bot running on a test server that responds to commands like !shock 050% 4.00s reliably. this code runs in python3 as this was what the discord library in python used. 
  3.2: limitations / current bugs: 
    3.2.1: major bug #1: if power level was set to 3, power level seems to jump to 100 despite the right bits being transmitted. i'm unsure why this occurs but as an interim measure, i've set power levels of 1 or 2 to increase to 3 to ensure the power level isn't too high (this is bad and hurts a lot). 
    3.2.2: Major Limitation #1: interpreting of power level and time is very strict. if you don't use format 000% 0.00s, it won't work. i'm working on this but it was set like this because that's how (with my limited programming skills) I got it to work. 

4: future plans:
  4.1: Sourcing and decoding / verifying compatability of a currently sold collar: I'll be working on buying and testing a collar that's avaliable in most places and can be readily identified, so users can be sure to have a collar that works out of the box. 
  4.2: improving power level / duration interpretation and general command use to be more intuitive: first priority is remove restrictive syntax for the power level and time, then work on improving the general usability of the bot.
  4.3: documentation documentation documentation! this will be my FIRST priority and i'll focus on setup first, then outline my process for decoding the collar. i'll also attach some documetation / photo of the collar itself so if anyone wants to jump in and try and secure one themselves they can try and get a reasonably compatible one. 
  
 Thanks for reading, comments or suggestions are welcome, keep them sfw please folks!
   
