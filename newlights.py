from rpi_ws281x import *
import datetime
import time
import argparse
import sys
import math

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

#set some colors for convenience
RED = Color(255,0,0)
ORANGE = Color(255,165,0)
YELLOW = Color(255,255,0)
GREEN = Color(0,255,0)
BLUE = Color(0,0,255)
INDIGO = Color(75,0,130)
PURPLE = Color(128, 0, 128)
WHITE = Color(255,255,255)
BLACK = Color(0,0,0)

#global position variables...
global pos
global inv_pos
inv_pos = 900 #end of the short strip... this works backwards...
pos = 0
cycle_speed = .19411 #one cycle takes on average .19411 seconds.. we should probably take 
                     #another look and see if we can get this more accurate with more tests

#function to do some math to decide comet_length given the speed and cycle speed
def get_comet_length(velocity, cycle_speed):
    return round(30*velocity*cycle_speed)

#turn an entire strip a solid color.. off is BLACK
def solid(strip, color):
    for light in range(strip.numPixels()):
        strip.setPixelColor(light, color)
    strip.show()
    
#comet function for main strip, looped through with global variable 
def comet(strip, color, comet_length):
    global pos
    
    if pos>=strip.numPixels()-comet_length:
        pos=0
        solid(strip, BLACK)
    
    for light in range(comet_length):
        strip.setPixelColor(pos+light, color)
        strip.setPixelColor(pos-1-light, BLACK)
    
    pos+=comet_length
    strip.show()

#comet function for short strip, looped through with global variable  
def inv_comet(strip, color, comet_length):
    global inv_pos
    
    if inv_pos<=comet_length:
        inv_pos = 150*6
        solid(strip, BLACK)  
          
    for light in range(comet_length):
        strip.setPixelColor(inv_pos-light, color)
        strip.setPixelColor(inv_pos+1+light, BLACK)  
    inv_pos-=comet_length
    strip.show()
    
def run(strip1, strip2, distance_m, comet_length, color):
    #we will assume the longer strip is FIRST, only using the short strip when necessary
    distance_traveled = 0

    while distance_traveled < distance_m:
        #first case... only need the long strip
        if distance_m <= 170:
            cycles=0

            while cycles<=math.floor(distance_m/comet_length):
                comet(strip1, color, comet_length)
                cycles+=1
                distance_traveled += math.floor(comet_length/30)

        #second case.. we need both strips
        elif distance_m > 170 and distance_m <= 200:
            long_cycles = 0
            short_cycles = 0

            while long_cycles<=math.floor(170/comet_length):
                comet(strip1, color, comet_length)
                long_cycles+=1
                distance_traveled += math.floor(comet_length/30)

            while short_cycles<=math.floor((distance_m-170)/comet_length):
                inv_comet(strip2, color, comet_length)
                short_cycles+=1
                distance_traveled += math.floor(comet_length/30)

def blink_test(strips):
    i=0
    while i<=3:
        for strip in strips:
            solid(strip, RED)
        time.sleep(.5)
        for strip in strips:
            solid(strip, BLACK)
        time.sleep(.5)
        i+=1
  
if __name__ == '__main__':
    #===SETUP===#
    #command line arguements collected
    distance_m = int(sys.argv[1])
    velocity_mps = float(sys.argv[6])
    print("desired distance m: " + str(distance_m))
    print("Desired Velocity m/s: " + str(velocity_mps))
    comet_length = get_comet_length(velocity_mps, cycle_speed)

    #setup and begin strips
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    small_strip = Adafruit_NeoPixel(SLED_COUNT, SLED_PIN, SLED_FREQ_HZ, SLED_DMA, SLED_INVERT, SLED_BRIGHTNESS, SLED_CHANNEL, SLED_STRIP)
    print("Initialized both strips...")
    strip.begin()
    small_strip.begin()
    print("Began Both Strips...")

    #clear out previous stuff just in case
    solid(strip, BLACK)
    solid(small_strip, BLACK)
    print("Blacked all Pixels")

    #brightness stuff... probably should make this dynamic
    print(str(strip.getBrightness()) + " brightness\n" + str(small_strip.getBrightness()) + " small brightness")
    print("SETUP COMPLETE")
    #===========#

    #===THE ACTUAL CALL TO START HAPPENS HERE===#
    print("Running...")
    blink_test([strip, small_strip])
    #run(strip, small_strip, distance_m, comet_length, WHITE)
    #solid(strip, WHITE)
    #===========================================#

    #cleanup any leftover lights
    solid(strip, BLACK)
    solid(small_strip, BLACK)
    print("Done.")