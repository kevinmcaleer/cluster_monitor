# RGB Test
from colour import rgb2hex, hex2rgb, hsv2hex, rgb2hsv
import plasma
from plasma import plasma2040

r = 0
g = 0
b = 255

h,s,v = rgb2hsv(r,g,b)
hex = hsv2hex(h,s,v)

NUM_LEDS = 36

print(f'hex: {hex}')

# WS2812 / NeoPixel™ LEDs
led_strip = plasma.APA102(NUM_LEDS, 0, 0, plasma2040.DAT, plasma2040.CLK)

# Start updating the LED strip
led_strip.start()

for i in range(NUM_LEDS):
    led_strip.set_hsv(i,h,s,v)



