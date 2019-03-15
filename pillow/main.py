#!/usr/bin/env python3

import os
import sys
from PIL import Image

def main():
    print('Howdy')
    print(sys.version)

    image = Image.open('corgi.png')
    # image.save('corgi.png')
    image.show()

if __name__ == '__main__': main()
