from machine import Pin, PWM
from umqtt.simple import MQTTClient
import network
import time

# Wi-Fi credentials
ssid = "Wokwi-GUEST"
password = ""

# MQTT details
mqtt_broker = "broker.hivemq.com"
client_id = "esp32-servo-client"

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(0.1)
    print("Connected to WiFi")

# Servo setup
servo = PWM(Pin(21), freq=50)

# Function to convert angle to duty cycle
def angle_to_duty(angle):
    return int((angle / 180) * 102 + 26)  # 0.5ms–2.5ms pulse width (26–128)

# MQTT callback
def sub_cb(topic, msg):
    topic = topic.decode()
    angle = int(msg.decode())
    duty = angle_to_duty(angle)
    print(f"{topic}: {angle}° → duty={duty}")
    servo.duty(duty)
  

# Main program
connect_wifi()
client = MQTTClient(client_id, mqtt_broker)
client.set_callback(sub_cb)
client.connect()

# Subscribe to topics
client.subscribe("esp32/servo1")
print("MQTT connected and subscribed to servo topic")

# Loop to check messages
while True:
    client.check_msg()
    time.sleep(0.1)

