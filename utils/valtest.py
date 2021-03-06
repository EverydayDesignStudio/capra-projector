"""
# ==============================================================
#      ---   Exploring metadata as a design material   ---
# ==============================================================

Tickets
- try reading values from MCP without other GPIO pins configured

"""
#from oloFunctions import *
#              _____
#  ______________  /____  _________
#  __  ___/  _ \  __/  / / /__  __ \
#  _(__  )/  __/ /_ / /_/ /__  /_/ /
#  /____/ \___/\__/ \__,_/ _  .___/
#  ========================/_/====

import sh
sh.init()
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


import time
#from oloFunctions import *

import queue
from statistics import mean

"""
\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\
Migratable to sh.py or oloFunctions
=\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==
"""
class col:
    prp = '\033[95m'
    vio = '\033[94m'
    gre = '\033[92m'
    yel = '\033[93m'
    ora = '\033[91m'
    none = '\033[0m'
    red = '\033[1m'
    und = '\033[4m'

def exectime(then):
    now = time.time()
    extime = now - then
    return "{0:.6f}".format(round(extime,7))


"""
\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\
=\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==\==
"""


# print(sh.CLK)
# mcp = Adafruit_MCP3008.MCP3008(clk=sh.CLK, cs=sh.CS, miso=sh.MISO, mosi=sh.MOSI)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

stablizeSliderPos = queue.Queue(maxsize=20) # average out 20 values

# # GPIO configuration:
# gpio.setup(sh.switch1, gpio.IN) #gpio 16  - three pole switch 1
# gpio.setup(sh.switch2, gpio.IN) #gpio 18  - three pole switch 2

print('Reading MCP3008 values, press Ctrl-C to quit...')

#  ______
#  ___  /___________________
#  __  /_  __ \  __ \__  __ \
#  _  / / /_/ / /_/ /_  /_/ /
#  /_/  \____/\____/_  .___/
# ===================/_/===

while(True):
    # Read all the ADC channel values in a list.
    then = time.time()
    readValues()

    if (sh.values[6] < 100):
        if (stablizeSliderPos.full()):
            stablizeSliderPos.get()
        stablizeSliderPos.put(sh.values[7])
        avgPos = int(mean(list(stablizeSliderPos.queue)))
    else:
        with stablizeSliderPos.mutex:
            stablizeSliderPos.queue.clear()
        avgPos = 0

    #print(col.yel + 'readvals exec time: ' + str(exectime(then)) + col.none)
    # Print the ADC values.
    then = time.time()
    #print sh.values[0]
    timeframe()
    print (col.red + sh.timeframe + col.none)
    #printValues(sh.values)
    print(sh.values)
    print("    @@ linearlized volume value: {}".format(linearlizeVolume(sh.values[4])))
#    print("    @@ qsize: {}, mean: {}".format(stablizeSliderPos.qsize(), avgPos))

    #print('printvals exec time: ' + str(exectime(then)))

    # Pause for half a second.
    #time.sleep(0.5)
