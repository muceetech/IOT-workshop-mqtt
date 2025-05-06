from machine import Pin, PWM
import network, time, ujson
from umqtt.simple import MQTTClient

# Connect to WiFi
ssid = 'Wokwi-GUEST'
password = ''
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while not station.isconnected():
    time.sleep(0.1)

# Set up PWM pins
pwm_red = PWM(Pin(21), freq=1000)
pwm_green = PWM(Pin(22), freq=1000)
pwm_blue = PWM(Pin(23), freq=1000)

def set_color(r, g, b):
    pwm_red.duty(int(r * 4.01))    # Convert 0-255 to 0-1023
    pwm_green.duty(int(g * 4.01))
    pwm_blue.duty(int(b * 4.01))

# MQTT setup
def sub_cb(topic, msg):
    data = ujson.loads(msg)
    set_color(data['r'], data['g'], data['b'])

client = MQTTClient("esp32-rgb", "broker.hivemq.com", port=1883)
client.set_callback(sub_cb)
client.connect()
client.subscribe("esp32/rgb")

print("Listening for RGB updates...")
while True:
    client.check_msg()
    time.sleep(0.1)

