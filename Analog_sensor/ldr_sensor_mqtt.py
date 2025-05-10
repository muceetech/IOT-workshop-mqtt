
import network
import time
from machine import ADC, Pin
from umqttsimple import MQTTClient

# ===== DECLARATION =====

GAMMA = 0.7;
RL10 = 50;

# ===== CONFIGURATION =====
#WIFI_SSID = 'Wokwi-GUEST'
#WIFI_PASS = ''

MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'esp32-analog-client'
MQTT_TOPIC = b'esp32/ldr'

# ===== CONNECT TO WIFI =====
def connect_wifi():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('Wokwi-GUEST', '')
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")
def connect_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print("Connected to MQTT broker")
    return client

# ===== MAIN PROGRAM =====
connect_wifi()
client = connect_mqtt()

adc = ADC(Pin(32))        # GPIO32
adc.atten(ADC.ATTN_11DB)  # Full range: 0 - 3.6V
adc.width(ADC.WIDTH_12BIT)

while True:
    value = adc.read()                    # 0-4095
    voltage = (value / 4095) * 3.3        # Convert to volts
    resistance = 2000 * voltage / (3.3 - voltage)
    lux = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA))
    msg = "{:.0f}".format(lux/10)
    print(msg, "Lux")
    client.publish(b'esp32/ldr', msg)
    time.sleep(0.1)  # 100 ms sampling
