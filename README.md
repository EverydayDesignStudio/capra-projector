# Capra Explorer
_Artefact that stores -and lets one browse- the archive of photos and data collected with the Capra Collector._


## Hardware
The Explorer consists of:

- Raspberry Pi 4
- Explorer Control PCB
- [Samsung T5](https://www.amazon.com/dp/B073GZBT36/ref=cm_sw_em_r_mt_dp_U_5zDuDbEAWBSE9) 500GB SSD
- Aaxa Pico Projector ([P2-B](http://aaxatech.com/products/P2B_pico_projector.html); previously [HD-Pico](http://aaxatech.com/products/hd_pico_projector.html))
- Adafruit NeoPixel Strip

The Explorer Control PCB connects all control components to the raspberry pi.  The control components on this PCB are:

| Name | Function   | Pin             | Component*** |
| ---- | ---------- | --------------- | ------------ |
| S1   | NEXT       | BCM 6           | Tactile      |
| S2   | MODE*      | ADC ch 2        | Tactile      |
| S3   | PREV       | BCM 12          | Tactile      |
| S4   | PLAY/PAUSE | BCM 5           | Tactile      |
| SL1  | MODE 1*    | ADC ch 2        | Slider       |
| SL1  | MODE 2*    | ADC ch 1        | Slider       |
| SL1  | MODE 3*    | ADC ch 0        | Slider       |
| SW3  | NAVIGATE   | BCM A=23 B=24** | Rotary Encoder - rotation |
| SW3  | ALL/ONE    | BCM 25          | Rotary Encoder - switch   |
| ACCELEROMETER | ACC_X    | ADC ch 7 | Sparkfun Module |
| ACCELEROMETER | ACC_Y    | ADC ch 6 | Sparkfun Module |
| ACCELEROMETER | ACC_Z    | ADC ch 5 | Sparkfun Module |

_\*The PCB offers some flexibility. Either S2 is installed on the board OR SL1 is installed. In the case of SL1, the three positions of the slider correspond to the three modes. In the case of S2 the user would toggle through the modes by repeatedly pressing the button. Hence the overlapping pin numbers between SL1 - MODE2 and S2._

_\**The component in question here is a rotary encoder. This component uses two pins (A & B) to determine either clockwise or counterclockwise rotation. Numbers in table are BCM numbers_

_\***Component Numbers are:_


| Component      | Manufacturer Number   |
| -------------- | --------------------- |
| Tactile        | [2-1825910-7 ](https://www.digikey.ca/products/en?keywords=450-1642)
| Slider         | [MHS233K](https://www.digikey.ca/products/en?keywords=679-1868)
| Rotary Encoder | [PEC11R-4215F-N0024](https://www.digikey.ca/products/en?keywords=PEC11R-4215F-N0024-ND)
| Sparkfun Accelerometer | [ADXL337 (breakout)](https://www.sparkfun.com/products/12786)

> __DESIGN ERROR:__
The PCB has a design error regarding the MODE-related channels on the ADC (ch 0, 1, 2). This design error has two consequences:
1. Channels 0, 1, 2 on the ADC are left floating when disconnected at the slider switch. These should be pulled low by separate 10kΩ resistors.
2. The base of the switch is pulled low by a 10kΩ resistor (R1). Instead of pulling the base low, pull it high instead (i.e. connect R1 to the base of the switch and 3V3)
