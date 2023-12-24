import time, machine, array
import rp2
from machine import Pin

NUM_LEDS = 6
BRIGHTNESS = 0.1

# change color format from array to 24 bit value
def setColor(color):
    r = int(color[0]*BRIGHTNESS)
    g = int(color[1]*BRIGHTNESS)
    b = int(color[2]*BRIGHTNESS)
    return (g<<16) + (r<<8) + b

# pio fcuniton
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    wrap_target()
    out(x, 1)               # get 1 bit from of statmachine input buffer and add it to x variable
    set(pins, 1) [1]        # set output pin value 1
    mov(pins, x) [1]        # move x value to output pin
    set(pins, 0)            # set output pin value 0
    wrap()

sm = rp2.StateMachine(0, ws2812, freq=5000000, set_base=Pin(15), out_base=Pin(15))          # define statemachine
sm.active(1)                                                                                # activate statemachine

ar = array.array("I", [0 for _ in range(NUM_LEDS)])                                         # an array for storing led color values

# set first color of leds
for i in range(NUM_LEDS):
    ar[i] = setColor((255, 0, 0))
 
sm.put(ar, 8)               # send first color values to state machine buffer
time.sleep_ms(1000)         # wait 1 second

cc = 1

# start color cycle
while True:
    ar[cc - 1] = setColor((255, 0, 0))      # set previus pixel red
    ar[cc] = setColor((0, 255, 0))          # set pixel green
    sm.put(ar, 8)                           # send pixel values to state machine buffer
    cc = (cc + 1) % NUM_LEDS                
    time.sleep(1)
