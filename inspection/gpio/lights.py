#!/usr/bin/env python
# coding: utf-8

# In[6]:


from gpiozero import LED
# from signal import pause


# In[ ]:


class Signalling():
    red=LED(26)
    yellow=LED(19)
    green=LED(13)
    
    def __init__(self,threshold):
        self.threshold=threshold
        
    def signals():
        if self.threshold>0.5:
            self.red.on()
            print("red on")
        elif threshold > 0.3:
            self.yellow.on()
            print("yellow on")
        else:
            self.green.on()
            print("green on")
        sleep(2)
    

