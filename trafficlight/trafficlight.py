import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# Setup Wi-Fi and MQTT
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""
MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = "esp32-traffic"
MQTT_TOPIC = b"esp32/traffic"

# Pins for Red, Yellow, Green LEDs
led_red = Pin(19, Pin.OUT)
led_yellow = Pin(18, Pin.OUT)
led_green = Pin(5, Pin.OUT)
led_red.value(0)
led_yellow.value(0)
led_green.value(0)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        time.sleep(0.2)
    print("WiFi Connected!")

def handle_message(topic, msg):
    color = msg.decode()
    print("Received:", color)
    led_red.value(0)
    led_yellow.value(0)
    led_green.value(0)
    if color == "red":
        led_red.value(1)
    elif color == "yellow":
        led_yellow.value(1)
    elif color == "green":
        led_green.value(1)

def main():
    connect_wifi()
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
    client.set_callback(handle_message)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Connected to MQTT broker")

    while True:
        client.check_msg()
        time.sleep(0.1)

main()

