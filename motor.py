import network
import time
from umqtt.simple import MQTTClient
from machine import Pin, PWM

# Adafruit IO MQTT configuration
AIO_SERVER = 'io.adafruit.com'
AIO_PORT = 1883
AIO_USER = 'AnnieHuang'
AIO_KEY = 'aio_ZyPx627n11X7mV4Wqs4hb9HuyCtM'
AIO_FEED_MOTOR = AIO_USER + '/feeds/motor'  # Motor feed

# Define motor control pins for the Cytron Maker Drive
MOTOR_M1A_PIN = PWM(Pin(27))
MOTOR_M1B_PIN = PWM(Pin(15))

# Motor speed (adjusted for safety)
SPEED = 1023

def motor_forward():
    MOTOR_M1A_PIN.duty(SPEED)
    MOTOR_M1B_PIN.duty(0)

def motor_stop():
    MOTOR_M1A_PIN.duty(0)
    MOTOR_M1B_PIN.duty(0)

# MQTT callback function
def mqtt_callback(topic, msg):
    print('Received message:', msg)
    command = msg.decode()
    print(command)
    if command == "1":
        motor_forward()
    elif command == "0":
        motor_stop()

# Connect to MQTT
client = MQTTClient(AIO_USER, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(AIO_FEED_MOTOR)  # Subscribe to motor feed
print('Connected to MQTT')

# Main loop
while True:
    try:
        client.check_msg()
    except:
        client.disconnect()
        time.sleep(5)
        client.connect()
    time.sleep(5)
