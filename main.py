##Afonso Mota, 67581, app id "trombe"

from network import LoRa
import socket
import time
import ubinascii
import pycom
from machine import Pin, PWM, RTC
import dht22

#time = year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]]
rtc = RTC()
rtc.init((2014, 5, 1, 4, 13, 0, 0, 0))

#initializing LoRa in LoRaWAN mode, selecting the region
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)
pycom.heartbeat(False)

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('XXXXXXXXXXXXXXXXX')
app_key = ubinascii.unhexlify('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')

print("Initializing DHT22 Sensor... ",end='')
DHTcam = dht22.device(Pin.exp_board.G22)
DHTi = dht22.device(Pin.exp_board.G5)
print("Ready!\n")

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    pycom.heartbeat(False)
    pycom.rgbled(0x007f00)
    time.sleep(2.5)
    print('Not yet joined...')

print ('Joined\n')
pycom.heartbeat(True)
pycom.heartbeat(False)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

pwm = PWM(0, frequency=50)
pwm_c = pwm.channel(0, pin='P8', duty_cycle=0.04)
pwm_c.duty_cycle(0.05)


def receive():
    try:
        datainbytes = s.recvfrom(64)
        print(datainbytes)
        message, port = datainbytes

        if (port == 0):
            return None

        decodedmessage = ubinascii.hexlify(message).decode()
        print('Information: ', decodedmessage, '; Port: ', port)

        if (port == 1):
            if (decodedmessage == "00"):
                print("Instruction: Closing the shutters\n")
                #pwm_c.duty_cycle(0.017)
            if (decodedmessage == "01"):
                print("Instrução: Abertura dos servos\n")
                #pwm_c.duty_cycle(0.1)

        if (port == 2):
            if (decodedmessage == "00"):
                print("Instrução: Fecho da persiana\n")
                #pwm_c.duty_cycle(0.017)
            if (decodedmessage == "01"):
                print("Instrução: Abertura da persiana\n")
                #pwm_c.duty_cycle(0.1)

        if (port == 3):
            year = int(decodedmessage[:2], 16) + 2000
            month = int(decodedmessage[2:4], 16)
            day = int(decodedmessage[4:6], 16)
            hour = int(decodedmessage[6:8], 16)
            minute = int(decodedmessage[8:10], 16)
            second = int(decodedmessage[10:12], 16)
            microsecond = int(decodedmessage[14:16], 16)
            hora = year, month, day, hour, minute, second, microsecond
            tzinfo = None
            rtc.init(datetime=(year, month, day, hour, minute, second, microsecond, tzinfo))
            print("Data atualizada com sucesso\n")
            s.bind(3)
            s.setblocking(True)
            s.send(bytes([01, 02, 03, 04]))
            s.setblocking(False)
            receive()
            time.sleep(10)

    except socket.timeout:
        print("Nada recebido")

while (True):
    # start a new measurement (taking 2 seconds) to ensure that the next
    # retrieval of readings has current values
    print('Real Time Clock ->', rtc.now(), '\n')
    # now start a 2nd measurements which - according to the DHT22 datasheet -
    # delivers the measured values from the previous reading
    hasreading=False
    numtrials=0

    while(not hasreading):
        hasreading=DHTcam.trigger()
        numtrials=numtrials+1
        if hasreading:
            print("RH = {}%  T = {}C".format(DHTcam.humidity, DHTcam.temperature))
        else:
            print(DHTcam.status)

    HUMcam_msb=int(DHTcam.humidity*100/256)
    HUMcam_lsb=int(DHTcam.humidity*100%256)

    TMPcam_int=int(DHTcam.temperature*100)
    # if temperature value is negative, then represent it by its 2's complement (16 bit)
    if (TMPcam_int<0):
        TMPcam_int=65536+TMPcam_int

    TMPcam_msb=int(TMPcam_int/256)
    TMPcam_lsb=int(TMPcam_int%256)
    print("RH = {} {}  T = {} {}".format(HUMcam_msb, HUMcam_lsb, TMPcam_msb, TMPcam_lsb))

    '''while(not hasreading):
        hasreading=DHTi.trigger()
        numtrials=numtrials+1
        if hasreading:
            print("RH = {}%  T = {}C".format(DHTi.humidity, DHTi.temperature))
        else:
            print(DHTi.status)

    HUMi_msb=int(DHTi.humidity*100/256)
    HUMi_lsb=int(DHTi.humidity*100%256)

    TMPi_int=int(DHTi.temperature*100)
    # if temperature value is negative, then represent it by its 2's complement (16 bit)
    if (TMPi_int<0):
        TMPi_int=65536+TMPi_int

    TMPi_msb=int(TMPi_int/256)
    TMPi_lsb=int(TMPi_int%256)
    print("RH = {} {}  T = {} {}".format(HUMi_msb, HUMi_lsb, TMPi_msb, TMPi_lsb))'''

    HUMi_msb, HUMi_lsb, TMPi_msb, TMPi_lsb = [0x07, 0xD0, 0x08, 0x10]
    print(HUMcam_msb, HUMcam_lsb, TMPcam_msb, TMPcam_lsb, HUMi_msb, HUMi_lsb, TMPi_msb, TMPi_lsb)

    pycom.rgbled(0x7f7f00)
    s.bind(1)
    s.setblocking(True)
    s.send(bytes([HUMcam_msb, HUMcam_lsb, TMPcam_msb, TMPcam_lsb, HUMi_msb, HUMi_lsb, TMPi_msb, TMPi_lsb]))
    s.setblocking(False)

    receive()

    pycom.heartbeat(False)

    time.sleep(30)

    if (rtc.now()[3] >= 9 and rtc.now()[3] < 20):
        s.bind(4)
        s.setblocking(True)
        s.send(bytes([01]))
        s.setblocking(False)
        print("Abertura da persiana - Enviado para o TTN\n")
        receive()
        time.sleep(10)

    else:
        s.bind(4)
        s.setblocking(True)
        s.send(bytes([00]))
        s.setblocking(False)
        print("Fecho da persiana - Enviado para o TTN\n")
        receive()
        time.sleep(10)

    pycom.rgbled(0x7f0000)
    s.bind(2)
    s.setblocking(True)
    s.send(bytes([rtc.now()[3], rtc.now()[4]]))
    print('Hora enviada (H:M) -> ', rtc.now()[3],':', rtc.now()[4], '\n')
    s.setblocking(False)

    receive()

    pycom.heartbeat(False)

    # wait for such a time period that we have one measurement every 600 seconds
    time.sleep(10)
