from uart_timeout_any import uartTimeOut
from machine import Pin, ADC
import utime as time
import json

pot1 = ADC(2)
pot2 = ADC(3)
led1 = Pin(25, Pin.OUT)
led2 = Pin(14, Pin.OUT)
led3 = Pin(15, Pin.OUT) 
myUart = uartTimeOut(0, 115200, tx=Pin(16), rx=Pin(17, Pin.IN, Pin.PULL_UP))
mDebug = False

AT_TIMEOUT = 0
AT_OK = 1
AT_ERROR = -1
autoRecv = 1
resp_temp = {"resp": AT_TIMEOUT, "cmd": ""}

server_ip = "192.168.2.135"
server_port = 1337
lastTime = 0
tcpConnected = False

SSID = "SUPERONLINE_WiFi_7938"
PSWD = "47VF4PXKJKFX"

# wait response function
def waitResp(res="OK", timeout=10000):
    resp = []
    byte_res = bytes(str.encode(res))    # convert res parameter to byte to compare 
    retVal = resp_temp
    prvMills = time.ticks_ms()      # save time for calculate timeout

    # wait until timeout expires
    while (time.ticks_ms() - prvMills) < timeout:

        # check uart buffer is empty
        if myUart.any():        
            # read data until \n and append it to response array
            cc = myUart.readline(100)
            resp.append(cc)

        # check if response array len bigger then 1
        if len(resp) > 1:
            # read response and check is match with parameter
            if resp[-1].rstrip() == byte_res:
                retVal["resp"] = AT_OK
                break

            # check response includes ERROR
            elif resp[-1].rstrip() == b"ERROR":
                retVal["resp"] = AT_ERROR
                print("AT CMD ERROR")
                break

    # convert response to str
    # converting string must start from array index 1 
    respStr = ""
    for i in range(1, len(resp)):
        respStr = respStr + resp[i].decode("utf-8")

    # if debug is True print response
    if mDebug:
        print (resp)

    # assign response value to return value
    retVal["cmd"] = respStr
    return retVal

# send AT command and check response is same with parameter
def sendCMD_waitResp(cmd, res="OK", timeout=10000):
    cmd = cmd + "\r\n"      # add \n to end of the string

    # if debug active print send command
    if mDebug:
        print(cmd)
        pass
    
    myUart.write(cmd)   # send cmd to ESP8266
    return waitResp(res, timeout)   # wait cmd response

# send value over tcp connection
def sendTCP_value(pVal, timeout=10000):
    # send 
    mResp = sendCMD_waitResp("AT+CIPSEND=" + str(len(pVal)), res='>', timeout=timeout)
    if mResp["resp"] == AT_OK:
        myUart.write(pVal)
    else:
        print("TCP Send Error!")

# connect TCP server
def startTCP_connection(pIp, pPort, timeout = 10000):
    cmd = sendCMD_waitResp('AT+CIPSTART="TCP","' +
            pIp +
            '",' +
            str(pPort), timeout=timeout)
    return cmd

# connect WiFi with SSID and password
def connect_WiFi(pSSID, pPswd, timeout = 10000):
    return sendCMD_waitResp("AT+CWJAP_CUR=\"" + pSSID + "\",\"" +
                            pPswd + "\"", timeout=timeout)

cmd = sendCMD_waitResp("AT+CWMODE=1", timeout=1000)

print("Scanning APs...")
cmd = sendCMD_waitResp("AT+CWLAP", timeout=5000)
print(cmd["cmd"])

cmd = connect_WiFi(SSID, PSWD)
print(cmd["cmd"])

cmd = sendCMD_waitResp("AT+CIFSR")
print(cmd["cmd"])

time.sleep(1)
print("Connecting TCP...")
cmd = startTCP_connection(server_ip, server_port)

if cmd["resp"] == AT_OK:
    tcpConnected = True

while True:
    potVal1 = pot1.read_u16()
    potVal2 = pot2.read_u16()

    # check incoming UART data
    if myUart.any():
        recData = []
        while myUart.any():
            recv = myUart.readline(100)     # read data from UART 
            recData.append(recv)            # append data to recieve buffer

            if "+IPD" in str(recv):         # check data includes +IPD
                splitData = str(recv).split("|")
                parseData = json.loads(splitData[1])
                print(parseData["LED1"], " " , parseData["LED2"])
                led2.value(int(parseData["LED1"]))
                led3.value(int(parseData["LED2"]))
            
            elif "CLOSED" in str(recv):     # check daha includes CLOSED
                tcpConnected = False

        # print (recData)

    if time.ticks_ms() - lastTime > 1000:
        if tcpConnected:
            sendVal = "#;" + str(potVal1) + ";" + str(potVal2) + ";"
            sendTCP_value(sendVal)
        
        led1.toggle()
        lastTime = time.ticks_ms()

    # time.sleep(1)
