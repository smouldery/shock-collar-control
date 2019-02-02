# setup for  collarbot, tested on Rasbian
#before we start, we check if it's been installed already
if [ -f /root/collarbot ]; then
    echo "this script has been run before on this machine. the script will still run, but this may result in the bot being started twice."
    echo "once installation is complete and pi has rebooted, please edit /etc/rc.local using the command 'sudo nano /etc/rc.local' to remove the duplicated line"
    echo "this line can be identified by looking for a file path ending in /collarbot/collarbot.py, make sure there's only one such line."
    echo "please make a note of this and press enter to continue with the installation, or ctrl+c to end the setup"
    read -p "press enter when ready to continue..." randomvariable
    echo "starting the install now"
fi

#first step, we update the list of packages and update any packages. 
echo "updating package list and any installed packages..."
apt-get update
apt-get upgrade -y
echo "update done!"
echo "installing the required SYSTEM packages (python packages are done in the next step"
echo "we use python3 to run the control script for the transmitter, and talk to the discord bot."
echo "we use python3-pip to install the python modules for the python script."
echo "installing these two now"
apt-get install -y python3 python3-pip
echo "done!"
echo "now we install two python modules - gpiozero controls the gpio pins + transmitter, and discord talks to the discord bot."
echo "we use the pyton installer we installed above to do this with 'pip3 install <packagename>"
pip3 install gpiozero
echo "gpio zero installed!"
pip3 install discord
echo "discord module installed!"
echo "now we're ready to copy the script from github, and install it with your bot key. if you haven't already, create a bot on discord's site (see github wiki for how to do this"
echo "we install this in the current working directory `pwd` under a new folder, collarbot. full path, `pwd`/collarbot/. first we make the folder, then download the script. doing this now."
mkdir `pwd`/collarbot/
wget -O `pwd`/collarbot/collarbot.py 'https://raw.githubusercontent.com/smouldery/shock-collar-control/master/collarbot.py'
echo "done! now we need to add your discord bot key so it works with YOUR bot"
read -p "enter your bot key here then press enter: " botkey
echo "botkey entered was" $botkey
echo "now we write this to the config file where the control script can import it!"
echo "TOKEN = '"$botkey"'" >> `pwd`/collarbot/collarbot_config.py
echo "Great! now we're done with all that, let's make sure the script runs whenever your pi boots."
echo " to do this, we put it in a file designed for this purpose, /etc/rc.local. first, we activate it..."
chmod +x /etc/rc.local
echo "and now we add a line telling it to start our program. this is appended at the end of the file"
sed -i -e '$i \python3 '`pwd`'/collarbot/collarbot.py &\n' /etc/rc.local
echo "great! now the bot will boot at startup. now all we need to do is to reboot and test it out!"
echo "one more thing - if this install script is run more than once, it can cause issues"
echo "so, we need to add something (a file in root, called collarbot, containing 'installed', which we check for at the start of this script"
echo "and if it's present warn the user. adding the file now"
echo "installed" >> /root/collarbot
echo "ok, all done! press enter when you're ready to reboot"
read -p "Press enter to reboot your pi" randomvariable2
reboot

