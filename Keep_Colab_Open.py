from mss import mss 
import pydirectinput
import cv2
import numpy as np
import pytesseract

from matplotlib import pyplot as plt
import time

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" #Path of tesseract 
class Colab():
    
    def __init__(self):
        
        super().__init__()
         
        self.cap = mss()
        self.window_loc = {'top':400, 'left':650, 'width':300, 'height':60}
        self.done_loc = {'top':430, 'left':660, 'width':250, 'height':60}
        
        
    def step(self):
        
        done, done_cap = self.get_done()
        new_obs = self.get_obs()
        
        return new_obs, done
                                                                                  
    
    def render(self):
        cv2.imshow('Screen',np.array(self.cap.grab(self.window_loc))[:,:,:3])
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.close()
    
    def reset(self):
        time.sleep(1)
        return self.get_obs()
        
    def close(self):
        cv2.destroyAllWindows()
    
    def get_obs(self):
        raw = np.array(self.cap.grab(self.window_loc))[:,:,:3] 
        
        gray = cv2.cvtColor(raw,cv2.COLOR_BGR2GRAY )
        
        resized = cv2.resize(gray, (100,83))
        
        channel = np.reshape(resized, (1,83,100))
        
        return channel
                            
    def get_done(self):
        done_cap = np.array(self.cap.grab(self.done_loc))[:,:,:3]
        
        strings = ['Hala','Orada', 'MISINIZ']
        #strings = ['Are','you', 'still',"there"] #For english
        
        done = False
        res = pytesseract.image_to_string(done_cap)[:4]
        
        if res in strings:
            done = True
            
        return done, done_cap
    
env = Colab()

done, done_cap = env.get_done()
plt.imshow(done_cap)

for episode in range(10):
    obs = env.reset()
    done = False
    

    while not done:
        obs, done = env.step()
        if done:
            pydirectinput.click(x=850,y=620)
        