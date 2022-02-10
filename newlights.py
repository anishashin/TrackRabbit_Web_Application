from rpi_ws281x import *
import datetime
#import argparse
import time
import sys
import math
import csv

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

def blink_test(strips):
    i=0
    while i<=2:
        if i==0:
            color = RED
        elif i == 1:
            color == ORANGE
        else:
            color = GREEN

        for strip in strips:
            solid(strip, color)
        time.sleep(.2)
        for strip in strips:
            solid(strip, BLACK)
        time.sleep(.2)
        i+=1
        
def comet_test(strip):
    while True:
        comet(strip, WHITE, 40)

#turn an entire strip a solid color.. off is BLACK
def solid(strip, color):
    for light in range(strip.numPixels()):
        strip.setPixelColor(light, color)
    strip.show()
    
#comet function for main strip, looped through with global variable 
def comet(strip, color, comet_length):
    global pos
    print("1")
    if pos>=strip.numPixels()-comet_length:
        print("2")
        pos=0
        solid(strip, BLACK)
        print("after solid")
        
    for light in range(comet_length):
        print("for loop in comet")
        strip.setPixelColor(pos+light, color)
        print("first set")
        strip.setPixelColor(pos-1-light, BLACK)
        print("second set")
    print("end")        
    pos+=comet_length
    strip.show()
    print("shown")

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
    
def run_for_real(strip1, strip2, distance_m, comet_length, color):
    global pos
    global inv_pos
    print(strip1, strip2, distance_m, comet_length, color)
    d_to_l = 30*distance_m #total number of lights we need to actually travel
    total_cycles = math.floor(d_to_l / comet_length) #how many cycles we need to actually do to travel the required distance
    #keep in mind the first strip is only 34*150=5100 lights long
    #case 1 we do not need the second strip
    if d_to_l <= 34*150: #if the number of lights we need to travel is LESS than or equal to that of the first strip (34strips*150lps)
        
        print("first case")
        print("1", total_cycles)
        print("2", type(pos))
        #print("3", range(total_cycles))
        #LEFT OFF HERE
        for i in range(total_cycles): #we know that we only need the first strip, so comet_length * #cycles = d_to_l
            print("heheheh")
            comet(strip1, color, comet_length)
            print("looping first case")
    else: #we require more than one strip, perhaps multiple loops so
        cycles_passed = 0 #how many cycles have we done so far
        print("second case")
        while cycles_passed < total_cycles: #while there are still cycles to go
            print("while loop")
            for i in range(math.floor((34*150)/comet_length)): #this part should run at most this many times in a row unless cut off by cycle counter
                if cycles_passed > total_cycles:
                    break
                print("first for loop")
                comet(strip1, color, comet_length)
                cycles_passed+=1
                

            for j in range(math.floor((6*150)/comet_length)): #this part should run at most this many times in a row unless cut off by cycle counter
                if cycles_passed > total_cycles:
                    break
                print("second for loop")
                inv_comet(strip2, color, comet_length)
                cycles_passed+=1
                

def automated_test_of_run_for_real(strip1, strip2):
    print("Begining tests...")
    tests = [[60, 15], [60, 4], [100, 10], [100, 2], [200, 10], [300, 50]]
    results = []
    for i in range(len(tests)):
        print("test #" + str(i))
        start_time = datetime.datetime.now()
        run_for_real(strip1, strip2, tests[i][0], get_comet_length(tests[i][1], cycle_speed), WHITE)
        end_time = datetime.datetime.now()
        duration = end_time-start_time
        temp_dict = {
            "distance m": tests[i][0],
            "velocity": tests[i][1],
            "theoretical time" : tests[i][0]/tests[i][1],
            "actual time" : duration,
            "constant": get_comet_length(tests[i][1], cycle_speed)/(30*tests[i][1]),
            "comet_length" :get_comet_length(tests[i][1], cycle_speed)
        }
        results.append(temp_dict)
        print(temp_dict)
    print("Tests complete.")
    keys = results[0].keys()
    a_file = open("rfr_tests.csv", "w")
    dict_writer = csv.DictWriter(a_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)
    a_file.close()
        

  
if __name__ == '__main__':
    #===SETUP===#
    #command line arguements collected
    distance_m = int(sys.argv[1])
    velocity_mps = float(sys.argv[6])
    for i in range(len(sys.argv)):
        print(str(i), str(sys.argv[i]), type(sys.argv[i]))
    print(distance_m, type(distance_m), velocity_mps, type(velocity_mps))
    
    # #setup to take in color values once the site can do that...
    # color_str = str(sys.argv[7])
    # #apparently in python 3.10 they actually finally added switch cases but im not using it here for the sake of backwards compatability
    # if color_str == "RED":
    #     comet_color = RED
    # elif color_str == "ORANGE":
    #     comet_color = ORANGE
    # elif color_str == "YELLOW":
    #     comet_color = YELLOW
    # elif color_str == "GREEN":
    #     comet_color = GREEN
    # elif color_str == "BLUE":
    #     comet_color = BLUE
    # elif color_str == "INDIGO":
    #     comet_color = INDIGO
    # elif color_str == "PURPLE":
    #     comet_color = PURPLE
    # elif color_str == "WHITE":
    #     comet_color = WHITE
    # elif color_str == "BLACK":
    #     comet_color = BLACK
    # else:
    #     comet_color = WHITE #failsafe if something goes wrong itll be white
    # #we also probably want to make the brightness dynamic as well, maybe give an option 1-10 and correlate it to the 0-255 range
    
    print("Desired Distance m: " + str(distance_m))
    print("Desired Velocity m/s: " + str(velocity_mps))
    comet_length = get_comet_length(velocity_mps, cycle_speed)
    print("The comet will be: " + str(comet_length) + " pixels long.")

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
    print("Start...")
    blink_test([strip, small_strip])
    #automated_test_of_run_for_real(strip, small_strip)
    start_time = datetime.datetime.now()
    run_for_real(strip, small_strip, distance_m, comet_length, WHITE)
    end_time = datetime.datetime.now()
    dur = end_time-start_time
    print("Duration: " + str(dur))
    print("Done.")
    #===========================================#

    #cleanup any leftover lights
    print("Cleaning up...")
    solid(strip, BLACK)
    solid(small_strip, BLACK)
    print("Done.")