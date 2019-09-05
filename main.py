from umqtt.simple import MQTTClient
import time
import machine
import webrepl
import network
from machine import Pin, PWM, ADC
webrepl.start()

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ML2-iPhone', 'Testforesp')
        timeout = 0
        while not sta_if.isconnected():
            print('connecting')
            timeout = timeout + 1
            time.sleep(1)
            if timeout > 10:
                print('connection failed')
                return
    print('connected!')
    print('network config:', sta_if.ifconfig())

do_connect()

myMqttClient = "Mannysesp"
adafruitIoUrl = "io.adafruit.com"
adafruitUsername = "mannyl"
adafruitAioKey = "0a9515b6be2948538d50a785229998ac"

c = MQTTClient(myMqttClient, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
c.connect()

pin = machine.Pin(13, machine.Pin.OUT)
adc = ADC(Pin(36))
pwm = PWM(Pin(21), freq=500, duty=0)

def sub_cb(topic, msg):
    print('test')
    print('test1')
    pin.on()
    print((topic, msg))
    t = 0
    intensity = 500
    print('test2')
    pwm.duty(intensity)
    print('test3')
    while t < 10:
        t = t + 1
        time.sleep(1)
    while t < 70:
        if (adc.read() > 0):
            pwm.duty(intensity)
        else:
            pwm.duty(0)
        time.sleep(1)
        t = t + 1
        intensity += 8
    pin.off()
    pwm.duty(0)
    

c.set_callback(sub_cb)
c.subscribe("mannyl/feeds/alarmtest")

def check_msg(Timer):
    try:
        c.check_msg()
    except:
        print('error')
        machine.reset()


tm = machine.Timer(1)
tm.init(period=500, mode=tm.PERIODIC, callback=check_msg)


