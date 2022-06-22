# Clean console
import os
os.system('cls')

# Sending commands
import pydirectinput

# OCR for game extraction
import pytesseract
# Tranformation framework
import numpy as np
# Visualize captured frames
from matplotlib import pyplot as plt
# Bring time for poses
import time
# Custom Game environement
from WebGame import WebGame

env = WebGame()

while(1):
    done, done_cap = env.getDone()
    if(done) :
        time.sleep(1)
        print('Action')
        env.step(0)