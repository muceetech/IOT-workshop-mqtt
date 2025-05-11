import machine 
import time

# Bipolar stepper motor connected to A4988 motor controller 
# dir pin to pin 18 , Step pin to pin 5 of ESP32. change as per yout neeed
# Connections from A4988 driver IC to stepper motor
#  Stepper motor - A4988 Driver
#  A+ - 1B
#  A- - 1A
#  B+ - 2A
#  B- - 2B


dir_pin = machine.Pin(5, machine.Pin.OUT)
step = machine.Pin(18,machine.Pin.OUT)

dir_pin.value(1)
while True:
	step.value(1)
	time.sleep(0.01)
	step.value(0)
	time.sleep(0.01)
