import network
import time
from umqtt.simple import MQTTClient
from machine import Pin

# Adafruit IO MQTT configuration
AIO_SERVER = 'io.adafruit.com'
AIO_PORT = 1883
AIO_USER = 'AnnieHuang'
AIO_KEY = 'aio_ZyPx627n11X7mV4Wqs4hb9HuyCtM'
AIO_FEED_LED1 = AIO_USER + '/feeds/green'
AIO_FEED_LED2 = AIO_USER + '/feeds/red'

# LED setup
led1 = Pin(32, Pin.OUT)  # Example: GPIO 32
led2 = Pin(12, Pin.OUT)  # Example: GPIO 27

# MQTT callback function
def mqtt_callback(topic, msg):
    print('Received message:', msg)
    if topic == AIO_FEED_LED1.encode():
        led1.value(int(msg))
    elif topic == AIO_FEED_LED2.encode():
        led2.value(int(msg))

# Connect to MQTT
client = MQTTClient(AIO_USER, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(AIO_FEED_LED1)
client.subscribe(AIO_FEED_LED2)
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
