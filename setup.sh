# setup for  collarbot, tested on Rasbian 9 (Stretch)
echo "starting the install now"

#first step, we update the list of packages.. 
echo "updating package list ..."
apt-get update
echo "update done!"
echo "installing the required SYSTEM packages (python packages are done in the next step"
echo "we use python3 to run the control script for the transmitter, and talk to the discord bot."
echo "we use python3-pip to install the python modules for the python script."
echo "installing these two now"
apt-get install -y python3 python3-pip pigpio
echo "done! now we install the discord module which talks to the discord bot."
echo "we use the pyton installer we installed above to do this with 'pip3 install <packagename>"
pip3 install discord
echo "discord module installed!"
echo "now we're ready to copy the script and defaults file from github, and install it with your bot key. if you haven't already, create a bot on discord's site (see github wiki for how to do this"
echo "we install this in /opt/ under a new folder, collarbot. full path, /opt/collarbot/. first we make the folder, then download the files. doing this now."
mkdir /opt/collarbot/
wget -O /opt/collarbot/collarbot_config.py 'https://raw.githubusercontent.com/smouldery/shock-collar-control/master/collarbot_config.py'
wget -O /opt/collarbot/collarbot.py 'https://raw.githubusercontent.com/smouldery/shock-collar-control/master/collarbot.py'
echo "done! now we need to add your discord bot key so it works with YOUR bot"
read -p "enter your bot key here then press enter: " botkey
echo "botkey entered was" $botkey
echo "now we write this to the config file where the control script can import it!"
echo "TOKEN = '"$botkey"'" >> /opt/collarbot/collarbot_config.py
echo "now we make sure the folder and files are executable..."
chown -R nobody /opt/collarbot/
chmod -R 755 /opt/collarbot/
echo "Great! now we're done with all that, let's make sure the script runs whenever your pi boots."
echo "To do this we first make sure the bot can access the GPIO ports"
usermod -a -G gpio nobody
echo "next, we add it as a service to systemd. this involves downloading a file from the github and putting it in the relevant folder,"
echo " reloading systemd, enabling the service to start at boot, and finally, starting the service"
wget -O /etc/systemd/system/collarbot.service 'https://raw.githubusercontent.com/smouldery/shock-collar-control/master/collarbot.service'
chmod 755 /etc/systemd/system/collarbot.service
systemctl daemon-reload
systemcrl enable --now pigpiod
systemctl enable --now collarbot
echo "in about 5-10 seconds your bot should now boot. check your discord server and try it! type !help for a list of commands"
