
from machine import Pin, I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import time, network, utelegram, dht

I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

telegram_api_key = "YOUR API KEY"

led = Pin("LED", Pin.OUT)
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
lcd.clear()

d = dht.DHT11(machine.Pin(15))

ssid = 'SUPERONLINE_WiFi_7938'
pswd = '47VF4PXKJKFX'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, pswd)

print("Connecting Wifi.", end='')
lcd.putstr("Connecting WiFi")

while not wlan.isconnected() and wlan.status() >= 0:
    print('.', end='')
    lcd.putstr(".")
    time.sleep(0.5)

print('')
print(wlan.ifconfig())
lcd.clear()
lcd.putstr("WiFi Connected")

def get_message(message):
    lcd.clear()
    lcd.putstr(message['message']['text'])
    bot.send(message['message']['chat']['id'], message['message']['text'].upper())

def reply_ping(message):
    print(message)
    bot.send(message['message']['chat']['id'], 'pong')
    
def hum_cb(message):
    d.measure()
    lcd.clear()
    lcd.putstr("Send Hum: " + str(d.humidity()))
    
    # print(message)
    bot.send(message['message']['chat']['id'], d.humidity())
    
def temp_cb(message):
    d.measure()
    lcd.clear()
    lcd.putstr("Send Temp: " + str(d.temperature()))
    
    # print(message)
    bot.send(message['message']['chat']['id'], d.temperature())
    
def led_cb(message):
    msg = message['message']['text']
    msg_sp = msg.split(' ')
    print(msg_sp)
    if len(msg_sp) != 3:
        bot.send(message['message']['chat']['id'], "Yanlis Format /led 1 1")
        return
    
    if msg_sp[1] == '1':
        if msg_sp[2] == '1':
            led.on()
            bot.send(message['message']['chat']['id'], "LED YANDI")
        else:
            led.off()
            bot.send(message['message']['chat']['id'], "LED SONDU")

def clear_cb(message):
    lcd.clear()            
    

bot = utelegram.ubot(telegram_api_key)
bot.register('/ping', reply_ping)
bot.register('/led', led_cb)
bot.register('/temp', temp_cb)
bot.register('/hum', hum_cb)
bot.register('/clear', clear_cb)
bot.set_default_handler(get_message)

print('BOT LISTENING')
lcd.clear()
lcd.putstr("BOT LISTENING")


bot.listen()

