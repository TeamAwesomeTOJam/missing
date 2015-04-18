'''
Created on 2010-04-23

@author: daniel
'''

import pickle

import pyglet

from floor import Floor
from settings import playerspeed
from entity import PlayerEntity

class GameMode(object):
    '''
    classdocs are fun
    '''

    def __init__(self, window, floors):
        '''
        Constructor
        '''
        self.window = window
        self.floors = floors
        self._floor_num = 0
        self.load_new_floor(self.current_floor)
        self.camera_x = 0
        self.camera_y = 0
        
        self.music_player = pyglet.media.Player()
        self.music_player.eos_action = pyglet.media.Player.EOS_LOOP
        self.music_player.queue(pyglet.resource.media('music/spooky.wav'))
        self.music_player.play()
        
        #key states
        self.up_state = 0;
        self.down_state = 0;
        self.right_state = 0;
        self.left_state = 0;
    
    def _get_floor(self):
        return self.floors[self._floor_num]
    
    def _set_floor(self):
        pass
    
    current_floor = property(_get_floor, _set_floor)
    
    def _get_floor_num(self):
        return self._floor_num
    
    def _set_floor_num(self, num):
        self.load_new_floor(num)
    
    floor_um = property(_get_floor_num, _set_floor_num)
    
    def load_new_floor(self,floor):
        self.floor_num = floor
    
    def on_update(self, dt):
        self.current_floor.do_lighting = True
        self.current_floor.on_update(dt)
        self.camera_x = int(self.current_floor.player.x)
        self.camera_y = int(self.current_floor.player.y)
        if self.current_floor.lose:
            self.current_floor.lose = False
            self.window.change_mode('lose screen')
        if self.current_floor.win:
            self.current_floor.win = False
            self.window.change_mode('win screen')
    
    def on_draw(self):
        self.current_floor.on_draw()
    
    def on_event(self, updown, event): 
        if event == 'up':
            self.up_state = updown
        elif event == 'down':
            self.down_state = updown
        elif event == 'right':
            self.right_state = updown
        elif event == 'left':
            self.left_state = updown
        elif event == 'action':
            self.current_floor.player.action(updown)
        elif event == 'edit mode' and updown == 1:
            self.window.change_mode('edit mode')
        elif event == 'entity edit mode' and updown == 1:
            self.window.change_mode('entity edit mode')
            
        dx_ratio = self.right_state - self.left_state
        dy_ratio = self.up_state - self.down_state
        if(dx_ratio and dy_ratio):
            ratio = 0.75
        else:
            ratio  = 1
            
        self.current_floor.player.dy = playerspeed * dy_ratio * ratio
        self.current_floor.player.dx = playerspeed * dx_ratio * ratio
    
    def enter(self):
        self.window.load_floors()
        self.up_state=0
        self.down_state=0
        self.right_state=0
        self.left_state=0
        
    def exit(self):
        self.music_player.pause()
            
            