'''
Created on Apr 23, 2010

@author: jonathan
'''
import pyglet
import gamemode
import editmode
import entityeditmode
import os
from settings import keymap
from floor import Floor
from entity import *
from tile import world_tile_list, other_tile_list
from splashscreen import *


class GameWindow(pyglet.window.Window):
    '''
    classdocs
    '''

    def __init__(self,load_file):
        '''
        Constructor
        '''
        pyglet.window.Window.__init__(self, fullscreen=True)
        self.load_file = load_file
        self.floors = []
        self.load_floors()
        self._modes = {'game mode':gamemode.GameMode(self,self.floors),
                       'edit mode':editmode.EditMode(self,self.floors),
                       'entity edit mode':entityeditmode.EntityEditMode(self,self.floors),
                       'welcome screen': WelcomeScreen(self),
                       'credits screen': CreditsScreen(self),
                       'lose screen': LoseScreen(self),
                       'win screen':WinScreen(self)
                       }
        self._mode = None
        self.change_mode('welcome screen')
        self.fps_display = pyglet.clock.ClockDisplay()

    def on_draw(self):
        self.clear()
        if self.mode:
            pyglet.gl.glPushMatrix()
            pyglet.gl.glTranslatef(self.width / 2.0 - self.mode.camera_x,
                               self.height / 2.0 -self.mode.camera_y, 
                               0)
            self.mode.on_draw()
            pyglet.gl.glPopMatrix()
        self.fps_display.draw()
        
    def _get_mode(self):
        if self._mode in self._modes:
            return self._modes[self._mode]
        else:
            return None
    
    def _set_mode(self, mode):
        pass
    
    mode = property(_get_mode, _set_mode)
    
    def change_mode(self, new_mode):
        if self.mode:
            pyglet.clock.unschedule(self.mode.on_update)
            self.mode.exit()
        self._mode = new_mode
        self.mode.enter();
        pyglet.clock.schedule(self.mode.on_update)
        
    def on_key_press(self,symbol,modifiers):
        if symbol in keymap:
            s = keymap[symbol]
            if s == 'quit':
                self.on_close()
            elif s == 'full screen':
                self.set_fullscreen(not self.fullscreen)
            else:
                self.mode.on_event(1, s)
        else:
            self.mode.on_event(1, 'any key')
    
    def on_key_release(self,symbol,modifiers):
        if symbol in keymap:
            self.mode.on_event(0, keymap[symbol])
        else:
            self.mode.on_event(1, 'any key')
    
    def load_floors(self):
        del self.floors[:]
        if self.load_file and os.path.exists(self.load_file):
            f = open(self.load_file,'r')
            floors = []
            last_breaker_trigger = None
            last_door_trigger = None
            tile_list = world_tile_list
            for line in f:
                line = line[:-1]
                s = line.split(':')
                if s[0] == 'floor':
                    new_floor = Floor(int(s[1]), int(s[2]))
                    floors.append(new_floor)
                    new_floor.world_tiles = []
                    new_floor.other_tiles = []
                    
                elif s[0] == 'world':
                    tile_list = world_tile_list
                    append_list = floors[-1].world_tiles
                elif s[0] == 'other':
                    tile_list = other_tile_list
                    append_list = floors[-1].other_tiles
                elif s[0] == 'col':
                    append_list.append([])
                elif s[0] == 'tile':
                    new_tile = tile_list[int(s[1])]
                    floor = floors[-1]
                    illum = float(s[2])
                    x = int(s[3])
                    y = int(s[4])
                    o = int(s[5])
                    append_list[-1].append(new_tile(floor, illum ,x ,y, o))
                elif s[0] == 'entity':
                    if s[1] == 'AssistantEntity':
                        floors[-1].assistant.x = int(s[2])
                        floors[-1].assistant.y = int(s[3])
                    elif s[1] == 'GhoulEntity':
                        floors[-1].add_entity(GhoulEntity(floors[-1], int(s[2]), int(s[3])))
                    elif s[1] == 'PlayerEntity':
                        floors[-1].player.x = int(s[2])
                        floors[-1].player.y = int(s[3])
                    elif s[1] == 'OrbEntity':
                        floors[-1].add_entity(OrbEntity(floors[-1], int(s[2]), int(s[3])))
                    elif s[1] == 'DoorTriggerEntity':
                        last_door_trigger = DoorTriggerEntity(floors[-1], int(s[2]), int(s[3]), int(s[4]), int(s[5]))
                        last_door_trigger.hide()
                        floors[-1].add_entity(last_door_trigger)
                    elif s[1] == 'BreakerTriggerEntity':
                        last_breaker_trigger = BreakerTriggerEntity(floors[-1], int(s[2]), int(s[3]), int(s[4]), int(s[5]))
                        last_breaker_trigger.hide()
                        floors[-1].add_entity(last_breaker_trigger)
                    elif s[1] == 'DoorMarkEntity':
                        mark = DoorMarkEntity(floors[-1], int(s[2]), int(s[3]), int(s[4]), int(s[5]), last_door_trigger)
                        floors[-1].add_entity(mark)
                        mark.hide()
                    elif s[1] == 'BreakerMarkEntity':
                        mark = BreakerMarkEntity(floors[-1], int(s[2]), int(s[3]), int(s[4]), int(s[5]), last_breaker_trigger)
                        floors[-1].add_entity(mark)
                        mark.hide()
    
                   
            #self.floors = floors 
            for f in floors:
                self.floors.append(f)
        else:
            self.floors.append(Floor(20,20))
            #self.floors = [Floor(20,20)]
            
    def save(self):
        if self.load_file:
            f = open(self.load_file,'w')
            for floor in self.floors:
                f.write('floor:%i:%i\n' % (floor.width,floor.height))
                f.write('world\n')
                for col in floor.world_tiles:
                    f.write('col\n')
                    for t in col:
                        i = 0
                        for c in world_tile_list:
                            if isinstance(t,c):
                                break
                            i += 1
                        f.write('tile:%i:%f:%i:%i:%i\n' % (i, t.base_illumination,t.x,t.y,t.orientation))
                f.write('other\n')
                for col in floor.other_tiles:
                    f.write('col\n')
                    for t in col:
                        i = 0
                        for c in other_tile_list:
                            if isinstance(t,c):
                                break
                            i += 1
                        f.write('tile:%i:%f:%i:%i:%i\n' % (i, t.base_illumination,t.x,t.y,t.orientation))
                f.write('entities\n')
                for e in floor.entities:
                    if isinstance(e, AssistantEntity):
                        f.write('entity:AssistantEntity:%i:%i\n' % (e.x, e.y))
                    elif isinstance(e, GhoulEntity):
                        f.write('entity:GhoulEntity:%i:%i\n' % (e.x, e.y))
                    elif isinstance(e, PlayerEntity):
                        f.write('entity:PlayerEntity:%i:%i\n' % (e.x, e.y))
                    elif isinstance(e, OrbEntity):
                        f.write('entity:OrbEntity:%i:%i\n' % (e.x, e.y))
                    elif isinstance(e, DoorTriggerEntity):
                        f.write('entity:DoorTriggerEntity:%i:%i:%i:%i\n' % (e.x, e.y, e.orientation, e.delay))
                        for m in e.marks:
                            f.write('entity:DoorMarkEntity:%i:%i:%i:%i\n' % (m.tile_x, m.tile_y, m.x, m.y))
                    elif isinstance(e, BreakerTriggerEntity):
                        f.write('entity:BreakerTriggerEntity:%i:%i:%i:%i\n' % (e.x, e.y, e.orientation, e.delay))
                        for m in e.marks:
                            f.write('entity:BreakerMarkEntity:%i:%i:%i:%i\n' % (m.tile_x, m.tile_y, m.x, m.y))
                        
            f.close()
    
    def on_close(self):
        pyglet.window.Window.on_close(self)
        
        