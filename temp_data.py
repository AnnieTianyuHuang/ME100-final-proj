import machine
import network
import urequests
import dht
import time

# Pin definitions
ldr_pin = machine.ADC(machine.Pin(33))
dht_pin = machine.Pin(14)
sensor = dht.DHT11(dht_pin)

# IFTTT settings
ifttt_key = "dNsQVLSLx83M-hG8IMyOJNV3QAcRQnpK4ZUyj1GBCFB"
event_name = "temp_data"
ifttt_url = "https://maker.ifttt.com/trigger/{}/with/key/{}"

def get_light_percentage():
    ldr_value = ldr_pin.read()
    percentage = (ldr_value * 100) / 4095
    return percentage

def send_data_to_sheet(value1, value2, value3):
    url = ifttt_url.format(event_name, ifttt_key) + "?value1={}&value2={}&value3={}".format(value1, value2, value3)
    print(url)
    response = urequests.get(url)
    print(response.text)
    response.close()
    
def check_temp_and_notify(temperature):
    if temperature > 25:
        url = 'https://maker.ifttt.com/trigger/temp_exceed_25/json/with/key/dNsQVLSLx83M-hG8IMyOJNV3QAcRQnpK4ZUyj1GBCFB'.format(ifttt_key)
        response = urequests.get(url)
        print("Temperature exceeded 25°C. Phone call initiated.")
        response.close()

while True:
    sensor.measure()
    humidity = sensor.humidity()
    temperature = sensor.temperature()
    light_percentage = get_light_percentage()

    print("Values are", humidity, temperature, light_percentage)

    send_data_to_sheet(humidity, temperature, light_percentage)
    check_temp_and_notify(temperature)
    time.sleep(10)
