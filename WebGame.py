# Screen captures
from mss import mss
# Frame processing
import cv2
# OCR for game extraction
import pytesseract
# Sending commands
import pydirectinput
# Environement components
from gym import Env
from gym.spaces import Box, Discrete
# Tranformation framework
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\c.molinier\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract'

class WebGame(Env) :
    # Setup environement action and observation
    def __init__(self) :
        super().__init__()

        # Setup spaces
        self.observation_space = Box(low=0, high=255, shape=(1,83,100), dtype=np.uint8)
        self.action_space = Discrete(3)

        # Define extraction parameters for the game
        self.cap = mss()
        mon2 = self.cap.monitors[2]
        self.game_location = {'top': mon2['top']+80, 'left': mon2['left'], 'width': 1900,'height': 900}
        self.done_location = {'top': mon2['top']+360, 'left': mon2['left']+625, 'width': 600,'height': 90} 
        #{'mon':2 ,'top': 405, 'left': 630, 'width': 660, 'height': 70}

    # Do someting in the game
    def step(self, action):
        # Action key - 0 = Space, 1 = Duck(down), 2 = No action (no op)

        action_map = {
            0: 'space',
            1: 'down',
            2: 'no_op'
        }

        if action !=2 :
            pydirectinput.press(action_map[action])
        

    # visualize game
    def render(self):
        pass
    
    # Restart game
    def restart(self):
        pass

    # Close down the observation
    def close(self):
        pass

    # Get the part of the observation of the game
    def getObservation(self):
        # Get screen capture
        raw = np.array(self.cap.grab(self.game_location)) [:,:,:3] #.astype(np.uint8)
        # Grayscale
        gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
        # Resize
        resized = cv2.resize(gray, (200, 94))
        # Add channels first
        channel = np.reshape(resized, (1, 94, 200))
        return channel  

    # Get the done text
    def getDone(self):
        done_cap = np.array(self.cap.grab(self.done_location))
        done_cap = cv2.cvtColor(done_cap, cv2.COLOR_BGR2GRAY)
        done_strings = ['GAME', 'GAHE']
        done=False
        # if np.sum(done_cap) < 44300000:
        #     done = True
        res = pytesseract.image_to_string(done_cap==172)[:4]
        if res in done_strings:
            done = True
        return done, done_cap