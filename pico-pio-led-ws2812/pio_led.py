import time
import rp2
from machine import Pin

# define pio function
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1) [31]           # set out pin 1
    nop()        [31]
    nop()        [31]
    nop()        [31]
    nop()        [31]
    nop()        [31]
    set(pins, 0) [31]           # set out pin 0
    nop()        [31]
    nop()        [31]
    nop()        [31]
    nop()        [31]
    nop()        [31]
    wrap() 

sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(15))  # create state machine 

sm.active(1)                # activate state machine

time.sleep(5)               # wait 5 seconds

sm.active(0)                # deactivate state machine



