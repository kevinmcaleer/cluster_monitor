from wifi_config import SSID, PASSWORD 
import network
from umqttsimple import MQTTClient
from machine import Pin
from time import sleep, ticks_ms
import plasma
from plasma import plasma_stick, plasma2040
from breakout_bme280 import BreakoutBME280
from pimoroni_i2c import PimoroniI2C
import json

I2C_PINS = {"sda": 20, "scl": 21}

i2c = PimoroniI2C(**I2C_PINS)
bme = BreakoutBME280(i2c)

MQTT_BROKER = "192.168.1.152"
CLIENT_ID = "cluster monitor"

# LED Strip setup
brightness = 0.25 # Set the overall brightness
NUM_LEDS = 36 # Set how many LEDs you have
SPEED = 20 # The SPEED that the LEDs cycle at (1 - 255)
UPDATES = 60 # How many times the LEDs will be updated per second

# WS2812 / NeoPixel™ LEDs
led_strip = plasma.APA102(NUM_LEDS, 0, 0, plasma2040.DAT, plasma2040.CLK)

# Start updating the LED strip
led_strip.start()

offset = 0.0

def connect_wifi():
        """ Connect to Wi-Fi."""

        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            print('.', end="")
            sleep(0.25)
        print(f'Connected to WiFi, IP is: {sta_if.ifconfig()[0]}')
        return sta_if

wlan = connect_wifi()

MQTT_BROKER = "192.168.1.152"
CLIENT_ID = "burgerbot"
topic = "cluster/colour"
status_topic = "cluster/status"

led = Pin("LED", Pin.OUT)
led.on()

GREEN = 0.3
RED = 0.0
BLUE = 0.6
YELLOW = 0.16

def warning():
    print("WARNING")
    hue = YELLOW
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, hue, 1.0, brightness)

def alert():
    print("ALERT")
    hue = RED
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, hue, 1.0, brightness)

def normal():
    print("NORMAL")
    hue = BLUE
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, hue, 1.0, brightness)

def green():
    print("GREEN")
    hue = GREEN
    for i in range(NUM_LEDS):
        led_strip.set_hsv(i, hue, 1.0, brightness)

def sub_cb(topic, msg):
    global brightness
    """ Subscribe call back """
    global bot
    
    msg = msg.decode("utf-8")
    topic = topic.decode("utf-8")
     
    print(f'topic {topic}, msg {msg}')
    
    if 'alert' in msg:
        print(f"alert {msg}")
        alert()

    if 'warning' in msg:
        print(f"warning {msg}")
        warning()

    if 'normal' in msg:
        print(f"normal {msg}")
        normal()
                   
    if 'green' in msg:
        print(f"green {msg}")
        green()
        
    if 'brightness' in msg:
        payload = json.loads(msg)
        
        print(f"brightness set to {brightness}")
        brightness = float(payload["brightness"]) 

def connect_and_subscribe():
    """ Connect to the MQTT broker and subscribe to the topic"""
    global CLIENT_ID, MQTT_BROKER
    
    print(CLIENT_ID, MQTT_BROKER, topic, )
    client = MQTTClient(CLIENT_ID, MQTT_BROKER, keepalive=30)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic)
    
    return client

def restart_reconnect():
    global client
    print('Failed to connect to MQTT broker, Reconnecting...')
    sleep(10)
    client = connect_and_subscribe()

def take_reading(client):
    reading = bme.read()
    temp = round(reading[0],1)
    pressure = round(reading[1],1)
    humidity = round(reading[2],1)
    msg = json.dumps({'temperature': temp,
           'pressure': pressure,
           'humidity': humidity})
    print(f'BME Reading: {msg}')
    print(f'topic is {status_topic}')
    client.publish(status_topic, msg)

# Connect to wifi
timer = ticks_ms()
print("Connecting to Wifi...")
while wlan.isconnected() == False:
    current_time = ticks_ms()
    if current_time >= (timer + 250):
        timer = ticks_ms()
        led.toggle()
    
print("Connected")
print(wlan.ifconfig())

try:
    client = connect_and_subscribe()
except OSError as e:
    client = None
    restart_reconnect()

normal()

while True:
    try:
        client.check_msg()
        current_time = ticks_ms()
        if current_time >= (timer + 1000):
            timer = ticks_ms()
            take_reading(client)
            print(timer, current_time)
            led.toggle()
            
    except OSError as e:
        restart_reconnect()