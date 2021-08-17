from machine import Pin, ADC, PWM
import time

led1 = Pin(25, Pin.OUT)
led2 = Pin(12, Pin.OUT)
potPin = ADC(2)
pwm = PWM(Pin(13))
btn = Pin(17, Pin.IN, Pin.PULL_UP)

def btnInt(pPin):
    print("Butona Basildi")
    led2.toggle()

btn.irq(btnInt, Pin.IRQ_FALLING)

pwm.freq(1000)

while True:
    adcVal = potPin.read_u16()
    pwm.duty_u16(adcVal)
    print(adcVal * 3.3 / 65536)
    time.sleep(0.1)