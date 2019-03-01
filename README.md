
# shock-collar-control
Hardware instructions, RF protocol decoding, and control software to enable remote control of commercially available shock collars

1: preliminaries:
- this project is to control a shock collar - a device traditionally used in "training" dogs and pets. while I cannot stop you from using it for this purpose, I condemn in the strongest possible terms the use of shock collars, and by extension, the use of this software to control shock collars, that are used on any entity that can feel pain that is unable to (i.e. non-human animals, human children) or does not (i.e. unwilling adults) consent to it's use on them. 

- this project uses commecial products that are intended for use on non-human animals, and involve electricity. I offer no guarantee that use outside (or within) the manifacturers intended use are safe and I reccomend you seek medical advice on the issue before use.

- all code in this repository, and all comments / contributions, should be safe for work. any NSFW uses of the shock collar control system are fine by me but should be discussed in a manner that minimizes their nsfw-ness please!

- this project makes use of a number of less-open / completely closed / commerical software and hardware. if anyone has affordable alternatives, i'd love to hear them, I used what I did because I wanted a working thing.

Hope y'all enjoy it!

~smouldery

2: Introduction:
  - 2.1: general intro:

this project aims to take manually controlled shock collars, and introduce a remote interface so they can be operated either autonomously, or manually over larger distances than is possible with provided hardware. code is in python3. 

  - 2.2: initial project scope:
    - 2.2.1: Initially, the testing is being done with an 'Esky® –Electronics Sky' shock collar, model 998DR-1. this model is tricky to find but similar versions can be found, and I suspect operate on the same protocols as the one I have. 
    - 2.2.2: This collar operates on the 433mhz frequency. further details of this protocol can be found in the [protocol](https://github.com/smouldery/shock-collar-control/wiki/protocol) section of the wiki, and the steps taken to decode it can be found in the [decoding the protocol](https://github.com/smouldery/shock-collar-control/wiki/decoding_the_protocol) section of the wiki
  - 2.3 Hardware: at present, the controller runs on a Raspberry pi 2 (official hardware) and model 2008-8 433mhz transmitter of unknown origin (i.e. buy a cheap one). this just runs off the raspberry pi power provided via the pins. it should run on most raspberry pi's (tested on the zero) i'll be documenting this in detail on the wiki on the [hardware page](https://github.com/smouldery/shock-collar-control/wiki/hardware) so take a look there for further details.
    
3: the code so far...
  - 3.1: current status: at present, the code is operating in what seems to be a stable manner. I have a discord bot running on a test server that responds to commands like !shock 050% 4.00s reliably. 
  - 3.2 Setup of current project: see wiki page [here](https://github.com/smouldery/shock-collar-control/wiki/setup)
  
4: future plans:
  - 4.1: Sourcing and decoding / verifying compatability of a currently sold collar: I'll be working on buying and testing a collar that's avaliable in most places and can be readily identified, so users can be sure to have a collar that works out of the box. 
  - 4.3: documentation documentation documentation! this will be my FIRST priority and i'll focus on setup first, then outline my process for decoding the collar. i'll also attach some documetation / photo of the collar itself so if anyone wants to jump in and try and secure one themselves they can try and get a reasonably compatible one. 
  
 Thanks for reading, comments or suggestions are welcome, keep them sfw please folks!

HUGE THANKS TO THE FOLLOWING PEOPLE:

- thank you to Github user CodeYouFools for help with systemd and some file path / install courtesy updates, as well as general suggestions and help
   
