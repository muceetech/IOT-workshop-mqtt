import machine
import network
import time
import ujson
from umqtt.simple import MQTTClient
from mpu6050 import MPU6050

# WiFi and MQTT config
SSID = 'Wokwi-GUEST'
PASSWORD = ''
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = b"esp32/mpu6050"

# Connect to WiFi
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)
while not sta.isconnected():
    time.sleep(0.1)
print("WiFi connected")

# Setup I2C and MPU6050
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
mpu = MPU6050(i2c)

# MQTT Setup
client = MQTTClient("esp32-mpu-client", MQTT_BROKER)
client.connect()
print("MQTT connected")

# Constants
ACC_SCALE = 16384.0  # LSB/g
GYRO_SCALE = 131.0   # LSB/(°/s)
G = 9.81             # m/s²

# Main loop
while True:
    raw = mpu.get_values()

    acc_x = (raw['AcX'] / ACC_SCALE) * G
    acc_y = (raw['AcY'] / ACC_SCALE) * G
    acc_z = (raw['AcZ'] / ACC_SCALE) * G

    gyro_x = raw['GyX'] / GYRO_SCALE
    gyro_y = raw['GyY'] / GYRO_SCALE
    gyro_z = raw['GyZ'] / GYRO_SCALE

    data = ujson.dumps({
        "acc_x": round(acc_x, 2),
        "acc_y": round(acc_y, 2),
        "acc_z": round(acc_z, 2),
        "gyro_x": round(gyro_x, 2),
        "gyro_y": round(gyro_y, 2),
        "gyro_z": round(gyro_z, 2)
    })

    client.publish(MQTT_TOPIC, data)
    print("Published:", data)
    time.sleep(1)

