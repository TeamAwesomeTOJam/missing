'''
Created on 2010-04-24

@author: daniel
'''

from entity import *
from tile import *

class EntityEditMode(object):
    
    def __init__(self,window,floors):
        self.window = window
        self.floors = floors
        self._floor_num = 0
        self.current_tile_x = 0
        self.current_tile_y = 0 
        self.camera_x = 0
        self.camera_y = 0
        self.orientation = 0
        self.delay = 0
        self.marks = 0
        self.last_door_trigger= None
        self.last_breaker_trigger = None
    
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
        for e in self.current_floor.entities:
            e.show()
        target = TargetEntity(self.current_floor,self.camera_x,self.camera_y)
        self.current_floor.add_entity(target)
        target.orientation = self.orientation
        self.current_floor.on_draw()
        self.current_floor.remove_entity(target)
    
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
            elif event == 'entity edit mode':
                for e in self.current_floor.entities:
                    e.hide()
                self.window.change_mode('game mode')
            elif event == 'edit mode':
                for e in self.current_floor.entities:
                    e.hide()
                self.window.change_mode('edit mode')
            elif event == 'delete':
                for e in self.current_floor.entities:
                    if math.fabs(e.x - self.camera_x) < tile_width/2 and math.fabs(e.y - self.camera_y) < tile_height/2:
                        if not e == self.current_floor.player and not e == self.current_floor.assistant:
                            self.current_floor.remove_entity(e)
            elif ord('0') <= ord(event[0]) <= ord('9'):
                self.delay = ord(event[0]) - ord('0')
            elif event == 'place orb':
                self.current_floor.add_entity(OrbEntity(self.current_floor, self.camera_x, self.camera_y))
            elif event == 'place ghoul':
                self.current_floor.add_entity(GhoulEntity(self.current_floor, self.camera_x, self.camera_y))
            elif event == 'place player':
                self.current_floor.player.x = self.camera_x
                self.current_floor.player.y = self.camera_y
            elif event == 'place assistant':
                self.current_floor.assistant.x = self.camera_x
                self.current_floor.assistant.y = self.camera_y
            elif event == 'place breaker trigger':
                t = BreakerTriggerEntity(self.current_floor,self.camera_x,self.camera_y,self.orientation,self.delay)
                self.last_breaker_trigger = t
                self.current_floor.add_entity(t)
            elif event == 'place door trigger':
                t = DoorTriggerEntity(self.current_floor,self.camera_x,self.camera_y,self.orientation,self.delay)
                self.last_door_trigger = t
                self.current_floor.add_entity(t)
            elif event == 'mark breaker':
                if self.last_breaker_trigger:
                    m = BreakerMarkEntity(self.current_floor,self.current_tile_x,self.current_tile_y,self.camera_x,self.camera_y,self.last_breaker_trigger)
                    self.current_floor.add_entity(m)
            elif event == 'mark door':
                if self.last_door_trigger:
                    m = DoorMarkEntity(self.current_floor,self.current_tile_x,self.current_tile_y,self.camera_x,self.camera_y,self.last_door_trigger)
                    self.current_floor.add_entity(m)
            elif event == 'place next floor':
                self.current_floor.add_entity(NextFloorEntity(self.current_floor, self.camera_x, self.camera_y))
            elif event == 'toggle lights':
                self.current_floor.do_lighting = not self.current_floor.do_lighting
            elif event == 'save':
                self.window.save()
    
    def exit(self):
        pass
        
    def enter(self):
        pass
