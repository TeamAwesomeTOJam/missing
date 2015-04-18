'''
Created on 2010-04-25

@author: daniel
'''

import pyglet

class SplashScreen(object):
    
    def __init__(self,window,next_mode,image):
        self.window = window
        self.sprite = pyglet.sprite.Sprite(image, 
                                           0,
                                           0)
        self.next_mode = next_mode
        self.camera_x = 1024/2
        self.camera_y = 768/2
    
    def on_event(self,updown,event):
        self.window.change_mode(self.next_mode)
        
    def on_draw(self):
        self.sprite.draw()
    
    def on_update(self,dt):
        pass
    
    def exit(self):
        pass
    
    def enter(self):
        pass

class WelcomeScreen(SplashScreen):
    
    def __init__(self,window):
        SplashScreen.__init__(self,window,'game mode',pyglet.resource.image('welcome_screen.png'))

class CreditsScreen(SplashScreen):
    
    def __init__(self,window):
        SplashScreen.__init__(self,window,'welcome screen',pyglet.resource.image('credits_screen.png'))

class LoseScreen(SplashScreen):
    
    def __init__(self,window):
        SplashScreen.__init__(self,window,'credits screen',pyglet.resource.image('lose_screen.png'))
  
class WinScreen(SplashScreen):
    
    def __init__(self,window):
        SplashScreen.__init__(self,window,'credits screen',pyglet.resource.image('win_screen.png'))      