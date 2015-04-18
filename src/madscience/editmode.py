'''
Created on 2010-04-24

@author: daniel
'''
from tile import *

class EditMode(object):
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
        self.current_tile_x = 0
        self.current_tile_y = 0 
        self.camera_x = 0
        self.camera_y = 0
        self.world = 'real'
        self.new_tile_ind = 1
        self.illumination = 0
        self.orientation = 0
    
    def on_update(self,dt):
        tile = self.current_floor.world_tiles[self.current_tile_x][self.current_tile_y]
        self.camera_x = tile.x
        self.camera_y = tile.y
        self.current_floor.lighting()
    
    def _get_floor(self):
        return self.floors[self._floor_num]
    
    def _set_floor(self):
        pass
    
    current_floor = property(_get_floor, _set_floor)
    
    def on_draw(self):
        self.current_floor.on_draw()
        tile = self.current_floor.world_tiles[self.current_tile_x][self.current_tile_y]
        if self.world == 'real':
            new_tile = world_tile_list[self.new_tile_ind]
        else:
            new_tile = other_tile_list[self.new_tile_ind]
        self.orientation = self.orientation % new_tile.num_orientations
        new_tile(self.current_floor,self.illumination / 9.0 ,tile.x, tile.y,self.orientation).sprite.draw()
        
    
    def on_event(self,updown,event):
        if updown == 1:
            if event == 'up' and self.current_tile_y < len(self.current_floor.world_tiles[0]) - 1:
                self.current_tile_y += 1
            elif event == 'down' and self.current_tile_y > 0:
                self.current_tile_y -= 1
            elif event == 'right' and self.current_tile_x < len(self.current_floor.world_tiles) - 1:
                self.current_tile_x += 1
            elif event == 'left' and self.current_tile_x > 0:
                self.current_tile_x -= 1
            elif event ==  'action':
                tile = self.current_floor.world_tiles[self.current_tile_x][self.current_tile_y]
                if self.world == 'real':
                    new_tile = world_tile_list[self.new_tile_ind]
                    self.current_floor.world_tiles[self.current_tile_x][self.current_tile_y] = new_tile(self.current_floor, self.illumination / 9.0, tile.x, tile.y, self.orientation)
                else:
                    new_tile = other_tile_list[self.new_tile_ind]
                    self.current_floor.other_tiles[self.current_tile_x][self.current_tile_y] = new_tile(self.current_floor, 1, tile.x, tile.y, self.orientation)
            elif event == 'edit mode':
                self.window.change_mode('game mode')
            elif event == 'entity edit mode':
                self.window.change_mode('entity edit mode')
            elif event == 'next tile':
                if self.world == 'real':
                    self.new_tile_ind = (self.new_tile_ind + 1) % len(world_tile_list)
                else:
                    self.new_tile_ind = (self.new_tile_ind + 1) % len(other_tile_list)
            elif event == 'next world':
                if self.world == 'real':
                    self.world = 'other'
                    self.new_tile_ind = self.new_tile_ind % len(other_tile_list)
                else:
                    self.new_tile_ind = self.new_tile_ind % len(world_tile_list)
                    self.world = 'real'
            elif ord('0') <= ord(event[0]) <= ord('9'):
                self.illumination = ord(event[0]) - ord('0')
            elif event == 'change illumination':
                self.current_floor.world_tiles[self.current_tile_x][self.current_tile_y].base_illumination = self.illumination
            elif event == 'rotate':
                if self.world == 'real':
                    new_tile = world_tile_list[self.new_tile_ind]
                else:
                    new_tile = other_tile_list[self.new_tile_ind] 
                self.orientation = (self.orientation + 1) % new_tile.num_orientations
            elif event == 'toggle lights':
                self.current_floor.do_lighting = not self.current_floor.do_lighting
            elif event == 'save':
                self.window.save()
    
    def exit(self):
        pass
    
    def enter(self):
        pass
                
            
        
        
        
