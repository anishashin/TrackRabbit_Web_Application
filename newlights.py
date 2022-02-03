from rpi_ws281x import *
import datetime
import time
import argparse
import sys

#for the longer pcm strand
LED_COUNT = 150*34
LED_PIN = 21
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 127
LED_INVERT = False
LED_CHANNEL = 0
LED_STRIP = ws.WS2811_STRIP_GRB


#for the shorter pwm strand
SLED_COUNT = 150*34
SLED_PIN = 18
SLED_FREQ_HZ = 800000
SLED_DMA = 10
SLED_BRIGHTNESS = 127
SLED_INVERT = False
SLED_CHANNEL = 0
SLED_STRIP = ws.WS2811_STRIP_GRB

RED = Color(255,0,0)
ORANGE = Color(255,165,0)
YELLOW = Color(255,255,0)
GREEN = Color(0,255,0)
BLUE = Color(0,0,255)
INDIGO = Color(75,0,130)
PURPLE = Color(128, 0, 128)
WHITE = Color(255,255,255)
BLACK = Color(0,0,0)

RAINBOW = (RED, ORANGE, YELLOW, GREEN, BLUE, INDIGO, PURPLE, BLACK)
CHRISTMAS = (RED, WHITE, GREEN)
HALLOWEEN = (ORANGE, WHITE, PURPLE)

global pos
global start_time
global inv_pos
global inv_start_time

inv_pos = 900 #end of the short strip... this works backwards...
pos = 0
comet_length = 90

def solid(strip, color):
    for light in range(strip.numPixels()):
        strip.setPixelColor(light, color)
    strip.show()
    
def thirds(strip, color1, color2, color3):
    for light in range(int(strip.numPixels()/3)):
        strip.setPixelColor(light, color)
    for light in range(int(strip.numPixels()/3)):
        strip.setPixelColor(light+int(strip.numPixels()/3), color)
    for light in range(int(strip.numPixels()/3)):
        strip.setPixelColor(light+2*int(strip.numPixels()/3), color)
    strip.show()

def comet(strip, color, comet_length):
    global pos
    global start_time
    
    if pos>=strip.numPixels()-comet_length:
        pos=0
        solid(strip, BLACK)
        #end_time = datetime.datetime.now()
        #print("Loop Complete\n" + str(end_time-start_time))
    
    for light in range(comet_length):
        strip.setPixelColor(pos+light, color)
        strip.setPixelColor(pos-1-light, BLACK)
    
    pos+=comet_length
    strip.show()
    
def inv_comet(strip, color, comet_length):
    global inv_pos
    global start_time
    
    if inv_pos<=comet_length:
        inv_pos = 150*6
        solid(strip, BLACK)
        print(datetime.datetime.now()-start_time)
        #print("End of first strip\n" + str(inv_end_time - inv_start_time))
    
    for light in range(comet_length):
        strip.setPixelColor(inv_pos-light, color)
        strip.setPixelColor(inv_pos+1+light, BLACK)
        
    inv_pos-=comet_length
    strip.show()
    
def comet3(strip, color1, color2, color3, comet_length):
    global pos
    
    if pos>=strip.numPixels()-3*comet_length:
        pos=0
        solid(strip, BLACK)    
    
    for light in range(comet_length):
        strip.setPixelColor(pos+light, color1)
        strip.setPixelColor(pos+comet_length+light, color2)
        strip.setPixelColor(pos+2*comet_length+light, color3)
        strip.setPixelColor(pos-1-light, BLACK)
        strip.setPixelColor(pos-comet_length-1-light, BLACK)
        strip.setPixelColor(pos-(2*comet_length)-1-light, BLACK)
        
    pos+=comet_length*3
    strip.show()
    

def comet_test(comet_length):
    #COMET LENGTH SHOULD BE EASILY DIVISIBLE INTO 150 ALWAYS NO MATTER WHAT OR ELSE BAD STUFF HAPPENS
    while True:
        counter = 0
        counter2 = 0
        while counter<(150*6/comet_length)-1:
            inv_comet(small_strip, INDIGO, comet_length)
            counter+=1
        solid(small_strip, BLACK)
        while counter2<(LED_COUNT/comet_length)-1:
            comet(strip, INDIGO, comet_length)
            counter2+=1
        solid(strip, BLACK)
        

test_length=10
if __name__ == '__main__':
    print(sys.argv[1])
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    small_strip = Adafruit_NeoPixel(SLED_COUNT, SLED_PIN, SLED_FREQ_HZ, SLED_DMA, SLED_INVERT, SLED_BRIGHTNESS, SLED_CHANNEL, SLED_STRIP)
    print("Initialized both strips...")
    strip.begin()
    small_strip.begin()
    print("Began Both Strips...")
    solid(strip, BLACK)
    solid(small_strip, BLACK)
    print("Blacked all Pixels O.o 8======D")
    print(str(strip.getBrightness()) + " brightness\n" + str(small_strip.getBrightness()) + " small brightness")
    start_time = datetime.datetime.now()
    #inv_start_time = datetime.datetime.now()
    print("Set timer starts.. this doesnt really work anymore...")
    print("Running test loop")
    solid(strip, BLUE)
    #comet_test(test_length)
