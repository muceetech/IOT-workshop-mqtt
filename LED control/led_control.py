import network
import time
from umqtt.simple import MQTTClient
import machine

# WiFi config
ssid = 'Wokwi-GUEST'
password = ''

# MQTT config
mqtt_server = 'broker.hivemq.com'
client_id = 'esp8266_client'
topic_sub = b'esp/led'

# LED setup
led = machine.Pin(2, machine.Pin.OUT)  # onboard LED, active LOW

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to WiFi...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(0.5)
    print('WiFi connected:', wlan.ifconfig())

def on_message(topic, msg):
    print('Received:', topic, msg)
    if msg == b'on':
        led.value(1)
    elif msg == b'off':
        led.value(0)

def connect_mqtt():
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to MQTT and subscribed to', topic_sub)
    return client

# Main
connect_wifi()
client = connect_mqtt()

while True:
    try:
        client.check_msg()
    except OSError as e:
        print('Error:', e)
        time.sleep(5)
        machine.reset()

