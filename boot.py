import esp
import network
import time
import machine

print('running boot')

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
password = 'hhhhhhhh'

if wlan.isconnected():
    print('connected')
    wlan.disconnect()
    
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('hi', password) 

    tries = 0
    while not wlan.isconnected() and tries < 30:
        print('...')

        time.sleep(5)
        tries = tries + 1
    print('network config:', wlan.ifconfig())
    
    
    if wlan.isconnected():
        print("WiFi connected at", wlan.ifconfig()[0])
    else:
        print("Mission failed")
        

# print current date and time using real-time clock
from machine import RTC

print("inquire RTC time")

rtc = machine.RTC()
rtc.datetime()
print(rtc.datetime())

