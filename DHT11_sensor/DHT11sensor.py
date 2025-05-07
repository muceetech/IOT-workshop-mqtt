import dht
import machine
import time
import network
import ujson
from umqtt.simple import MQTTClient

# Setup
ssid = 'Wokwi-GUEST'
password = ''
mqtt_broker = 'broker.hivemq.com'
mqtt_topic = 'esp32/dht'

# Connect Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
while not wifi.isconnected():
    time.sleep(0.1)

# DHT Sensor on GPIO 15
sensor = dht.DHT22(machine.Pin(15))

# MQTT setup
client = MQTTClient("esp32-dht", mqtt_broker)
client.connect()

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        payload = ujson.dumps({"temp": temp, "hum": hum})
        print("Publishing:", payload)
        client.publish(mqtt_topic, payload)
    except Exception as e:
        print("Error reading sensor:", e)
    time.sleep(2)

