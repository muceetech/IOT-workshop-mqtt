import network
import time
from machine import Pin, time_pulse_us
from umqtt.simple import MQTTClient

# Wi-Fi and MQTT config
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""
MQTT_BROKER = "broker.hivemq.com"
MQTT_CLIENT_ID = "esp32-distance-sensor"
MQTT_TOPIC = b"esp32/distance"

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        time.sleep(0.1)
    print("Connected to WiFi")

# Measure distance
def get_distance_cm(trigger, echo):
    trigger.off()
    time.sleep_us(2)
    trigger.on()
    time.sleep_us(10)
    trigger.off()
    duration = time_pulse_us(echo, 1, 30000)  # timeout 30ms
    distance_cm = (duration / 2) / 29.4
    return round(distance_cm, 1)

# Setup
trigger = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)

connect_wifi()
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.connect()
print("Connected to MQTT")

# Loop
while True:
    try:
        dist = get_distance_cm(trigger, echo)
        print("Distance:", dist, "cm")
        client.publish(MQTT_TOPIC, str(dist))
    except Exception as e:
        print("Error:", e)
    time.sleep(0.5)


