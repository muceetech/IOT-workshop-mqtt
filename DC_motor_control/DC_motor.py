import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# Wi-Fi + MQTT setup
SSID = 'Wokwi-GUEST'
PASSWORD = ''
MQTT_BROKER = 'broker.hivemq.com'
CLIENT_ID = 'esp32-dc-motor'
TOPIC_SPEED = b'esp32/motor/speed'
TOPIC_DIR = b'esp32/motor/direction'

# Motor pins (L298N or L9110S)
IN1 = Pin(5, Pin.OUT)   # Motor direction
IN2 = Pin(18, Pin.OUT)  # Motor direction
EN = PWM(Pin(19), freq=1000)  # Motor speed

# Init
IN1.off()
IN2.off()
EN.duty(0)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        time.sleep(0.2)
    print("Wi-Fi connected")

def mqtt_callback(topic, msg):
    global IN1, IN2
    msg = msg.decode()
    if topic == TOPIC_SPEED:
        duty = int(int(msg) * 1023 / 100)  # 0-100% to 0-1023
        EN.duty(duty)
        print("Speed set to", duty)
    elif topic == TOPIC_DIR:
        if msg == "cw":
            IN1.on()
            IN2.off()
        elif msg == "ccw":
            IN1.off()
            IN2.on()
        elif msg == "stop":
            IN1.off()
            IN2.off()
        print("Direction:", msg)

connect_wifi()
client = MQTTClient(CLIENT_ID, MQTT_BROKER)
client.set_callback(mqtt_callback)
client.connect()
client.subscribe(TOPIC_SPEED)
client.subscribe(TOPIC_DIR)
print("Connected to MQTT and subscribed to topics")

while True:
    client.check_msg()
    time.sleep(0.1)

