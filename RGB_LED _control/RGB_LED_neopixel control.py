import network, time, ujson
from umqtt.simple import MQTTClient
from machine import Pin
import neopixel

# WiFi connection
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("Wokwi-GUEST", "")
while not station.isconnected():
    time.sleep(0.1)

np = neopixel.NeoPixel(Pin(5), 1)

def set_color(r, g, b):
    np[0] = (r, g, b)
    np.write()

# MQTT setup
def sub_cb(topic, msg):
    data = ujson.loads(msg)
    set_color(data['r'], data['g'], data['b'])

client = MQTTClient("esp32-neopixel", "broker.hivemq.com", port=1883)
client.set_callback(sub_cb)
client.connect()
client.subscribe("esp32/rgb")

print("Listening for RGB updates...")
while True:
    client.check_msg()
    time.sleep(0.1)
