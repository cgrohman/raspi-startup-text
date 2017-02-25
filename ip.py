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

def send_message(client, twilio_number, numbers, ip_address ):
  for number in numbers:
    message = client.sms.messages.create(to= number,
                                         from_=twilio_number,
                                         body=ip_address)

def load_twilio_config():
  twilio_sid    = <Twilio SID>
  twilio_token  = <Twilio Token>
  twilio_number = <Twilio Phone Number>

  write_to_log('{} {} {}'.format(twilio_sid, twilio_token, twilio_number))
  if not all([twilio_sid, twilio_token, twilio_number]):
    write_to_log('Could not load twilio config')
  return twilio_sid, twilio_token, twilio_number

def main():
  twilio_sid, twilio_token, twilio_number = load_twilio_config()
  client = TwilioRestClient(twilio_sid, twilio_token)
  max_tries = 20
  numbers = ['+12818657476']
  for i in range(0, max_tries):
    ip_address = get_ip('wlan0')
    if ip_address is not None:
      write_to_log(twilio_number+' '+ip_address)
      send_message(client, twilio_number, numbers, ip_address)
      sys.exit()
    time.sleep(1)

if __name__ == "__main__": main()


