from espzero import LED
from time import sleep
led1 = LED(16)
led2 = LED(5)
led3 = LED(4)

while True:
    led1.on()
    led2.off()
    led3.off()
    sleep(2)
    
    led1.off()
    led2.on()
    led3.off()
    sleep(1)
    
    led1.off()
    led2.off()
    led3.on()
    sleep(2)
    


