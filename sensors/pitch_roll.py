#!/usr/bin/env python3

import sys
import time
import math
from envirophat import motion

def write(line):
    sys.stdout.write(line)
    sys.stdout.flush()


write("--- Enviro pHAT Monitoring ---")

try:
    while True:
        acc_values = [round(x, 2) for x in motion.accelerometer()]
        ax = acc_values[0]
        ay = acc_values[1]
        az = acc_values[2]
        
        pitch = 180 * math.atan(ax/math.sqrt(ay*ay + az*az))/math.pi
        roll = 180 * math.atan(ay/math.sqrt(ax*ax + az*az))/math.pi
        
        if roll > -45 and roll < 45:
            orientation = 'landscape'
        elif roll >= 45 or roll <= -45:
            orientation = 'vertical'

        output = """
Accelerometer: {ax}g {ay}g {az}g

Pitch: {p}
Roll: {r}

Orientation: {o}

""".format(
            ax=acc_values[0],
            ay=acc_values[1],
            az=acc_values[2],
            p = pitch,
            r = roll,
            o = orientation
        )

        output = output.replace("\n", "\n\033[K")
        write(output)
        lines = len(output.split("\n"))
        write("\033[{}A".format(lines - 1))

        time.sleep(.1)

except KeyboardInterrupt:
    pass
