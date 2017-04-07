# raspi-startup-text

Steps to run:
 - Must have wlan0 configured for auto connection
 - edit launcher.sh to have correct directory structure
 - install needed python packages: "pip install -r requirements.txt"
 - chmod 755 launcher.sh
 - run: "sudo crontab -e" and add the following:
     @reboot sh /home/pi/launcher.sh >/home/pi/startup/logs/cronlog 2>&1
     ** Note you may need to alter the directory structure **
 - edit ip.py to add in you Twilio information
