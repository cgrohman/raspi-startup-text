#!/usr/bin/pyton
from twilio.rest import TwilioRestClient
import os
import sys
import time
import socket
import fcntl
import struct


def write_to_log(text):
  with open('logs/runtime.log','a+') as file:
    file.write(text+'\n')

def get_ip(ifname):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
           s.fileno(),
           0x8915,  # SIOCGIFADDR
           struct.pack('256s', ifname[:15])
           )[20:24])
  except:
    return None

def send_message(client, twilio_number, numbers, body ):
  for number in numbers:
    message = client.sms.messages.create(to= number,
                                         from_=twilio_number,
                                         body=body)

def load_twilio_config():
  config = {}
  execfile('config.py', config)

  twilio_sid    = config['TWILIO_SID']
  twilio_token  = config['TWILIO_TOKEN']
  twilio_number = config['TWILIO_NUMBER']

  if not all([twilio_sid, twilio_token, twilio_number]):
    write_to_log('Could not load twilio config')
  return twilio_sid, twilio_token, twilio_number

def main():
  max_tries = 20
  numbers   = ['+12818657476']
  links     = ['wlan0','eth0']
  twilio_sid, twilio_token, twilio_number = load_twilio_config()
  client = TwilioRestClient(twilio_sid, twilio_token)
  for i in range(0, max_tries):
    for link in links:
      ip_address = get_ip(link)
      if ip_address is not None:
        write_to_log(twilio_number+' '+ip_address)
        send_message(client, twilio_number, numbers, '\n'+link +': '+ip_address)
        sys.exit()
    time.sleep(1)

if __name__ == "__main__": main()


